# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0002_auto_20141001_2107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='api_key',
        ),
        migrations.AlterField(
            model_name='device',
            name='user',
            field=models.ForeignKey(related_name='devices', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='value',
            field=models.TextField(verbose_name='The encrypted value for the entry.', help_text='Usually a password.'),
            preserve_default=True,
        ),
    ]
