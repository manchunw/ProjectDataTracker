# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdttracker', '0005_auto_20151118_1719'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionLog',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('action_log_created_by', models.ForeignKey(to='pdttracker.ProjectMember')),
                ('action_log_description', models.ForeignKey(to='pdttracker.ActionLogDescription')),
                ('defect_tracked', models.ForeignKey(to='pdttracker.Defect', null=True, blank=True)),
                ('iteration_tracked', models.ForeignKey(to='pdttracker.Iteration', null=True, blank=True)),
                ('phase_tracked', models.ForeignKey(to='pdttracker.Phase', null=True, blank=True)),
                ('project_tracked', models.ForeignKey(to='pdttracker.Project', null=True, blank=True)),
            ],
        ),
    ]
