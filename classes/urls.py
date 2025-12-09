from django.urls import path,include
from . import views

urlpatterns = [
    
    path('classes_list/',views.class_list,name="class_list"),
    path('class_edit/<int:id>',views.class_edit,name="class_edit")

]