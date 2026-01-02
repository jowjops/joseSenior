from django.db import models

# Create your models here.
class LatestNews(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    news_image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    tag = models.CharField(max_length=50, default='General',null=True, blank=True)

    def __str__(self):
        return self.title

class Announcement(models.Model):
    ANNOUNCEMENT_FOR_CHOICES = [
        ('All', 'All Users'),
        ('Students', 'Students Only'),
        ('Teachers', 'Teachers Only'),
        ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    announcment_for = models.CharField(max_length=50, default='All',null=True, blank=True, choices=ANNOUNCEMENT_FOR_CHOICES)

    def __str__(self):
        return self.title

