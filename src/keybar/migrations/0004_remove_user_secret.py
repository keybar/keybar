# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0003_auto_20150508_0901'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='secret',
        ),
    ]
