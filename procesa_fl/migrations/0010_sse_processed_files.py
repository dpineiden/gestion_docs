# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('procesa_fl', '0009_auto_20150407_1513'),
    ]

    operations = [
        migrations.CreateModel(
            name='SSE_Processed_Files',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('folder', models.CharField(max_length=50)),
                ('processed_files', models.FilePathField(max_length=500, recursive=True)),
                ('save_date', models.DateTimeField(auto_now=True)),
                ('planilla', models.ForeignKey(default=1, to='procesa_fl.Planilla_SSE')),
            ],
            options={
                'ordering': ['planilla', 'processed_files', 'save_date'],
            },
        ),
    ]
