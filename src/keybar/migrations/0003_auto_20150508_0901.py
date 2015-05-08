# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0002_auto_20150508_0747'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamVault',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, default=uuid.uuid4)),
                ('team', models.ForeignKey(to='keybar.Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vault',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, default=uuid.uuid4)),
                ('slug', models.SlugField(null=True)),
                ('name', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('organization', models.ForeignKey(to='keybar.Organization')),
                ('teams', models.ManyToManyField(blank=True, through='keybar.TeamVault', to='keybar.Team')),
            ],
        ),
        migrations.RemoveField(
            model_name='entry',
            name='owner',
        ),
        migrations.AddField(
            model_name='teamvault',
            name='vault',
            field=models.ForeignKey(to='keybar.Vault'),
        ),
        migrations.AddField(
            model_name='entry',
            name='vault',
            field=models.ForeignKey(to='keybar.Vault', default=None),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='vault',
            unique_together=set([('organization', 'slug')]),
        ),
    ]
