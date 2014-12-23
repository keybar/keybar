# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields
import django.utils.timezone
import uuidfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('id', uuidfield.fields.UUIDField(max_length=32, serialize=False, unique=True, editable=False, primary_key=True, blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='Email', unique=True)),
                ('name', models.TextField(null=True, verbose_name='Name', blank=True, max_length=100)),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_staff', models.BooleanField(help_text='Designates whether the user can log into this admin site.', default=False, verbose_name='staff status')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
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
                ('id', uuidfield.fields.UUIDField(max_length=32, serialize=False, unique=True, editable=False, primary_key=True, blank=True)),
                ('name', models.TextField(default='', verbose_name='Device name', blank=True)),
                ('public_key', models.TextField(verbose_name='Device Public Key')),
                ('authorized', models.NullBooleanField(default=None, verbose_name='Authorized?')),
                ('user', models.ForeignKey(related_name='devices', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', uuidfield.fields.UUIDField(max_length=32, serialize=False, unique=True, editable=False, primary_key=True, blank=True)),
                ('title', models.TextField(default='', verbose_name='Title', blank=True)),
                ('url', models.URLField(default='', blank=True)),
                ('identifier', models.TextField(help_text='Usually a username or email address', verbose_name='Identifier for login')),
                ('value', models.BinaryField(help_text='Usually a password.', verbose_name='The encrypted value for the entry.')),
                ('description', models.TextField(default='', verbose_name='Description', blank=True)),
                ('tags', djorm_pgarray.fields.TextArrayField(dbtype='text')),
                ('salt', models.BinaryField(null=True, blank=True)),
                ('force_two_factor_authorization', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
