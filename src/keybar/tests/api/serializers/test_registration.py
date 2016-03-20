import pytest

from keybar.api.serializers.registration import RegisterSerializer

@pytest.mark.django_db
class TestRegisterSerializer:

    def test_requires_email(self):
        serializer = RegisterSerializer(data={
            'password': 'supersafepassword',
        })

        assert not serializer.is_valid()
        assert serializer.errors == {'email': ['This field is required.']}

    def test_requires_password(self):
        serializer = RegisterSerializer(data={
            'email': 'foo@bar.com',
        })

        assert not serializer.is_valid()
        assert serializer.errors == {'password': ['This field is required.']}

    def test_validates_password(self):
        serializer = RegisterSerializer(data={
            'password': 'short',
            'email': 'foo@bar.com'
        })

        assert not serializer.is_valid()

        # We're configuring to at least 10 characters.
        assert serializer.errors == {
            'password': [
                'This password is too short. It must contain at '
                'least 10 characters.'
            ]
        }
