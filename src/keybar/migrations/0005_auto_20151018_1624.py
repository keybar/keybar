# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


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
