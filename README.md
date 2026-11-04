# GmailReader

A command-line tool to bulk mark **all messages** in a Gmail account as **read** or **unread** using the Gmail API — including messages in Spam and Trash.

---

## What It Does

- Authenticates with your Gmail account via **OAuth 2.0**
- Lets you choose to mark **all messages as read** or **all messages as unread**
- Processes messages in batches of 500 for efficiency
- Covers **every folder**: Inbox, Sent, Spam, Trash, and all labels
- Verifies you are signed in to the correct Gmail account before making any changes
- Reuses a saved token on subsequent runs — no repeated browser login needed

---

## Setup

### 1. Create Google Cloud credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select an existing one)
3. Enable the **Gmail API**
4. Go to **APIs & Services → Credentials → Create Credentials → OAuth client ID**
5. Choose **Desktop app**, then download the JSON file
6. Save it as `credentials.json` in this directory

### 2. Create a `.env` file

```text
GMAIL_EMAIL=your-email@gmail.com
GMAIL_CREDENTIALS_FILE=credentials.json
```

Replace `your-email@gmail.com` with the Gmail address you want to use.

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run the tool

```powershell
python main.py
```

---

## Usage

### Interactive mode (no arguments)

```powershell
python main.py
```

You will be prompted:

```
What would you like to do?
0 - Mark all messages as read
1 - Mark all messages as unread
Enter 0 or 1:
```

### Command-line argument mode

```powershell
# Mark all messages as READ
python main.py 0

# Mark all messages as UNREAD
python main.py 1
```

---

## First Run

The first run opens a browser window for Google authorization. After you approve access, a `token.json` file is saved locally so future runs do not require re-authorization.

> **Note:** The authenticated Google account must match the `GMAIL_EMAIL` set in your `.env` file. If it does not match, the tool will exit with an error.

---

## Security

The following files contain sensitive credentials and are excluded from Git:

| File | Description |
|------|-------------|
| `credentials.json` | Your Google OAuth client secrets |
| `token.json` | Your saved access/refresh token |
| `emails.jsonl` | Any exported email data |

> **Never share or commit these files.**

---

## Requirements

- Python 3.8+
- A Google account with Gmail API access enabled
