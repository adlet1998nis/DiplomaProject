# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    password = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    position = models.CharField(max_length=100, blank=True)

    token = models.CharField(max_length=255)
    photo = models.CharField(max_length=1000, blank=True)

    read = models.ManyToManyField('Book', blank=True)

    def __str__(self):
        return self.phone


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Comment(models.Model):
    text = models.CharField(max_length=100)
    author = models.ForeignKey(Person, related_name='comment_author', blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

class Book(models.Model):
    name = models.CharField(max_length=100)
    isbn = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.CharField(max_length=100000)
    photo = models.CharField(max_length=1000)

    rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)
    genre = models.ManyToManyField('Genre', related_name='genre_books', blank=True)
    comments = models.ManyToManyField('Comment', related_name='comment_book', blank=True)

    company_book = models.BooleanField(default=False)
    belong = models.ForeignKey('Person', related_name='belong', on_delete=models.CASCADE, null=True, blank=True)
    reader = models.ForeignKey('Person', related_name='reader', on_delete=models.CASCADE, null=True, blank=True)
    requesters = models.ManyToManyField('Person', related_name='requesters', blank=True)

    history = models.ManyToManyField('Person', related_name='history', blank=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    text = models.CharField(max_length=1000)
    author = models.ForeignKey(Person, related_name='author', blank=False)
    recipient = models.ForeignKey(Person, related_name='recipient', blank=False)
    sended_time = models.DateTimeField(default=timezone.now)
    status = models.IntegerField(default=0)
    book = models.ForeignKey('Book', related_name='message_book')

    def __str__(self):
        return self.author.name + " " + self.recipient.name


class Community(models.Model):
    author = models.ForeignKey('Person', related_name='community_person')
    book = models.ForeignKey('Book', related_name='community_book')
