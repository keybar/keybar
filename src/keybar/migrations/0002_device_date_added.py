# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
