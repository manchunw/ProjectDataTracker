# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdttracker', '0008_auto_20151118_1730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='defect',
            name='iteration_injected',
        ),
        migrations.RemoveField(
            model_name='defect',
            name='recorded_in',
        ),
        migrations.RemoveField(
            model_name='actionlog',
            name='defect_tracked',
        ),
        migrations.DeleteModel(
            name='Defect',
        ),
    ]
