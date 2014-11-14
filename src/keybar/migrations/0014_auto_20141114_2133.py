# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0013_auto_20141114_2133'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='uuid',
            new_name='id',
        ),
    ]
