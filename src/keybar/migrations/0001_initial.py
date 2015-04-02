# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields
import django.utils.timezone
import keybar.models.user
import keybar.utils.db.json
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='Email')),
                ('name', models.TextField(max_length=100, null=True, blank=True, verbose_name='Name')),
                ('is_active', models.BooleanField(verbose_name='active', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_staff', models.BooleanField(verbose_name='staff status', default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('secret', models.BinaryField()),
            ],
            options={
                'verbose_name_plural': 'Users',
                'verbose_name': 'User',
            },
            managers=[
                ('objects', keybar.models.user.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.TextField(default='', blank=True, verbose_name='Device name')),
                ('public_key', models.TextField(unique=True, verbose_name='Device Public Key')),
                ('authorized', models.NullBooleanField(default=None, verbose_name='Authorized?')),
                ('user', models.ForeignKey(related_name='devices', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.TextField(default='', blank=True, verbose_name='Title')),
                ('url', models.URLField(default='', blank=True)),
                ('identifier', models.TextField(verbose_name='Identifier for login', help_text='Usually a username or email address')),
                ('value', models.BinaryField(verbose_name='The encrypted value for the entry.', help_text='Usually a password.')),
                ('description', models.TextField(default='', blank=True, verbose_name='Description')),
                ('tags', djorm_pgarray.fields.TextArrayField(dbtype='text')),
                ('salt', models.BinaryField(null=True, blank=True)),
                ('keys', keybar.utils.db.json.JSONField(default={})),
                ('log', keybar.utils.db.json.JSONField(default={})),
                ('force_two_factor_authorization', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
