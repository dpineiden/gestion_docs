# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('procesa_fl', '0006_remove_planilla_sse_filename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planilla_sse',
            name='file_sse',
            field=models.FileField(default=b'', upload_to=b'procesa_fl/sse_files'),
        ),
    ]
