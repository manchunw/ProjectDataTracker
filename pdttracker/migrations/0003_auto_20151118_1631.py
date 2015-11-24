# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdttracker', '0002_auto_20151118_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_title',
            field=models.CharField(max_length=50, verbose_name='Project title'),
        ),
    ]
