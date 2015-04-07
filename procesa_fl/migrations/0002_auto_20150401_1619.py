# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('procesa_fl', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='planilla_sse',
            options={'ordering': ['-upload_date']},
        ),
        migrations.AlterField(
            model_name='planilla_sse',
            name='upload_date',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
