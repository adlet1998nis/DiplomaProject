# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-16 20:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0022_auto_20190316_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='requesters',
            field=models.ManyToManyField(blank=True, related_name='requesters', to='Backend.Person'),
        ),
    ]
