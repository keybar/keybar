# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import decimal
import keybar.utils.db.json
import django.core.serializers.json


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0002_auto_20150103_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='log',
            field=keybar.utils.db.json.JSONField(default={}, encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}, decode_kwargs={'parse_float': decimal.Decimal}),
            preserve_default=True,
        ),
    ]
