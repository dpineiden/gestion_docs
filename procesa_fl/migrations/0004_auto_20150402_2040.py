# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('procesa_fl', '0003_auto_20150401_1739'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planilla_sse',
            name='path',
        ),
        migrations.AddField(
            model_name='planilla_sse',
            name='file_sse',
            field=models.FileField(default=b'', upload_to=b'ss_files'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='planilla_sse',
            name='path_sse',
            field=models.CharField(default=b'', max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='planilla_sse',
            name='filename',
            field=models.CharField(max_length=30),
            preserve_default=True,
        ),
    ]
