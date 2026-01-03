from django.contrib import admin
from . models import Class
from .models import ClassAnnouncement
# Register your models here.

admin.site.register(Class)
admin.site.register(ClassAnnouncement)