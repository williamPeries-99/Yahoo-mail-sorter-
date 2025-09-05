# email_sorter_background.py
import time
import socket
import imaplib
from email_sorter_core import process_emails, load_config

def login_to_imap(config):
    try:
        mail = imaplib.IMAP4_SSL("imap.mail.yahoo.com")
        mail.login(config["email"], config["password"])
        mail.sock.settimeout(20)
        print(f"[LOGIN] Logged in as {config['email']}")
        return mail
    except Exception as e:
        print(f"[LOGIN ERROR] {e}")
        return None

def keep_running_scheduler():
    mail = None
    while True:
        config = load_config()
        interval = config.get("interval_seconds", 60)

        try:
            if not mail:
                mail = login_to_imap(config)
                if not mail:
                    print("Retrying in 60 seconds...")
                    time.sleep(60)
                    continue

            print("[INFO] Running email sorter...")
            process_emails(mail, config)
            print(f"[WAIT] Waiting {interval} seconds...\n")
        except (imaplib.IMAP4.abort, imaplib.IMAP4.error, socket.timeout) as e:
            print(f"[SESSION ERROR] {e}. Reconnecting...")
            try:
                if mail:
                    mail.logout()
            except:
                pass
            mail = None  # force re-login on next loop
        except Exception as e:
            print(f"[UNEXPECTED ERROR] {e}")
        finally:
            time.sleep(interval)

if __name__ == "__main__":
    keep_running_scheduler()
