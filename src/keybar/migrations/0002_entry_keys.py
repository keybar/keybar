# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import keybar.utils.db.json


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='keys',
            field=keybar.utils.db.json.JSONField(default={}),
            preserve_default=True,
        ),
    ]
