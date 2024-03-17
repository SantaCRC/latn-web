from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.FileField(upload_to='keys/', blank=True, null=True)
    key_is_active = models.BooleanField(default=False)
    
class Document(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False, default='')
    description = models.TextField(blank=True, null=True, default='')
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
