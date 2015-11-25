# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('pdttracker', '0019_auto_20151125_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actionlog',
            name='action_log_created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True),
        ),
    ]
