# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-16 15:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0017_auto_20190316_1403'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='book',
        ),
    ]
