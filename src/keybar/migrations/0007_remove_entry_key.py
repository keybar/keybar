# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0006_device_public_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='key',
        ),
    ]
