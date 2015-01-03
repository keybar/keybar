# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import decimal
import django.core.serializers.json
import keybar.utils.db.json


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0003_entry_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='log',
            field=keybar.utils.db.json.JSONField(decode_kwargs={'parse_float': decimal.Decimal}, encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}, blank=True),
            preserve_default=True,
        ),
    ]
