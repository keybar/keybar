# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0003_entry_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='totp_secret',
            new_name='secret',
        ),
        migrations.AlterField(
            model_name='entry',
            name='tags',
            field=djorm_pgarray.fields.TextArrayField(dbtype='text', null=False),
            preserve_default=True,
        ),
    ]
