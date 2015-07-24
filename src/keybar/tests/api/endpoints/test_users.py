import mock
import pytest

from keybar.client import Client
from keybar.models.device import Device
from keybar.tests.factories.device import PRIVATE_KEY, AuthorizedDeviceFactory, DeviceFactory
from keybar.tests.factories.user import UserFactory


@pytest.mark.django_db(transaction=True)
class TestUsersEndpoint:

    def setup(self):
        user = UserFactory.create(email='test@none.none', is_superuser=True)
        device = AuthorizedDeviceFactory.create(user=user)
        self.client = Client(device.id, PRIVATE_KEY)

    def test_list(self, keybar_liveserver):
        endpoint = '{0}/api/users/'.format(keybar_liveserver.url)

        response = self.client.get(endpoint)

        assert response.status_code == 200
        assert response.json() == [{
            'date_joined': mock.ANY,
            'email': 'test@none.none',
            'id': mock.ANY
        }]

    def test_register(self, keybar_liveserver):
        # Not using the fixture.
        Device.objects.all().delete()

        device = DeviceFactory.create(user=None)
        self.client = Client(device.id, PRIVATE_KEY)

        endpoint = '{0}/api/users/register/'.format(keybar_liveserver.url)

        assert not device.authorized

        response = self.client.post(endpoint, data={
            'email': 'new-user@none.none',
            'password1': '123456'
        })

        assert response.status_code == 200
        assert response.json() == {
            'date_joined': mock.ANY,
            'email': 'new-user@none.none',
            'id': mock.ANY
        }

        assert Device.objects.get(user__email='new-user@none.none').authorized
