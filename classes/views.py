from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Class
from django.shortcuts import get_object_or_404
from users.models import TeacherProfile
from users.models import StudentProfile
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages



@login_required

def class_list(request):
    classes = Class.objects.all().order_by('name')
    teacher_count = TeacherProfile.objects.all().count()
    student_count = StudentProfile.objects.all().count()
    user = request.user

    if hasattr(user, 'studentprofile_profile'):
            return redirect('home')
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




from django.db import transaction
from django.contrib import messages
from .models import ClassAnnouncement
import json

def class_announcements_add(request):
    user = request.user
    
    if hasattr(user, 'studentprofile_profile'):
        return redirect('home')
    
    if request.method == 'POST':
        try:
            data = request.POST
            
            with transaction.atomic():
                announcement = ClassAnnouncement.objects.create(
                    class_related_id=data.get('class_related'),
                    title=data.get('title'),
                    content=data.get('content'),
                    subject=data.get('subject')
                )
            
            messages.success(request, 'Announcement created successfully!')
            return redirect('home')  # Change this to your actual list view
            
        except Exception as e:
            messages.error(request, f'Error creating announcement: {str(e)}')
            # Re-render form with existing data
            classes = Class.objects.all()
            return render(request, 'classes/class_announcements_add.html', {
                'classes': classes,
                'form_data': request.POST,
                'SUBJECTS_CHOICES': ClassAnnouncement.SUBJECTS_CHOICES
            })
    
    # GET request - show empty form
    classes = Class.objects.all()
    return render(request, 'classes/class_announcements_add.html', {
        'classes': classes,
        'SUBJECTS_CHOICES': ClassAnnouncement.SUBJECTS_CHOICES
    })

def announcements_list(request):
    user = request.user
    has_student_profile = hasattr(user, 'studentprofile_profile')
    
    if has_student_profile:
        student_profile = StudentProfile.objects.get(user=user)
        announcements = ClassAnnouncement.objects.select_related('class_related').filter(
            class_related=student_profile.class_level
        ).order_by('-published_date')
        return render(request, 'students/student_announcements_list.html', {
            'announcements': announcements,
            'has_student_profile': True,
            'student_profile': student_profile
        })
    else:
        announcements = ClassAnnouncement.objects.select_related('class_related').all().order_by('-published_date')
        return render(request, 'students/student_announcements_list.html', {
            'announcements': announcements,
            'has_student_profile': False
        })



@require_POST
def delete_announcement_direct(request, pk):
    user = request.user
    
    if hasattr(user, 'studentprofile_profile'):
        return HttpResponse('Permission denied', status=403)
    
    announcement = get_object_or_404(ClassAnnouncement, pk=pk)
    announcement.delete()
    return redirect('class_announcements_list')