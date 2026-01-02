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