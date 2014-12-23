# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0004_auto_20141213_1841'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='created_by',
            new_name='owner',
        ),
    ]
