# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdttracker', '0022_auto_20151126_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iteration',
            name='iteration_report',
            field=models.ForeignKey(null=True, blank=True, to='pdttracker.Report'),
        ),
        migrations.AlterField(
            model_name='phase',
            name='phase_report',
            field=models.ForeignKey(null=True, blank=True, to='pdttracker.Report'),
        ),
    ]
