# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdttracker', '0018_auto_20151124_1740'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='person_hrs',
        ),
        migrations.RemoveField(
            model_name='timer',
            name='time',
        ),
        migrations.RemoveField(
            model_name='timer',
            name='timer_created_by',
        ),
        migrations.AddField(
            model_name='report',
            name='person_hrs_defectmode',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='person_hrs_devmode',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='person_hrs_mgmtmode',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='report',
            name='removal_rate_per_person_hrs',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='timer',
            name='created_for',
            field=models.ForeignKey(null=True, to='pdttracker.Project', blank=True),
        ),
        migrations.AddField(
            model_name='timer',
            name='mode',
            field=models.CharField(default='devmode', max_length=10),
        ),
        migrations.AddField(
            model_name='timer',
            name='num_hrs',
            field=models.FloatField(default=0),
        ),
    ]
