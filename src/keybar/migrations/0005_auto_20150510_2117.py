# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0004_remove_user_secret'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='user',
            field=models.ForeignKey(related_name='devices', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
