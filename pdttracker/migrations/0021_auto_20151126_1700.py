# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdttracker', '0020_auto_20151125_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='timer',
            name='created_by',
            field=models.ForeignKey(to='pdttracker.ProjectMember', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='timer',
            name='timing_iteration',
            field=models.ForeignKey(to='pdttracker.Iteration', blank=True, null=True),
        ),
    ]
