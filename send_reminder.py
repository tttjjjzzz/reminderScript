"""
send_reminder.py

Sends a reminder email via Gmail SMTP.
Designed to be invoked by Windows Task Scheduler.
"""

import sys
import os
import logging
import smtplib
from email.message import EmailMessage
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).resolve().parent

REQUIRED_VARS = [
    "GMAIL_ADDRESS",
    "GMAIL_APP_PASSWORD",
    "RECIPIENT_EMAIL",
    "EMAIL_SUBJECT",
    "EMAIL_BODY",
]


def configure_logging():
    log_file = SCRIPT_DIR / "reminder.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, encoding="utf-8"),
        ],
    )


def load_config():
    load_dotenv(dotenv_path=SCRIPT_DIR / ".env")

    config = {}
    missing = []
    for var in REQUIRED_VARS:
        value = os.getenv(var)
        if not value or value.strip() == "":
            missing.append(var)
        else:
            config[var] = value.strip()

    if missing:
        logging.error("Missing required environment variables: %s", ", ".join(missing))
        sys.exit(1)

    return config


def send_email(config):
    msg = EmailMessage()
    msg["From"] = config["GMAIL_ADDRESS"]
    msg["To"] = config["RECIPIENT_EMAIL"]
    msg["Subject"] = config["EMAIL_SUBJECT"]
    msg.set_content(config["EMAIL_BODY"])

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as server:
        server.login(config["GMAIL_ADDRESS"], config["GMAIL_APP_PASSWORD"])
        server.send_message(msg)


def main():
    configure_logging()
    logging.info("Reminder script started at %s", datetime.now().isoformat())

    config = load_config()

    try:
        send_email(config)
        logging.info("Email sent successfully to %s", config["RECIPIENT_EMAIL"])
    except smtplib.SMTPAuthenticationError:
        logging.error("Gmail authentication failed. Check your email and app password.")
        sys.exit(1)
    except smtplib.SMTPException as exc:
        logging.error("SMTP error: %s", exc)
        sys.exit(1)
    except OSError as exc:
        logging.error("Network error: %s", exc)
        sys.exit(1)

    logging.info("Reminder script finished.")


if __name__ == "__main__":
    main()
