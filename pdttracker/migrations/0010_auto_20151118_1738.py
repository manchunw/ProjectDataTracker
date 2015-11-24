# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdttracker', '0009_auto_20151118_1737'),
    ]

    operations = [
        migrations.CreateModel(
            name='Defect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('defect_title', models.CharField(verbose_name='Defect title', max_length=50)),
                ('defect_type', models.CharField(verbose_name='Defect type', max_length=50)),
                ('defect_description', models.TextField(verbose_name='Defect description')),
                ('defect_remarks', models.TextField(verbose_name='Defect remarks')),
                ('iteration_injected', models.ForeignKey(blank=True, null=True, to='pdttracker.Iteration')),
                ('recorded_in', models.ForeignKey(blank=True, null=True, to='pdttracker.Project')),
            ],
        ),
        migrations.AddField(
            model_name='actionlog',
            name='defect_tracked',
            field=models.ForeignKey(blank=True, null=True, to='pdttracker.Defect'),
        ),
    ]
