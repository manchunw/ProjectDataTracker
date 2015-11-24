# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdttracker', '0017_project_yield_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timer',
            name='time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
