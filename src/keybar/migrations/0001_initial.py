# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuidfield.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('email', models.EmailField(verbose_name='Email', max_length=254, unique=True)),
                ('name', models.TextField(verbose_name='Name', max_length=100, null=True, blank=True)),
                ('is_active', models.BooleanField(verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('is_staff', models.BooleanField(verbose_name='staff status', help_text='Designates whether the user can log into this admin site.', default=False)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', uuidfield.fields.UUIDField(max_length=32, blank=True, unique=True, editable=False, serialize=False, primary_key=True)),
                ('name', models.TextField(verbose_name='Device name', blank=True, default='')),
                ('public_key', models.TextField(verbose_name='Device Public Key')),
                ('authorized', models.NullBooleanField(verbose_name='Authorized?', default=None)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='devices')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', uuidfield.fields.UUIDField(max_length=32, blank=True, unique=True, editable=False, serialize=False, primary_key=True)),
                ('title', models.TextField(verbose_name='Title', blank=True, default='')),
                ('url', models.URLField(blank=True, default='')),
                ('identifier', models.TextField(verbose_name='Identifier for login', help_text='Usually a username or email address')),
                ('value', models.BinaryField(verbose_name='The encrypted value for the entry.', help_text='Usually a password.')),
                ('description', models.TextField(verbose_name='Description', blank=True, default='')),
                ('salt', models.BinaryField(null=True, blank=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
