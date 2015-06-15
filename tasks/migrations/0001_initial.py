# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HBTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('celery_taskname', models.CharField(max_length=100)),
                ('parameters', models.TextField(null=True, blank=True)),
                ('resulthash', models.CharField(max_length=32, null=True, blank=True)),
                ('status', models.IntegerField(default=2, choices=[(1, b'Done'), (2, b'Pending'), (3, b'Failed')])),
                ('celery_id', models.CharField(max_length=50, unique=True, null=True, blank=True)),
                ('submitted', models.DateTimeField(default=datetime.datetime(2015, 6, 8, 19, 24, 30, 617245))),
            ],
        ),
        migrations.CreateModel(
            name='HBTaskRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picked_up', models.DateTimeField(default=datetime.datetime(2015, 6, 8, 19, 24, 30, 618177))),
                ('error', models.TextField(blank=True)),
                ('done', models.BooleanField(default=False)),
                ('task', models.ForeignKey(to='tasks.HBTask')),
            ],
        ),
    ]
