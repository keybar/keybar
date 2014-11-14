# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0008_entry_salt'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='created_by',
            field=models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
