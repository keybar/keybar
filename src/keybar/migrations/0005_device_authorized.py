# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0004_remove_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='authorized',
            field=models.NullBooleanField(verbose_name='Authorized?', default=None),
            preserve_default=True,
        ),
    ]
