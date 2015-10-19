# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0005_auto_20150904_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='public_key',
            field=models.TextField(unique=True, verbose_name='Device Public Key'),
        ),
    ]
