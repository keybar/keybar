import pytest

from keybar.api.serializers.registration import RegisterSerializer
from keybar.tests.factories.device import PUBLIC_KEY
from keybar.utils.crypto import serialize_public_key


@pytest.mark.django_db
class TestRegisterSerializer:

    def test_requires_email(self):
        serializer = RegisterSerializer(data={
            'password': 'supersafepassword',
            'public_key': serialize_public_key(PUBLIC_KEY)
        })

        assert not serializer.is_valid()
        assert serializer.errors == {'email': ['This field is required.']}

    def test_requires_password(self):
        serializer = RegisterSerializer(data={
            'email': 'foo@bar.com',
            'public_key': serialize_public_key(PUBLIC_KEY)
        })

        assert not serializer.is_valid()
        assert serializer.errors == {'password': ['This field is required.']}

    def test_requires_public_key(self):
        serializer = RegisterSerializer(data={
            'email': 'foo@bar.com',
            'password': 'supersafepassword',
        })

        assert not serializer.is_valid()
        assert serializer.errors == {'public_key': ['This field is required.']}

    def test_validates_password(self):
        serializer = RegisterSerializer(data={
            'password': 'short',
            'email': 'foo@bar.com',
            'public_key': serialize_public_key(PUBLIC_KEY)
        })

        assert not serializer.is_valid()

        # We're configuring to at least 10 characters.
        assert serializer.errors == {
            'password': [
                'This password is too short. It must contain at '
                'least 10 characters.'
            ]
        }

    def test_create(self):
        serializer = RegisterSerializer(data={
            'password': 'supersafepassword',
            'email': 'foo@bar.com',
            'public_key': serialize_public_key(PUBLIC_KEY),
        })

        assert serializer.is_valid()

        user = serializer.save()
        assert user.email == 'foo@bar.com'
        assert user.devices.count() == 1
        assert user.devices.first().fingerprint == 'e777 c552 5bab 7d95  58dc bb8d 6cd5 daf0'
