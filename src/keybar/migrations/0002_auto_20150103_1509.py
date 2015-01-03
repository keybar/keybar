# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import keybar.utils.db.uuid


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='id',
            field=keybar.utils.db.uuid.UUIDField(max_length=32, primary_key=True, blank=True, editable=False, unique=True, serialize=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='id',
            field=keybar.utils.db.uuid.UUIDField(max_length=32, primary_key=True, blank=True, editable=False, unique=True, serialize=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=keybar.utils.db.uuid.UUIDField(max_length=32, primary_key=True, blank=True, editable=False, unique=True, serialize=False),
            preserve_default=True,
        ),
    ]
