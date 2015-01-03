# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields
import keybar.utils.db.json
import django.core.serializers.json
import django.utils.timezone
import decimal
from django.conf import settings
import keybar.utils.db.uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('id', keybar.utils.db.uuid.UUIDField(serialize=False, max_length=32, editable=False, unique=True, blank=True, primary_key=True)),
                ('email', models.EmailField(verbose_name='Email', max_length=254, unique=True)),
                ('name', models.TextField(verbose_name='Name', max_length=100, blank=True, null=True)),
                ('is_active', models.BooleanField(verbose_name='active', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('is_staff', models.BooleanField(verbose_name='staff status', default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('secret', models.BinaryField()),
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
                ('id', keybar.utils.db.uuid.UUIDField(serialize=False, max_length=32, editable=False, unique=True, blank=True, primary_key=True)),
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
                ('id', keybar.utils.db.uuid.UUIDField(serialize=False, max_length=32, editable=False, unique=True, blank=True, primary_key=True)),
                ('title', models.TextField(verbose_name='Title', default='', blank=True)),
                ('url', models.URLField(default='', blank=True)),
                ('identifier', models.TextField(verbose_name='Identifier for login', help_text='Usually a username or email address')),
                ('value', models.BinaryField(verbose_name='The encrypted value for the entry.', help_text='Usually a password.')),
                ('description', models.TextField(verbose_name='Description', default='', blank=True)),
                ('tags', djorm_pgarray.fields.TextArrayField(dbtype='text')),
                ('salt', models.BinaryField(blank=True, null=True)),
                ('force_two_factor_authorization', models.BooleanField(default=False)),
                ('log', keybar.utils.db.json.JSONField(encode_kwargs={'cls': django.core.serializers.json.DjangoJSONEncoder}, default={}, decode_kwargs={'parse_float': decimal.Decimal})),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
