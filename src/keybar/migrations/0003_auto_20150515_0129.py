# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0002_device_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='vault',
            field=models.ForeignKey(to='keybar.Vault', related_name='entries'),
        ),
        migrations.AlterField(
            model_name='vault',
            name='slug',
            field=models.SlugField(),
        ),
    ]
