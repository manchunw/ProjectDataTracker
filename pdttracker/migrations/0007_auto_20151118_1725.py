# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdttracker', '0006_actionlog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectmember',
            name='member',
        ),
        migrations.RemoveField(
            model_name='projectmember',
            name='work_in',
        ),
        migrations.RemoveField(
            model_name='actionlog',
            name='action_log_created_by',
        ),
        migrations.RemoveField(
            model_name='timer',
            name='timer_created_by',
        ),
        migrations.DeleteModel(
            name='ProjectMember',
        ),
    ]
