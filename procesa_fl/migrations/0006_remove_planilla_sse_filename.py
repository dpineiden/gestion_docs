# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('procesa_fl', '0005_auto_20150407_1248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planilla_sse',
            name='filename',
        ),
    ]
