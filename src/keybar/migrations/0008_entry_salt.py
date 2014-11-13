# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0007_remove_entry_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='salt',
            field=models.BinaryField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
