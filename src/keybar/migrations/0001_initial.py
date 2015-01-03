# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import keybar.utils.db.json
import djorm_pgarray.fields
import keybar.utils.db.uuid
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('id', keybar.utils.db.uuid.UUIDField(editable=False, max_length=32, unique=True, serialize=False, blank=True, primary_key=True)),
                ('email', models.EmailField(max_length=254, verbose_name='Email', unique=True)),
                ('name', models.TextField(null=True, max_length=100, verbose_name='Name', blank=True)),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', verbose_name='staff status', default=False)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('secret', models.BinaryField()),
            ],
            options={
                'verbose_name_plural': 'Users',
                'verbose_name': 'User',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', keybar.utils.db.uuid.UUIDField(editable=False, max_length=32, unique=True, serialize=False, blank=True, primary_key=True)),
                ('name', models.TextField(verbose_name='Device name', default='', blank=True)),
                ('public_key', models.TextField(verbose_name='Device Public Key')),
                ('authorized', models.NullBooleanField(verbose_name='Authorized?', default=None)),
                ('user', models.ForeignKey(related_name='devices', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', keybar.utils.db.uuid.UUIDField(editable=False, max_length=32, unique=True, serialize=False, blank=True, primary_key=True)),
                ('title', models.TextField(verbose_name='Title', default='', blank=True)),
                ('url', models.URLField(blank=True, default='')),
                ('identifier', models.TextField(help_text='Usually a username or email address', verbose_name='Identifier for login')),
                ('value', models.BinaryField(help_text='Usually a password.', verbose_name='The encrypted value for the entry.')),
                ('description', models.TextField(verbose_name='Description', default='', blank=True)),
                ('tags', djorm_pgarray.fields.TextArrayField(dbtype='text')),
                ('salt', models.BinaryField(null=True, blank=True)),
                ('force_two_factor_authorization', models.BooleanField(default=False)),
                ('log', keybar.utils.db.json.JSONField(default={})),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
