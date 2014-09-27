import pytest


@pytest.mark.django_db
class TestIndexView(object):

    def test_index(self, client):
        response = client.get('/')
        assert response.template_name == ['keybar/web/index.html']
