# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0002_user_totp_secret'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='tags',
            field=djorm_pgarray.fields.TextArrayField(dbtype='text'),
            preserve_default=True,
        ),
    ]
