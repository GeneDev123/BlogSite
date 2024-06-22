from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class BlogPost(models.Model):
  title = models.CharField(max_length=255)
  content = models.TextField()
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.title

class ContactMessage(models.Model):
  name = models.CharField(max_length=100)
  email = models.EmailField()
  message = models.TextField()
  timestamp = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return f'{self.name} - {self.email}'
      
class FileUpload(models.Model):
  file_name = models.CharField(max_length=255)
  file = models.FileField(upload_to='media/')
  category = models.CharField(max_length=255)
  date_uploaded = models.DateTimeField(auto_now_add=True)
  date_modified = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.file_name
