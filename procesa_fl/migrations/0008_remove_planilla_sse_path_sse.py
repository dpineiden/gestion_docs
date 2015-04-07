# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('procesa_fl', '0007_auto_20150407_1444'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planilla_sse',
            name='path_sse',
        ),
    ]
