import imaplib
import email
import json
import os
import socket
from email.utils import parseaddr
from datetime import datetime

CONFIG_FILE = "config.json"
LOG_FILE = "log.txt"
LAST_UID_FILE = "last_uid.txt"

def log(message):
    msg = f"{datetime.now()} - {message}"
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def load_last_uid():
    if os.path.exists(LAST_UID_FILE):
        with open(LAST_UID_FILE, "r") as f:
            return f.read().strip()
    return None

def save_last_uid(uid):
    with open(LAST_UID_FILE, "w") as f:
        f.write(uid)

def process_emails():
    config = load_config()
    if not config.get("email") or not config.get("password"):
        log("Missing credentials in config.json")
        return

    try:
        mail = imaplib.IMAP4_SSL("imap.mail.yahoo.com")
        mail.login(config["email"], config["password"])
        mail.sock.settimeout(20)
        log(f"Logged in as {config['email']}")
    except Exception as e:
        log(f"Login failed: {e}")
        return

    try:
        mail.select(config.get("source_folder", "INBOX"), readonly=True)  # Read-only mode

        last_uid = load_last_uid()
        search_criteria = "ALL" if not last_uid else f"UID {int(last_uid)+1}:*"

        status, messages = mail.uid("search", None, search_criteria)
        if status != "OK":
            log("Failed to retrieve emails.")
            return

        email_uids = messages[0].split()
        total = len(email_uids)
        if total == 0:
            log("No new emails to process.")
            return

        log(f"Found {total} email(s) to process.")
        latest_uid = last_uid

        mail.sock.settimeout(15)

        for i, uid in enumerate(email_uids, 1):
            try:
                status, msg_data = mail.uid("fetch", uid, "(BODY.PEEK[])")  # Do NOT mark as read
                if status != "OK":
                    log(f"[{i}/{total}] Failed to fetch email UID {uid}")
                    continue

                msg = email.message_from_bytes(msg_data[0][1])
                sender = parseaddr(msg.get("From"))[1]

                if sender.lower() in config["important_senders"]:
                    result = mail.uid("COPY", uid, config["destination_folder"])
                    if result[0] == "OK":
                        log(f"Copied email from {sender} to {config['destination_folder']}")
                    else:
                        log(f"Failed to copy email UID {uid}")
                else:
                    log(f"Skipped email from {sender}")

                latest_uid = uid.decode()

            except Exception as e:
                log(f"[{i}/{total}] Error processing UID {uid}: {e}")
                continue

        if latest_uid:
            save_last_uid(latest_uid)
            log(f"Saved last processed UID: {latest_uid}")

        mail.logout()
        log("Email sorting complete.")

    except Exception as e:
        log(f"Error during processing: {e}")
