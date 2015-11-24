# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdttracker', '0004_report_report_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actionlog',
            name='action_log_created_by',
        ),
        migrations.RemoveField(
            model_name='actionlog',
            name='action_log_description',
        ),
        migrations.RemoveField(
            model_name='actionlog',
            name='defect_tracked',
        ),
        migrations.RemoveField(
            model_name='actionlog',
            name='iteration_tracked',
        ),
        migrations.RemoveField(
            model_name='actionlog',
            name='phase_tracked',
        ),
        migrations.RemoveField(
            model_name='actionlog',
            name='project_tracked',
        ),
        migrations.DeleteModel(
            name='ActionLog',
        ),
    ]
