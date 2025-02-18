import logging
import os
import smtplib
import ssl
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def send_email(recipients: dict, subject: str, body: str, config: dict,
               attachment: bool = False, attachment_path: Optional[str] = None,
               from_name: Optional[str] = "Automatic Notifications | DSIH Admin"):
    """
    Send an email to the recipients with the given subject and body.

    :param recipients: dict
        A dictionary of recipients with email addresses as keys and names as values.
    :param subject: str
        The subject of the email.
    :param body: str
        The body of the email.
    :param config: dict
        A dictionary of configuration parameters for the email.
    :param attachment: bool
        A boolean flag indicating whether to attach a file to the email.
    :param attachment_path: Optional[str]
        The path to the file to attach to the email.
    :param from_name: Optional[str]
        The name of the sender of the email.

    :return: bool
        A boolean flag indicating whether the email was sent successfully.

    :raises Exception:
        If the email fails to send, an exception is raised.
    """

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

        logger.info(f"Attaching file: {attachment_path}")

        try:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            encoders.encode_base64(part)

            attachment_name = attachment_path.replace("/", "_")
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {attachment_name}",
            )

            message.attach(part)
        except Exception as e:
            logger.error(f"Failed to attach file {attachment_path}: {e}")
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


def data_upload_email(upload_success: bool, recipients: dict, dataset_name: str, dataset_source: str,
                        no_files: int, latest_timestamp: datetime, attachment: bool = False):
    load_dotenv()
    config = {
        'SMTP_SERVER': os.getenv('SMTP_SERVER'),
        'PORT': os.getenv('PORT'),
        'EMAIL': os.getenv('EMAIL'),
        'PASSWORD': os.getenv('PASSWORD')
    }

    current_date = datetime.now().strftime("%Y-%m-%d")
    current_month = datetime.now().strftime("%Y-%m")
    log_file = f"logs/indrafetch-{current_month}-debug.log"

    latest_timestamp = latest_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    attachment_path = log_file

    if upload_success:
        status = "SUCCESSFUL"
        body = (
            f"Hello,\n"
            f"This is a system generated email. All {no_files} files obtained from {dataset_name} "
            f"on {dataset_source} have been successfully uploaded to S3 on {current_date}.\n"
            f"The last timestamp of data availability for {dataset_name} is {latest_timestamp} UTC, "
            f"when checked at approximately {current_timestamp} UTC.\n"
            f"Detailed health of the run can be found in the debug log file for the "
            f"current month on the server: {log_file}."
        )
    else:
        status = "FAILED"
        subject = f"{dataset_name} Daily data upload to S3 failed"
        body = (
            f"Hello,\n"
            f"This is a system generated email. One or more files from {dataset_name} "
            f"on {dataset_source} have failed to upload to S3 on {current_date}.\n"
            f"The last timestamp of data availability for {dataset_name} is {latest_timestamp} UTC, "
            f"when checked at approximately {current_timestamp} UTC.\n"
            f"Detailed health of the run can be found in the attached debug log file."
        )
        attachment = True

    subject = f"{dataset_name} Daily Data Run {status} on {current_date}"
    send_email(recipients=recipients, subject=subject, body=body, config=config,
               attachment=attachment, attachment_path=attachment_path)

    return True

__all__ = ["data_upload_email", "send_email"]
