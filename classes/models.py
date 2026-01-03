from django.db import models

class Class(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    schedule_image = models.ImageField(upload_to='class_schedules/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'
        

    def __str__(self):
        return self.name


class ClassAnnouncement(models.Model):
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

    class_related = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=50, choices=SUBJECTS_CHOICES)

    class Meta:
        verbose_name = 'Class Announcement'
        verbose_name_plural = 'Class Announcements'

    def __str__(self):
        return f"{self.title} - {self.class_related.name}"

