# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import keybar.utils.db.json
import uuid
import keybar.models.user
from django.conf import settings
import django.utils.timezone
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, verbose_name='last login', null=True)),
                ('id', models.UUIDField(primary_key=True, serialize=False, default=uuid.uuid4)),
                ('email', models.EmailField(max_length=254, verbose_name='Email', unique=True)),
                ('name', models.TextField(max_length=100, blank=True, verbose_name='Name', null=True)),
                ('is_active', models.BooleanField(verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('is_staff', models.BooleanField(verbose_name='staff status', help_text='Designates whether the user can log into this admin site.', default=False)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('secret', models.BinaryField()),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', keybar.models.user.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, default=uuid.uuid4)),
                ('name', models.TextField(blank=True, verbose_name='Device name', default='')),
                ('public_key', models.TextField(verbose_name='Device Public Key', unique=True)),
                ('authorized', models.NullBooleanField(verbose_name='Authorized?', default=None)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='devices')),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, default=uuid.uuid4)),
                ('title', models.TextField(blank=True, verbose_name='Title', default='')),
                ('url', models.URLField(blank=True, default='')),
                ('identifier', models.TextField(verbose_name='Identifier for login', help_text='Usually a username or email address')),
                ('value', models.BinaryField(verbose_name='The encrypted value for the entry.', help_text='Usually a password.')),
                ('description', models.TextField(blank=True, verbose_name='Description', default='')),
                ('tags', django.contrib.postgres.fields.ArrayField(blank=True, size=None, base_field=models.TextField(blank=True), null=True)),
                ('salt', models.BinaryField(blank=True, null=True)),
                ('keys', keybar.utils.db.json.JSONField(default={})),
                ('log', keybar.utils.db.json.JSONField(default={})),
                ('force_two_factor_authorization', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
