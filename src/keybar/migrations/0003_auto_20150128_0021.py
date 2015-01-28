# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0002_entry_keys'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='public_key',
            field=models.TextField(verbose_name='Device Public Key', unique=True),
            preserve_default=True,
        ),
    ]
