# GmailReader

Marks all messages in the configured Gmail account as unread using the Gmail API modify scope.

## Setup

1. Create a Google Cloud project, enable the Gmail API, and download an OAuth desktop-app client file.
2. Save that file as `credentials.json` in this directory.
3. Create a `.env` file:

```text
GMAIL_EMAIL=youremaiiid@gmail.com
GMAIL_CREDENTIALS_FILE=credentials.json
```

4. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

5. Run the reader:

```powershell
python main.py
```

The first run opens a browser for Google authorization and creates `token.json`. The authenticated account must be `rahulsnsihub@gmail.com`. Subsequent runs reuse the token and mark all messages, including messages in Spam and Trash, as unread.

Do not commit `credentials.json`, `token.json`, or `emails.jsonl`; they are ignored by Git.
