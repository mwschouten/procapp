# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hbtask',
            name='celery_id',
        ),
        migrations.AddField(
            model_name='hbtaskrun',
            name='celery_id',
            field=models.CharField(max_length=50, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='hbtask',
            name='status',
            field=models.IntegerField(default=0, choices=[(1, b'Done'), (0, b'Pending'), (2, b'Failed')]),
        ),
        migrations.AlterField(
            model_name='hbtask',
            name='submitted',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 10, 10, 33, 36, 417862)),
        ),
        migrations.AlterField(
            model_name='hbtaskrun',
            name='picked_up',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 10, 10, 33, 36, 418578)),
        ),
    ]
