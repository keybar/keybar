# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0004_auto_20151018_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(size=None, default=[], base_field=models.TextField(blank=True), blank=True),
        ),
    ]
