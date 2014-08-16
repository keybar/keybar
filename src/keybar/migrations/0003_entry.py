# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0002_auto_20140802_2203'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(blank=True, default='', max_length=256)),
                ('description', models.TextField(blank=True)),
                ('username', models.CharField(max_length=256)),
                ('value', models.TextField()),
                ('key', models.BinaryField(editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
