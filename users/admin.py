from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserType, StudentProfile, TeacherProfile

admin.site.register(UserType)
# admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)


from django.contrib import admin
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    # Which fields show up in the list view
    list_display = (
        'display_id', 'user', 'class_level',
        'enrollment_date', 'expected_graduation_year',
        'attendance_rate'
    )
    list_filter = ('class_level', 'expected_graduation_year')
    search_fields = ('student_id', 'user__username', 'parent_name', 'parent_email')

    # Organize fields into sections
    fieldsets = (
        ('Student Info', {
            'fields': ('student_id', 'class_level', 'enrollment_date', 'expected_graduation_year')
        }),
        ('Parent/Guardian Info', {
            'fields': ('parent_name', 'parent_email', 'parent_phone', 'parent_occupation'),
            'classes': ('collapse',)  # collapsible section
        }),
        ('Medical Info', {
            'fields': ('medical_conditions', 'allergies', 'medication'),
            'classes': ('collapse',)
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
        ('Attendance', {
            'fields': ('attendance_rate',)
        }),
    )

    # Optional: make some fields read-only
    readonly_fields = ('student_id', 'display_id')

    # Default ordering
    ordering = ('class_level', 'student_id')
