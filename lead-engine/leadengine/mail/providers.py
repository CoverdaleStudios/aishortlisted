"""Pluggable email delivery. Pick one in Settings -> email_provider.

- outbox  (default): writes each approved email as a .eml file to exports/outbox/. Nothing is sent.
                     Open the file in Outlook / Apple Mail / Thunderbird to send, or keep as a record.
- smtp           : sends through any mailbox with SMTP (Google Workspace, Microsoft 365, cPanel host...).
                   Password comes from the LEADENGINE_SMTP_PASSWORD environment variable, never the database.
- gmail / outlook: placeholders for OAuth API connectors (Gmail API / Microsoft Graph) - not wired up yet.
"""
import os
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formataddr, make_msgid
from pathlib import Path

EXPORTS = Path(__file__).resolve().parents[2] / "exports" / "outbox"


def build_message(settings: dict, to: str, subject: str, body: str) -> EmailMessage:
    msg = EmailMessage()
    sender = settings.get("smtp_from") or settings["business_email"]
    msg["From"] = formataddr((f"{settings['sender_name']} - {settings['business_name']}", sender))
    msg["To"] = to
    msg["Subject"] = subject
    msg["Reply-To"] = sender
    msg["Message-ID"] = make_msgid(domain=sender.split("@")[-1])
    # One-click-style opt-out by email (Spam Act: functional unsubscribe).
    msg["List-Unsubscribe"] = f"<mailto:{sender}?subject=unsubscribe>"
    msg.set_content(body)
    return msg


class Provider:
    name = "base"

    def send(self, msg: EmailMessage) -> str:
        raise NotImplementedError


class OutboxProvider(Provider):
    name = "outbox"

    def send(self, msg: EmailMessage) -> str:
        EXPORTS.mkdir(parents=True, exist_ok=True)
        safe = "".join(ch if ch.isalnum() else "_" for ch in msg["To"])[:60]
        path = EXPORTS / f"{msg['Message-ID'].strip('<>').split('@')[0]}_{safe}.eml"
        msg["X-Unsent"] = "1"  # Outlook opens it as a ready-to-send draft
        path.write_bytes(bytes(msg))
        return str(path)


class SMTPProvider(Provider):
    name = "smtp"

    def __init__(self, settings: dict):
        self.host = settings.get("smtp_host")
        self.port = int(settings.get("smtp_port") or 587)
        self.username = settings.get("smtp_username")
        self.password = os.environ.get("LEADENGINE_SMTP_PASSWORD")
        if not (self.host and self.username and self.password):
            raise RuntimeError("SMTP needs smtp_host, smtp_username (Settings) and LEADENGINE_SMTP_PASSWORD (env).")

    def send(self, msg: EmailMessage) -> str:
        ctx = ssl.create_default_context()
        if self.port == 465:
            with smtplib.SMTP_SSL(self.host, self.port, context=ctx, timeout=30) as s:
                s.login(self.username, self.password)
                s.send_message(msg)
        else:
            with smtplib.SMTP(self.host, self.port, timeout=30) as s:
                s.starttls(context=ctx)
                s.login(self.username, self.password)
                s.send_message(msg)
        return msg["Message-ID"]


class NotConnectedProvider(Provider):
    def __init__(self, name: str):
        self.name = name

    def send(self, msg: EmailMessage) -> str:
        raise RuntimeError(f"The {self.name} connector isn't set up yet - use 'outbox' or 'smtp' for now "
                           "(see README: Connecting email).")


def get_provider(settings: dict) -> Provider:
    choice = settings.get("email_provider", "outbox")
    if choice == "outbox":
        return OutboxProvider()
    if choice == "smtp":
        return SMTPProvider(settings)
    return NotConnectedProvider(choice)
