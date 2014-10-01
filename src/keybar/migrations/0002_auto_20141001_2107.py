# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', uuidfield.fields.UUIDField(unique=True, blank=True, primary_key=True, editable=False, serialize=False, max_length=32)),
                ('name', models.TextField(verbose_name='Device name', blank=True, default='')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='entry',
            name='username',
        ),
        migrations.AddField(
            model_name='entry',
            name='identifier',
            field=models.TextField(default=None, help_text='Usually a username or email address', verbose_name='Identifier for login'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='entry',
            name='description',
            field=models.TextField(verbose_name='Description', blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='entry',
            name='title',
            field=models.TextField(verbose_name='Title', blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='entry',
            name='value',
            field=models.TextField(help_text='Usually a password.', verbose_name='The value for the entry.'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.TextField(null=True, verbose_name='Name', blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.TextField(null=True, unique=True, verbose_name='Username', max_length=50),
        ),
    ]
