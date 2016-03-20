import mock
import pytest
from django.core.urlresolvers import reverse

from keybar.models.user import User
from keybar.models.device import Device
from keybar.utils.test import APIClient
from keybar.utils.crypto import serialize_public_key
from keybar.tests.factories.device import PUBLIC_KEY


@pytest.mark.django_db
class TestRegistration:

    def test_simple_register(self):
        url = reverse('api:register')

        response = APIClient().post(url, data={
            'email': 'test@example.com',
            'password': 'test123456',
            'public_key': serialize_public_key(PUBLIC_KEY)
        })

        assert response.status_code == 201
        assert response.json() == {
            'email': 'test@example.com',
            'device_id': mock.ANY
        }
        assert User.objects.filter(email='test@example.com').exists()

    def test_register_invalid_password(self):
        url = reverse('api:register')

        response = APIClient().post(url, data={
            'email': 'test@example.com',
            'password': '1234',
            'public_key': serialize_public_key(PUBLIC_KEY)
        })

        assert response.status_code == 400
        assert response.json() == {
            'password': [
                'This password is too short. It must contain at least 10 characters.',
                'This password is too common.',
                'This password is entirely numeric.'
            ]
        }

        # Make sure we never created a user or device
        assert User.objects.all().count() == 0
        assert Device.objects.all().count() == 0

    def test_register_invalid_email(self):
        url = reverse('api:register')

        response = APIClient().post(url, data={
            'email': 'test',
            'password': 'test123456',
            'public_key': serialize_public_key(PUBLIC_KEY)
        })

        assert response.status_code == 400
        assert response.json() == {
            'email': ['Enter a valid email address.']
        }

        assert User.objects.all().count() == 0
        assert Device.objects.all().count() == 0

    def test_register_invalid_public_key(self):
        url = reverse('api:register')

        response = APIClient().post(url, data={
            'email': 'test@test.test',
            'password': 'test123456',
            'public_key': 'invalid'
        })

        assert response.status_code == 400
        assert response.json() == {
            'public_key': ['Invalid public key']
        }

        assert User.objects.all().count() == 0
        assert Device.objects.all().count() == 0

    def test_register_invalid_email_unique(self):
        url = reverse('api:register')

        User.objects.create(email='test@test.test')
        response = APIClient().post(url, data={
            'email': 'test@test.test',
            'password': 'test123456',
            'public_key': serialize_public_key(PUBLIC_KEY)
        })

        assert response.status_code == 400
        assert response.json() == {
            'email': ['User with this Email already exists.']
        }
