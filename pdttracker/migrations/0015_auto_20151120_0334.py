# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdttracker', '0014_projectmember_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='num_iteration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='num_phase',
            field=models.IntegerField(default=0),
        ),
    ]
