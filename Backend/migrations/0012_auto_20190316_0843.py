# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-16 08:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0011_auto_20190316_0653'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='position',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='message',
            name='sended_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 16, 8, 43, 31, 350651, tzinfo=utc)),
        ),
    ]
