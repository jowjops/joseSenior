# users/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError
from classes.models import Class

# --------------------------
# BaseProfile (abstract)
# --------------------------
class BaseProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='%(class)s_profile')
    bio = models.TextField(blank=True, verbose_name="Biography")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Profile Picture")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Date of Birth")
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], blank=True)
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Phone Number")
    address = models.TextField(blank=True, verbose_name="Home Address")
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True, default="Lebanon")
    
    is_active = models.BooleanField(default=True, verbose_name="Active Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.__class__.__name__}"

    def get_display_name(self):
        return self.user.get_full_name() or self.user.username

# --------------------------
# UserType
# --------------------------
class UserType(models.Model):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('unknown', 'Unknown'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_type')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='unknown')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Type"
        verbose_name_plural = "User Types"
        ordering = ['user_type']

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"

    @property
    def profile(self):
        if hasattr(self.user, f'{self.user_type}_profile'):
            return getattr(self.user, f'{self.user_type}_profile')
        return None

# --------------------------
# StudentProfile
# --------------------------
class StudentProfile(BaseProfile):
    # GRADE_LEVEL_CHOICES = [
    #     ('kindergarten1', 'Kindergarten 1'),
    #     ('kindergarten2', 'Kindergarten 2'),
    #     ('kindergarten3', 'Kindergarten 3'),
    #     ('grade_1', 'Grade 1'),
    #     ('grade_2', 'Grade 2'),
    #     ('grade_3', 'Grade 3'),
    #     ('grade_4', 'Grade 4'),
    #     ('grade_5', 'Grade 5'),
    #     ('grade_6', 'Grade 6'),
    #     ('grade_7', 'Grade 7'),
    #     ('grade_8', 'Grade 8'),
    #     ('grade_9', 'Grade 9'),
    # ]

    student_id = models.CharField(max_length=20, verbose_name="Student ID",null=True,blank=True)
    # class_level = models.CharField(max_length=20, choices=GRADE_LEVEL_CHOICES, verbose_name="Class Level")
    class_level = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Class Level")
    enrollment_date = models.DateField(default=timezone.now, verbose_name="Enrollment Date")
    expected_graduation_year = models.PositiveIntegerField(blank=True, null=True, verbose_name="Expected Graduation Year")
    
    parent_name = models.CharField(max_length=100, verbose_name="Parent/Guardian Name",null=True, blank=True)
    parent_email = models.EmailField(verbose_name="Parent/Guardian Email",null=True, blank=True)
    parent_phone = models.CharField(max_length=20, verbose_name="Parent/Guardian Phone",null=True, blank=True)
    parent_occupation = models.CharField(max_length=100, verbose_name="Parent Occupation",null=True, blank=True)
    
    medical_conditions = models.TextField(blank=True, verbose_name="Medical Conditions")
    allergies = models.TextField(blank=True, verbose_name="Allergies")
    medication = models.TextField(blank=True, verbose_name="Current Medications")
    emergency_contact_name = models.CharField(max_length=100, verbose_name="Emergency Contact Name",null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, verbose_name="Emergency Contact Phone",null=True, blank=True)
    
    attendance_rate = models.DecimalField(max_digits=5, decimal_places=2, default=100.00, verbose_name="Attendance Rate %")
    
    class Meta:
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"
        ordering = ['class_level', 'student_id']
    
    def save(self, *args, **kwargs):
        if not self.student_id:
            self.student_id = f"STU{self.user.id:04d}"
        super().save(*args, **kwargs)

    def clean(self):
        if self.expected_graduation_year and self.expected_graduation_year < 1985:
            raise ValidationError({'expected_graduation_year': 'Graduation year must be 1985 or later.'})

    @property
    def display_id(self):
        return f"STU-{self.student_id}"

# --------------------------
# TeacherProfile
# --------------------------
class TeacherProfile(BaseProfile):
    EMPLOYEE_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('substitute', 'Substitute Teacher'),
    ]
    
    SUBJECTS_CHOICES = [
        ('math', 'Mathematics'),
        ('science', 'Science'),
        ('english', 'English'),
        ('history', 'History'),
        ('geography', 'Geography'),
        ('physics', 'Physics'),
        ('chemistry', 'Chemistry'),
        ('biology', 'Biology'),
        ('french', 'French'),
        ('arabic', 'Arabic'),
        ('art', 'Art'),
        ('music', 'Music'),
        ('pe', 'Physical Education'),
        ('computer', 'Computer Science'),
    ]

    DEPARTMENT_BLOCK_CHOICES = [
        ('dep_a', 'Main Department'),
        ('dep_b', 'New Department'),
        ('dep_both', 'Both Departments'),
    ]

    employee_id = models.CharField(max_length=20, unique=True, verbose_name="Employee ID")
    employee_type = models.CharField(max_length=20, choices=EMPLOYEE_TYPE_CHOICES, verbose_name="Employment Type")
    department = models.CharField(max_length=50, choices=DEPARTMENT_BLOCK_CHOICES, verbose_name="Department")
    position = models.CharField(max_length=100, verbose_name="Job Position", default="Teacher")
    qualifications = models.TextField(blank=True, verbose_name="Qualifications")
    specialization = models.CharField(max_length=200, blank=True, verbose_name="Area of Specialization")
    years_of_experience = models.PositiveIntegerField(default=0, verbose_name="Years of Experience")
    hire_date = models.DateField(default=timezone.now, verbose_name="Hire Date")
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Salary")
    
    subjects_taught = models.CharField(max_length=500, blank=True, verbose_name="Subjects Taught")
    is_homeroom_teacher = models.BooleanField(default=False, verbose_name="Homeroom Teacher")
    max_classes = models.PositiveIntegerField(default=5, verbose_name="Maximum Classes")
    
    # emergency_contact_name = models.CharField(max_length=100, blank=True, verbose_name="Emergency Contact Name", null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, verbose_name="Emergency Contact Phone", null=True)

    class Meta:
        verbose_name = "Teacher Profile"
        verbose_name_plural = "Teacher Profiles"
        ordering = ['department', 'employee_id']

    @property
    def display_id(self):
        return f"TCH-{self.employee_id}"

    @property
    def subject_list(self):
        return [subject.strip() for subject in self.subjects_taught.split(',')] if self.subjects_taught else []


# --------------------------
# Signals
# --------------------------
@receiver(post_save, sender=User)
def create_usertype(sender, instance, created, **kwargs):
    if created:
        try:
            from django.db import connection
            table_exists = 'users_usertype' in connection.introspection.table_names()
            
            if table_exists:
                UserType.objects.get_or_create(user=instance, defaults={'user_type': 'unknown'})
                print(f"✅ Created UserType for {instance.username}")
            else:
                print(f"⚠️ UserType table doesn't exist yet for {instance.username}")
        except Exception as e:
            print(f"❌ Error creating UserType for {instance.username}: {e}")

@receiver(post_save, sender=UserType)
def create_profile(sender, instance, created, **kwargs):
    if instance.user_type == 'student' and not hasattr(instance.user, 'student_profile'):
        StudentProfile.objects.create(
            user=instance.user,
            student_id=f"STU{instance.user.id:04d}",
            class_level='grade_1',
            enrollment_date=timezone.now(),
            parent_name="To be filled",
            parent_email="parent@example.com",
            parent_phone="+961700000000",
            parent_occupation="To be specified",
            emergency_contact_name="To be filled",
            emergency_contact_phone="+961700000000",
            current_gpa=None,
            major_subject=""
        )
        print(f"✅ Auto-created StudentProfile for {instance.user.username}")

    elif instance.user_type == 'teacher' and not hasattr(instance.user, 'teacher_profile'):
        TeacherProfile.objects.create(
            user=instance.user,
            employee_id=f"TCH{instance.user.id:04d}",
            employee_type='full_time',
            department='dep_a',
            position='Teacher',
            qualifications="To be specified",
            specialization="To be specified",
            years_of_experience=0,
            hire_date=timezone.now(),
            salary=None,
            subjects_taught="To be specified",
            is_homeroom_teacher=False,
            max_classes=5,
            emergency_contact_name="To be filled",
            emergency_contact_phone="+961700000000"
        )
        print(f"✅ Auto-created TeacherProfile for {instance.user.username}")

# --------------------------
# Helper methods for User
# --------------------------
def get_profile(self):
    if hasattr(self, 'user_type'):
        return self.user_type.profile
    return None

def get_user_type_display(self):
    if hasattr(self, 'user_type'):
        return self.user_type.get_user_type_display()
    return "Unknown"

User.add_to_class('get_profile', get_profile)
User.add_to_class('get_user_type_display', get_user_type_display)

