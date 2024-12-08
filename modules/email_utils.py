import smtplib
import email
import ssl
import os
import modules.config as config


def prepare_newsletter(
        sender: str,
        recipient: str,
        topic: str,
        newsletter: str
) -> bytes:
    email_message = email.message.Message()
    email_message.add_header('from', f"{config.APP_TITLE} <{sender}>")
    email_message.add_header('to', recipient)
    email_message.add_header(
        'subject', f"[{config.APP_TITLE}] Today's {topic} News"
    )
    email_message.set_payload(newsletter)

    return email_message.as_string().encode("utf-8")


def send_newsletter(
        topic: str,
        newsletter: str
) -> None:
    host = config.APP_EMAIL_HOST
    port = config.APP_EMAIL_PORT
    username = os.getenv("APP_EMAIL_USER")
    password = os.getenv("APP_EMAIL_PASS")
    context = ssl.create_default_context()
    sender = os.getenv("APP_EMAIL_INBOX")
    recipient = os.getenv("APP_EMAIL_INBOX")

    email_message = prepare_newsletter(sender, recipient, topic, newsletter)

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(sender, recipient, email_message)
