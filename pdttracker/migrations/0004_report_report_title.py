# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdttracker', '0003_auto_20151118_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='report_title',
            field=models.CharField(verbose_name='Report title', max_length=50, default='Report for testing'),
            preserve_default=False,
        ),
    ]
