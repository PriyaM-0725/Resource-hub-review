from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from subjects.models import Subject


class Resource(models.Model):
    RESOURCE_TYPES = (
        ('notes', 'Notes'),
        ('pyq', 'Previous Year Questions'),
        ('assignment', 'Assignment'),
        ('lab', 'Lab'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    file = models.FileField(upload_to='resources/')

    type = models.CharField(max_length=20, choices=RESOURCE_TYPES)

    subject = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # 🔥 Access Control (IMPORTANT)
    branch = models.CharField(max_length=50)
    year = models.IntegerField()
    regulation = models.CharField(max_length=20)

    downloads_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
from django.conf import settings

class Bookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.resource.title}"
    
class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.resource.title} ({self.rating})"
    
class DownloadLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} downloaded {self.resource.title}"