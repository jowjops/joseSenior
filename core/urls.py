from django.urls import path
from . import views
from .views import students_by_class


urlpatterns = [
    path('',views.home, name="home"),
    path('students/by-class/', students_by_class, name='students_by_class'),
    path('students/<int:pk>/increase_absence/', views.increase_absence, name='increase_absence'),
    path('students/<int:pk>/decrease_absence/', views.decrease_absence, name='decrease_absence'),
    path('students/<int:pk>/manage_absence/', views.manage_absence, name='manage_absence'),
    path('announcements/', views.announcement_list, name='announcement_list'),
]
