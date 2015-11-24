# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdttracker', '0015_auto_20151120_0334'),
    ]

    operations = [
        migrations.AddField(
            model_name='actionlogdescription',
            name='short_title',
            field=models.CharField(verbose_name='Action log short name', default='default', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='project_report',
            field=models.ForeignKey(to='pdttracker.Report', blank=True, null=True),
        ),
    ]
