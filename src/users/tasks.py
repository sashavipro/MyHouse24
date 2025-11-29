"""src/users/tasks.py."""

import logging
import smtplib

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task
def send_invitation_email_task(email, link):
    """Send invitation email with the activation link."""
    subject = "Приглашение в систему МойДом24"  # noqa: RUF001
    message = (
        f"Здравствуйте!\n\n"
        f'Вы были добавлены как владелец квартиры в системе "МойДом24".\n'  # noqa: RUF001
        f"Чтобы активировать аккаунт и задать пароль, перейдите по ссылке:\n\n"
        f"{link}\n\n"
        f"Ссылка одноразовая."
    )

    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
    except (smtplib.SMTPException, ConnectionError, OSError):
        logger.exception("Failed to send email to %s", email)
