# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0004_auto_20150904_1038'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='force_two_factor_authorization',
            new_name='enable_two_factor_authorization',
        ),
    ]
