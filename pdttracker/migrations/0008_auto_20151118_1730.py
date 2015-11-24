# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pdttracker', '0007_auto_20151118_1725'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('member', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('work_in', models.ForeignKey(null=True, to='pdttracker.Project', blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='actionlog',
            name='action_log_description',
            field=models.ForeignKey(null=True, to='pdttracker.ActionLogDescription', blank=True),
        ),
        migrations.AddField(
            model_name='actionlog',
            name='action_log_created_by',
            field=models.ForeignKey(null=True, to='pdttracker.ProjectMember', blank=True),
        ),
        migrations.AddField(
            model_name='timer',
            name='timer_created_by',
            field=models.ForeignKey(null=True, to='pdttracker.ProjectMember', blank=True),
        ),
    ]
