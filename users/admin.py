from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserType, StudentProfile, TeacherProfile

admin.site.register(UserType)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
