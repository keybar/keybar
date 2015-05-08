# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.UUIDField(serialize=False, default=uuid.uuid4, primary_key=True)),
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
                ('id', models.UUIDField(serialize=False, default=uuid.uuid4, primary_key=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('type', models.CharField(max_length=64, default='member', choices=[('member', 'Member'), ('admin', 'Admin'), ('owner', 'Owner')])),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('organization', models.ForeignKey(to='keybar.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationMemberTeam',
            fields=[
                ('id', models.UUIDField(serialize=False, default=uuid.uuid4, primary_key=True)),
                ('organization_member', models.ForeignKey(to='keybar.OrganizationMember')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.UUIDField(serialize=False, default=uuid.uuid4, primary_key=True)),
                ('slug', models.SlugField()),
                ('name', models.CharField(max_length=64)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('organization', models.ForeignKey(to='keybar.Organization')),
            ],
        ),
        migrations.AddField(
            model_name='organizationmemberteam',
            name='team',
            field=models.ForeignKey(to='keybar.Team'),
        ),
        migrations.AddField(
            model_name='organizationmember',
            name='teams',
            field=models.ManyToManyField(to='keybar.Team', blank=True, through='keybar.OrganizationMemberTeam'),
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
