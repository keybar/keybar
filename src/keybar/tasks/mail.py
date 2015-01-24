from django.core.mail import send_mail as django_send_mail

from keybar.tasks import celery
from keybar.utils.logging import logged


@logged
@celery.task(ignore_result=True, bind=True)
def send_mail_async(self, subject, message, from_email, recipient_list):
    try:
        django_send_mail(
            subject, message, from_email, recipient_list, fail_silently=False)
        self.logger.debug(
            'Successfully sent email message to %r.', ', '.join(recipient_list))
    except Exception as exc:
        # catching all exceptions b/c it could be any number of things
        # depending on the backend
        self.logger.warning(
            'Failed to send email message to %r, retrying.', ', '.join(recipient_list))
        self.retry(exc=exc, retry_countdown=60)
