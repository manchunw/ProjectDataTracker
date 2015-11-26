# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdttracker', '0021_auto_20151126_1700'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timer',
            old_name='created_by',
            new_name='timer_created_by',
        ),
        migrations.AddField(
            model_name='defect',
            name='defect_created_by',
            field=models.ForeignKey(null=True, blank=True, to='pdttracker.ProjectMember'),
        ),
    ]
