import logging
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

SUPPORT_EMAIL = "info@lifeplanneruniversal.com"
FROM_EMAIL = "Lifeplanner Universal <info@lifeplanneruniversal.com>"


def send_conversion_email(lead) -> bool:
    if not lead.email:
        logger.warning("Conversion email skipped for lead #%s — no email on record.", lead.id)
        return False

    program = lead.program or "Your Enrolled Program"

    subject = "Your Application Has Been Successfully Converted – Lifeplanner Universal"

    message = f"""Greetings from Lifeplanner Universal!

Dear {lead.name},

We are pleased to inform you that your application has been successfully converted.

Program : {program}
Status  : Converted

Our team will get in touch with you shortly with further details.

For any queries, contact us at {SUPPORT_EMAIL}.

Warm regards,
Team Lifeplanner Universal"""

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=FROM_EMAIL,
            recipient_list=[lead.email],
            fail_silently=False,
        )
        logger.info("Conversion email sent to %s for lead #%s.", lead.email, lead.id)
        return True

    except Exception as exc:
        logger.error("Failed to send conversion email to %s for lead #%s: %s", lead.email, lead.id, exc)
        return False