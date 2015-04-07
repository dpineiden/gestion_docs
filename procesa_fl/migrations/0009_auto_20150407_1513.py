# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('procesa_fl', '0008_remove_planilla_sse_path_sse'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='planilla_sse',
            options={'ordering': ['file_sse', 'upload_date', 'project', 'user_key']},
        ),
        migrations.AlterField(
            model_name='planilla_sse',
            name='upload_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
