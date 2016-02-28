# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

import django.contrib.postgres.fields
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import keybar.models.user


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('name', models.TextField(max_length=100, null=True, verbose_name='Name', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status', help_text='Designates whether the user can log into this admin site.')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
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
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.TextField(default='', verbose_name='Device name', blank=True)),
                ('public_key', models.BinaryField(unique=True, verbose_name='Device Public Key')),
                ('authorized', models.NullBooleanField(default=None, verbose_name='Authorized?')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True, related_name='devices')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.TextField(default='', verbose_name='Title', blank=True)),
                ('url', models.URLField(default='', blank=True)),
                ('identifier', models.TextField(verbose_name='Identifier for login', help_text='Usually a username or email address')),
                ('value', models.BinaryField(verbose_name='The encrypted value for the entry.', help_text='Usually a password.')),
                ('description', models.TextField(default='', verbose_name='Description', blank=True)),
                ('tags', django.contrib.postgres.fields.ArrayField(size=None, base_field=models.TextField(blank=True), null=True, blank=True)),
                ('salt', models.BinaryField(null=True, blank=True)),
                ('keys', django.contrib.postgres.fields.JSONField(default={})),
                ('log', django.contrib.postgres.fields.JSONField(default={})),
                ('force_two_factor_authorization', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('slug', models.SlugField(unique=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrganizationMember',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('type', models.CharField(choices=[('member', 'Member'), ('admin', 'Admin'), ('owner', 'Owner')], max_length=64, default='member')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('organization', models.ForeignKey(to='keybar.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationMemberTeam',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('organization_member', models.ForeignKey(to='keybar.OrganizationMember')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('slug', models.SlugField()),
                ('name', models.CharField(max_length=64)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('organization', models.ForeignKey(to='keybar.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='TeamVault',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('team', models.ForeignKey(to='keybar.Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vault',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('slug', models.SlugField(null=True)),
                ('name', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('organization', models.ForeignKey(to='keybar.Organization')),
                ('teams', models.ManyToManyField(to='keybar.Team', through='keybar.TeamVault', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='teamvault',
            name='vault',
            field=models.ForeignKey(to='keybar.Vault'),
        ),
        migrations.AddField(
            model_name='organizationmemberteam',
            name='team',
            field=models.ForeignKey(to='keybar.Team'),
        ),
        migrations.AddField(
            model_name='organizationmember',
            name='teams',
            field=models.ManyToManyField(to='keybar.Team', through='keybar.OrganizationMemberTeam', blank=True),
        ),
        migrations.AddField(
            model_name='organizationmember',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='organization_members'),
        ),
        migrations.AddField(
            model_name='organization',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='organization_memberships', through='keybar.OrganizationMember'),
        ),
        migrations.AddField(
            model_name='organization',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='entry',
            name='vault',
            field=models.ForeignKey(to='keybar.Vault'),
        ),
        migrations.AlterUniqueTogether(
            name='vault',
            unique_together=set([('organization', 'slug')]),
        ),
        migrations.AlterUniqueTogether(
            name='team',
            unique_together=set([('organization', 'slug')]),
        ),
        migrations.AlterUniqueTogether(
            name='organizationmemberteam',
            unique_together=set([('team', 'organization_member')]),
        ),
        migrations.AlterUniqueTogether(
            name='organizationmember',
            unique_together=set([('organization', 'user'), ('organization', 'email')]),
        ),
    ]
