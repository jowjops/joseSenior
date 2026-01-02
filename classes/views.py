from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Class
from django.shortcuts import get_object_or_404
from users.models import TeacherProfile
from users.models import StudentProfile
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponse

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

@login_required
def class_edit(request, id):
    selected_class = get_object_or_404(Class,id=id)
    students_count= StudentProfile.objects.filter(class_level=selected_class).count()
    if not request.user.is_superuser:
        return HttpResponse('Permission denied', status=403)
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        class_description = request.POST.get('class_description')
        selected_class.name = class_name
        selected_class.description = class_description
        if 'schedule_image' in request.FILES:
            selected_class.schedule_image = request.FILES['schedule_image']

        print(f"Updated class name to: {class_name}")
        selected_class.save()
        return redirect('class_edit', id=selected_class.id) 

    return render(request,'classes/class_edit.html',{'class':selected_class,'students_count':students_count})


@require_POST
def delete_class(request, class_id):
   
    class_to_delete = get_object_or_404(Class,id=class_id)

    if not request.user.is_superuser:
        return HttpResponse('Permission denied', status=403)
    class_to_delete.delete()

    return HttpResponse('deleted')

def class_readonly(request, id):
    selected_class = get_object_or_404(Class,id=id)
    students_count= StudentProfile.objects.filter(class_level=selected_class).count()
    return render(request,'classes/class_readonly.html',{'class':selected_class,'students_count':students_count})