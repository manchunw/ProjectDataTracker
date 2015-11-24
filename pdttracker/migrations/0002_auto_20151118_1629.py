# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdttracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iteration',
            name='iteration_name',
            field=models.CharField(max_length=50, verbose_name='Iteration name'),
        ),
        migrations.AlterField(
            model_name='phase',
            name='phase_name',
            field=models.CharField(max_length=50, verbose_name='Phase name'),
        ),
    ]
