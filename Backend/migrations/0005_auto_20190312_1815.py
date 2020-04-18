# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-12 18:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Backend', '0004_auto_20190312_1705'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='workers',
        ),
        migrations.AddField(
            model_name='book',
            name='photo',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='comment_book', to='Backend.Comment'),
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(blank=True, related_name='genre_books', to='Backend.Genre'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ManyToManyField(blank=True, related_name='comment_author', to='Backend.Person'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='book',
            field=models.ManyToManyField(blank=True, related_name='comment_book', to='Backend.Book'),
        ),
        migrations.AlterField(
            model_name='company',
            name='books',
            field=models.ManyToManyField(blank=True, related_name='company_books', to='Backend.Book'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='book',
            field=models.ManyToManyField(blank=True, related_name='genre_books', to='Backend.Book'),
        ),
        migrations.RemoveField(
            model_name='person',
            name='company',
        ),
        migrations.AddField(
            model_name='person',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Backend.Company'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='person',
            name='myBooks',
            field=models.ManyToManyField(blank=True, related_name='my_books', to='Backend.Book'),
        ),
        migrations.AlterField(
            model_name='person',
            name='readingBooks',
            field=models.ManyToManyField(blank=True, related_name='reading_books', to='Backend.Book'),
        ),
    ]
