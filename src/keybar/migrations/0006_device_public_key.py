# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0005_device_authorized'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='public_key',
            field=models.TextField(default='', verbose_name='Device Public Key'),
            preserve_default=False,
        ),
    ]
