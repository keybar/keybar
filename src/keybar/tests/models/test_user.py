import pytest
import mock
from django.core import mail

from keybar.models.user import User
from keybar.tests.factories.user import UserFactory


@pytest.mark.django_db
class TestUserModel:

    def setup(self):
        self.user = UserFactory.create()

    def test_send_email(self):
        self.user.send_mail('subject', 'message')

        assert len(mail.outbox) == 1
        message = mail.outbox[0]

        assert message.subject == 'subject'
        assert message.to == [self.user.email]
        assert message.body == 'message'

    @mock.patch('keybar.models.user.send_mail_async.delay')
    def test_send_mail_called_async(self, send_mail_async):
        self.user.send_mail('subject', 'message')
        send_mail_async.assert_called_once_with('subject', 'message',
            mock.ANY, [self.user.email])

    @mock.patch('keybar.tasks.mail.django_send_mail')
    @mock.patch('keybar.models.user.send_mail_async.retry')
    def test_send_mail_retried_on_error(self, retry, django_send_mail):
        django_send_mail.side_effect = Exception()
        self.user.send_mail('subject', 'message')
        retry.assert_called_once_with(retry_countdown=60, exc=mock.ANY)

    def test_short_name(self):
        assert self.user.get_short_name() == self.user.email

    def test_check_password(self):
        user = User()
        user.set_password('test')
        assert user.check_password('test')

    def test_check_password_unicode(self):
        user = User()
        user.set_password(u'winter is coming ☃❄')
        assert user.check_password(u'winter is coming ☃❄')
