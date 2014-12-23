# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0005_auto_20141223_0424'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='force_two_factor_authorization',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
