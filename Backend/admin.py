# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Person)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(Book)
admin.site.register(Community)
admin.site.register(Message)