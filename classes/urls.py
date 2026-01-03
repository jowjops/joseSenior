from django.urls import path,include
from . import views

urlpatterns = [
    
    path('classes_list/',views.class_list,name="class_list"),
    path('class_edit/<int:id>',views.class_edit,name="class_edit"),
    path('delete_class/<int:class_id>/',views.delete_class,name="delete_class"),
    path('class_readonly/<int:id>',views.class_readonly,name="class_readonly"),
    
    path('class_announcements_add/',views.class_announcements_add,name="class_announcements_add"),

    path('announcements/', views.announcements_list, name='class_announcements_list'),
    path('announcements/delete/<int:pk>/',views.delete_announcement_direct,name='delete_announcement_direct'),
    ]