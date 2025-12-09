from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Class
from django.shortcuts import get_object_or_404
from users.models import TeacherProfile
from users.models import StudentProfile

@login_required

def class_list(request):
    classes = Class.objects.all().order_by('name')
    teacher_count = TeacherProfile.objects.all().count()
    student_count = StudentProfile.objects.all().count()
    
    context = {
        'classes': classes,
        'count': classes.count(),
        'teacher_count':teacher_count,
        'student_count':student_count,
    }

    return render(request, 'classes/class_list.html', context)

def class_edit(request, id):
    selected_class = get_object_or_404(Class,id=id)
    students_count= StudentProfile.objects.filter(class_level=selected_class).count()
    return render(request,'classes/class_edit.html',{'class':selected_class,'students_count':students_count})