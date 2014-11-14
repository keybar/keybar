# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0010_auto_20141114_1455'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='username',
            new_name='identifier',
        ),
        migrations.RenameField(
            model_name='entry',
            old_name='password',
            new_name='value',
        ),
    ]
