# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdttracker', '0012_projectmember_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectmember',
            name='is_active',
        ),
        migrations.AddField(
            model_name='defect',
            name='iteration_resolved',
            field=models.ForeignKey(null=True, to='pdttracker.Iteration', related_name='iteration_resolved', blank=True),
        ),
        migrations.AlterField(
            model_name='defect',
            name='iteration_injected',
            field=models.ForeignKey(null=True, to='pdttracker.Iteration', related_name='iteration_injected', blank=True),
        ),
    ]
