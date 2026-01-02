from django.contrib import admin
from .models import Announcement
from .models import LatestNews

admin.site.register(LatestNews)
admin.site.register(Announcement)