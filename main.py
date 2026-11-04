import argparse
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def load_env_file():
    if not os.path.exists(".env"):
        return

    with open(".env", encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            name, value = line.split("=", 1)
            os.environ.setdefault(name.strip(), value.strip().strip('"\''))


load_env_file()

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
EXPECTED_EMAIL = os.getenv("GMAIL_EMAIL", "").strip()
CLIENT_SECRETS_FILE = os.getenv("GMAIL_CREDENTIALS_FILE", "credentials.json").strip()
TOKEN_SCOPE_FILE = "token.scope"


def authenticate():
    if not EXPECTED_EMAIL:
        raise ValueError("GMAIL_EMAIL is missing from .env")
    if not CLIENT_SECRETS_FILE:
        raise ValueError("GMAIL_CREDENTIALS_FILE is missing from .env")
    if not os.path.exists(CLIENT_SECRETS_FILE):
        raise FileNotFoundError(
            f"Credentials file not found: {CLIENT_SECRETS_FILE}"
        )

    creds = None

    has_expected_scope = False
    if os.path.exists(TOKEN_SCOPE_FILE):
        with open(TOKEN_SCOPE_FILE, encoding="utf-8") as scope_file:
            has_expected_scope = scope_file.read().strip() == SCOPES[0]

    if os.path.exists("token.json") and has_expected_scope:
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    elif os.path.exists("token.json"):
        os.remove("token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0, prompt="consent")

        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())
        with open(TOKEN_SCOPE_FILE, "w", encoding="utf-8") as scope_file:
            scope_file.write(SCOPES[0])

    service = build("gmail", "v1", credentials=creds)
    profile = service.users().getProfile(userId="me").execute()
    actual_email = profile.get("emailAddress", "")

    if actual_email.lower() != EXPECTED_EMAIL.lower():
        raise ValueError(f"Wrong account! Authenticated as {actual_email}")

    print(f"\nConnected to: {actual_email}")
    return service


def mark_all_emails(service, mark_as_unread):
    page_token = None
    total_emails = 0
    action = "unread" if mark_as_unread else "read"

    print(f"\nMarking all emails as {action}...\n")

    while True:
        response = service.users().messages().list(
            userId="me",
            maxResults=500,
            pageToken=page_token,
            includeSpamTrash=True,
        ).execute()

        message_ids = [item["id"] for item in response.get("messages", [])]

        if message_ids:
            service.users().messages().batchModify(
                userId="me",
                body={
                    "ids": message_ids,
                    "addLabelIds": ["UNREAD"] if mark_as_unread else [],
                    "removeLabelIds": [] if mark_as_unread else ["UNREAD"],
                },
            ).execute()
            total_emails += len(message_ids)
            print(f"Marked {total_emails} emails {action}")

        page_token = response.get("nextPageToken")
        if not page_token:
            break

    print("\n------------------------------")
    print(f"ALL EMAILS MARKED AS {action.upper()}")
    print("------------------------------")
    print(f"Total emails updated: {total_emails}")


def main():
    parser = argparse.ArgumentParser(
        description="Mark all Gmail messages as read or unread."
    )
    parser.add_argument(
        "action",
        nargs="?",
        choices=["0", "1"],
        help="Use 0 to mark all messages read, or 1 to mark all messages unread.",
    )
    args = parser.parse_args()
    action = args.action

    if action is None:
        print("\nWhat would you like to do?")
        print("0 - Mark all messages as read")
        print("1 - Mark all messages as unread")
        action = input("Enter 0 or 1: ").strip()

        if action not in {"0", "1"}:
            parser.error("Please enter only 0 or 1.")

    try:
        service = authenticate()
        mark_all_emails(service, mark_as_unread=action == "1")
    except Exception as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
