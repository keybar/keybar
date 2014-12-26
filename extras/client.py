import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'keybar.settings')

import django
django.setup()

from keybar.client import Client
from keybar.models.user import User

secret = open('extras/example_keys/id_rsa', 'rb').read()
user = User.objects.get(email='admin@admin.admin')
device_id = user.devices.all().first().id.hex

client = Client(device_id, secret)

response = client.get('//keybar.local:8443/api/v1/users/')

print(response.content)
