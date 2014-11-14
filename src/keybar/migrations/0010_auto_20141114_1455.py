# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0009_entry_created_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='identifier',
            new_name='username'
        ),
        migrations.RenameField(
            model_name='entry',
            old_name='value',
            new_name='password'
        ),
        migrations.AddField(
            model_name='entry',
            name='url',
            field=models.URLField(blank=True, default=''),
            preserve_default=True,
        ),
    ]
