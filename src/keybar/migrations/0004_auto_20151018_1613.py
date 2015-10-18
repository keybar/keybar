# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keybar', '0003_auto_20150515_0129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='members',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='owner',
        ),
        migrations.AlterUniqueTogether(
            name='organizationmember',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='organizationmember',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='organizationmember',
            name='teams',
        ),
        migrations.RemoveField(
            model_name='organizationmember',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='organizationmemberteam',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='organizationmemberteam',
            name='organization_member',
        ),
        migrations.RemoveField(
            model_name='organizationmemberteam',
            name='team',
        ),
        migrations.AlterUniqueTogether(
            name='team',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='team',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='teamvault',
            name='team',
        ),
        migrations.RemoveField(
            model_name='teamvault',
            name='vault',
        ),
        migrations.AddField(
            model_name='vault',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=None),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='vault',
            unique_together=set([]),
        ),
        migrations.DeleteModel(
            name='OrganizationMember',
        ),
        migrations.DeleteModel(
            name='OrganizationMemberTeam',
        ),
        migrations.RemoveField(
            model_name='vault',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='vault',
            name='teams',
        ),
        migrations.DeleteModel(
            name='Organization',
        ),
        migrations.DeleteModel(
            name='Team',
        ),
        migrations.DeleteModel(
            name='TeamVault',
        ),
    ]
