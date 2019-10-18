# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-20 15:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0008_auto_20160320_0836'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vault',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='vault',
        ),
        migrations.AddField(
            model_name='entry',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Vault',
        ),
    ]