# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdttracker', '0016_auto_20151124_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='yield_percentage',
            field=models.FloatField(default=0.8),
        ),
    ]
