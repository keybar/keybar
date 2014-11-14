# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0011_auto_20141114_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='uuid',
            field=uuidfield.fields.UUIDField(unique=True, blank=True, max_length=32, editable=False, default=None),
            preserve_default=False,
        ),
    ]
