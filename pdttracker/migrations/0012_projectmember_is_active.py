# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdttracker', '0011_project_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectmember',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
