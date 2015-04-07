# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('procesa_fl', '0002_auto_20150401_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('contact', models.CharField(max_length=100)),
                ('email_contact', models.EmailField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=10)),
                ('client', models.ForeignKey(to='procesa_fl.Cliente')),
            ],
            options={
                'ordering': ['code'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='planilla_sse',
            name='project',
            field=models.ForeignKey(default=1, to='procesa_fl.Proyecto'),
            preserve_default=True,
        ),
    ]
