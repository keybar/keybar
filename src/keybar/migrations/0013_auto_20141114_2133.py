# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0012_entry_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='id',
        ),
        migrations.AlterField(
            model_name='entry',
            name='uuid',
            field=uuidfield.fields.UUIDField(max_length=32, serialize=False, unique=True, primary_key=True, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
