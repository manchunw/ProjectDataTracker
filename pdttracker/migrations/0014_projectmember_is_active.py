# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdttracker', '0013_auto_20151120_0249'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectmember',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
