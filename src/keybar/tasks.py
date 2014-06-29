import logging

from django.core.mail import send_mail as django_send_mail

from keybar.celery import celery


@celery.task(ignore_result=True, bind=True)
def send_mail_async(self, subject, message, from_email, recipient_list):
    logger = logging.getLogger('keybar.tasks.send_mail_async')
    try:
        django_send_mail(subject, message, from_email, recipient_list,
                         fail_silently=False)
        logger.debug("Successfully sent email message to %r.",
            ', '.join(recipient_list))
    except Exception as exc:
        # catching all exceptions b/c it could be any number of things
        # depending on the backend
        logger.warning("Failed to send email message to %r, retrying.",
            ', '.join(recipient_list))
        self.retry(exc=exc, retry_countdown=60)
