# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import keybar.utils.db.json


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0003_auto_20150515_0129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='value',
        ),
        migrations.AddField(
            model_name='entry',
            name='values',
            field=keybar.utils.db.json.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='entry',
            name='identifier',
            field=models.TextField(verbose_name='Identifier for login', blank=True, help_text='Usually a username or email address'),
        ),
    ]
