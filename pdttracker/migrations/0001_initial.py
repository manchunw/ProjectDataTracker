# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ActionLogDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50, verbose_name='Action log description title')),
            ],
        ),
        migrations.CreateModel(
            name='Defect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('defect_title', models.CharField(max_length=50, verbose_name='Defect title')),
                ('defect_type', models.CharField(max_length=50, verbose_name='Defect type')),
                ('defect_description', models.TextField(verbose_name='Defect description')),
                ('defect_remarks', models.TextField(verbose_name='Defect remarks')),
            ],
        ),
        migrations.CreateModel(
            name='Iteration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iteration_name', models.CharField(max_length=50, verbose_name='name')),
                ('iteration_sequence', models.IntegerField(default=0)),
                ('iteration_sloc', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phase_name', models.CharField(max_length=50, verbose_name='name')),
                ('phase_sequence', models.IntegerField(default=0)),
                ('phase_sloc', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_title', models.CharField(max_length=50, verbose_name='Title')),
                ('project_description', models.TextField(verbose_name='Description')),
                ('project_sloc', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('current_iteration', models.ForeignKey(null=True, to='pdttracker.Iteration', blank=True)),
                ('current_phase', models.ForeignKey(null=True, to='pdttracker.Phase', blank=True)),
                ('in_charge_by', models.ForeignKey(related_name='in_charge_of', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('member', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('work_in', models.ForeignKey(to='pdttracker.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('defects_injected', models.IntegerField(default=0)),
                ('defects_removed', models.IntegerField(default=0)),
                ('delivered_sloc', models.IntegerField(default=0)),
                ('delivered_sloc_of_project', models.FloatField(default=0)),
                ('person_mths', models.IntegerField(default=0)),
                ('person_mths_of_project', models.FloatField(default=0)),
                ('delivered_sloc_per_person_mths', models.FloatField(default=0)),
                ('injection_rate_per_person_hrs', models.FloatField(default=0)),
                ('person_hrs', models.IntegerField(default=0)),
                ('defect_density_per_ksloc', models.FloatField(default=0)),
                ('yield_value', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Timer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('timer_created_by', models.ForeignKey(to='pdttracker.ProjectMember')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='project_report',
            field=models.ForeignKey(to='pdttracker.Report'),
        ),
        migrations.AddField(
            model_name='phase',
            name='in_project',
            field=models.ForeignKey(to='pdttracker.Project'),
        ),
        migrations.AddField(
            model_name='phase',
            name='phase_report',
            field=models.ForeignKey(to='pdttracker.Report'),
        ),
        migrations.AddField(
            model_name='iteration',
            name='in_phase',
            field=models.ForeignKey(to='pdttracker.Phase'),
        ),
        migrations.AddField(
            model_name='iteration',
            name='iteration_report',
            field=models.ForeignKey(to='pdttracker.Report'),
        ),
        migrations.AddField(
            model_name='defect',
            name='iteration_injected',
            field=models.ForeignKey(null=True, to='pdttracker.Iteration', blank=True),
        ),
        migrations.AddField(
            model_name='defect',
            name='recorded_in',
            field=models.ForeignKey(null=True, to='pdttracker.Project', blank=True),
        ),
        migrations.AddField(
            model_name='actionlog',
            name='action_log_created_by',
            field=models.ForeignKey(to='pdttracker.ProjectMember'),
        ),
        migrations.AddField(
            model_name='actionlog',
            name='action_log_description',
            field=models.ForeignKey(to='pdttracker.ActionLogDescription'),
        ),
        migrations.AddField(
            model_name='actionlog',
            name='defect_tracked',
            field=models.ForeignKey(null=True, to='pdttracker.Defect', blank=True),
        ),
        migrations.AddField(
            model_name='actionlog',
            name='iteration_tracked',
            field=models.ForeignKey(null=True, to='pdttracker.Iteration', blank=True),
        ),
        migrations.AddField(
            model_name='actionlog',
            name='phase_tracked',
            field=models.ForeignKey(null=True, to='pdttracker.Phase', blank=True),
        ),
        migrations.AddField(
            model_name='actionlog',
            name='project_tracked',
            field=models.ForeignKey(null=True, to='pdttracker.Project', blank=True),
        ),
    ]
