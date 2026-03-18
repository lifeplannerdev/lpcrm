import ssl
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

SUPPORT_EMAIL = "lifeplannerinfo1@gmail.com"
FROM_EMAIL = "Lifeplanner Universal <lifeplannerinfo1@gmail.com>"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "lifeplannerinfo1@gmail.com"
SMTP_PASSWORD = "qnwsisxmpmkghwwd"


def send_conversion_email(lead) -> bool:
    if not lead.email:
        logger.warning("Conversion email skipped for lead #%s — no email on record.", lead.id)
        return False

    program = lead.program or "Your Enrolled Program"
    subject = "Your Application Has Been Successfully Converted – Lifeplanner Universal"
    body = f"""Greetings from Lifeplanner Universal!

Dear {lead.name},

We are pleased to inform you that your application has been successfully converted.


Our team will get in touch with you shortly with further details.

For any queries, contact us at {SUPPORT_EMAIL}.

Warm regards,
Team Lifeplanner Universal"""

    try:
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = lead.email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, lead.email, msg.as_string())

        logger.info("Conversion email sent to %s for lead #%s.", lead.email, lead.id)
        return True

    except Exception as exc:
        logger.error("Failed to send conversion email to %s for lead #%s: %s", lead.email, lead.id, exc)
        return False