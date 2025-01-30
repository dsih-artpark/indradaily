import logging
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

logger = logging.getLogger(__name__)

def send_email(recipients: dict, subject: str, body: str, config: dict,
               attachment: bool = False, attachment_path: Optional[str] = None,
               from_name: Optional[str] = "Automatic Notifications | DSIH Admin"):

    logger.info("Starting to send email")

    receiver_emails = list(recipients.keys())
    SMTP_SERVER = config.get('SMTP_SERVER', 'smtp.gmail.com')
    PORT = config.get('PORT', 587)
    EMAIL = config.get('EMAIL')
    PASSWORD = config.get('PASSWORD')

    logger.debug(f"SMTP_SERVER: {SMTP_SERVER}, PORT: {PORT}, EMAIL: {EMAIL}")

    message = MIMEMultipart()
    message["From"] = from_name
    message["To"] = ", ".join([f"{name} <{email}>" for email, name in recipients.items()])
    message["Subject"] = subject

    logger.debug(f"Email subject: {subject}")
    logger.debug(f"Email recipients: {message['To']}")

    message.attach(MIMEText(body, "plain"))

    if attachment:
        filename = attachment_path
        logger.info(f"Attaching file: {filename}")

        try:
            with open(filename, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)

            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename.replace("/", "_")}",
            )

            message.attach(part)
        except Exception as e:
            logger.error(f"Failed to attach file: {e}")
            raise

    text = message.as_string()

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(SMTP_SERVER, PORT) as server:
            logger.info("Connecting to email server")
            server.starttls(context=context)
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, receiver_emails, text)
            logger.info("Email sent successfully")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        raise
