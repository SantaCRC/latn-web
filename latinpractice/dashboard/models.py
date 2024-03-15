from django.db import models

class User(models.Model):
    firstname = models.CharField(max_length=255, blank=False, null=False, default='')
    lastname = models.CharField(max_length=255, blank=False, null=False, default='')
    username = models.CharField(max_length=255, unique=True, blank=False, null=False, default='')
    password = models.CharField(max_length=255, blank=False, null=False, default='')
    email = models.CharField(max_length=255, unique=True, blank=False, null=False, default='')
    force_reset = models.BooleanField(default=True)
    key_url = models.CharField(max_length=255, blank=True, null=True, default='')
    
class Document(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False, default='')
    description = models.TextField(blank=True, null=True, default='')
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
