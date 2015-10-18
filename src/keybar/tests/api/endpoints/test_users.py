import mock
import pytest

from keybar.models.device import Device
from keybar.tests.factories.device import PRIVATE_KEY, AuthorizedDeviceFactory, DeviceFactory
from keybar.tests.factories.user import UserFactory
from keybar.tests.helpers import LiveServerTest


@pytest.mark.django_db(transaction=True)
class TestUsersEndpoint(LiveServerTest):

    def _setup(self):
        user = UserFactory.create(email='test@none.none', is_superuser=True)
        device = AuthorizedDeviceFactory.create(user=user)
        self.client = self.get_client(device.id, PRIVATE_KEY)

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
        # Not using the fixture, ensure we're actually creating a new device here
        Device.objects.all().delete()

        device = DeviceFactory.create(user=None)
        assert not device.authorized

        client = self.get_client(device.id, PRIVATE_KEY)

        response = client.register_user('new-user@none.none', '123456')

        assert response.status_code == 200
        assert response.json() == {
            'date_joined': mock.ANY,
            'email': 'new-user@none.none',
            'id': mock.ANY
        }

        assert Device.objects.get(user__email='new-user@none.none').authorized
