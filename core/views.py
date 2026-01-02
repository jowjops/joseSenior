from django.shortcuts import render
from .models import LatestNews
from classes.models import Class
from django.shortcuts import render
from users.decorators import teacher_or_admin_required
from django.shortcuts import get_object_or_404, redirect
from users.models import StudentProfile
from .models import Announcement


def home(request):
    news = LatestNews.objects.all().order_by('-published_date')[:3]
    return render(request,'core/home.html',{'news':news})


@teacher_or_admin_required
def students_by_class(request):
    classes = Class.objects.prefetch_related('students').all()
    return render(request, 'students/students_by_class.html', {
        'classes': classes
    })

def manage_absence(request, pk): 
    student = get_object_or_404(StudentProfile, pk=pk) 
    return render(request, 'students/student_absense.html', {'student': student})

def increase_absence(request, pk): 
    student = get_object_or_404(StudentProfile, pk=pk) 
    student.absence_value += 1 
    student.save() 
    return redirect('students_by_class') 

def decrease_absence(request, pk):
    student = get_object_or_404(StudentProfile, pk=pk) 
    if student.absence_value > 0: student.absence_value -= 1 
    student.save() 
    return redirect('students_by_class')


def announcement_list(request):
    announcements = Announcement.objects.order_by('-published_date')
    return render(request, 'announcements.html', {'announcements': announcements})