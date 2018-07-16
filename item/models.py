from django.db import models

from user.models import User
# Create your models here.
class Lost(models.Model):
  user = models.ForeignKey(User, related_name='my_lost', on_delete=models.CASCADE)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  title = models.CharField(max_length=100, blank=True, null=True)
  itemType = models.CharField(max_length=100, blank=True, null=True)
  acquiredDate = models.CharField(max_length=20, blank=True, null=True)
  acquiredTime = models.CharField(max_length=20, blank=True, null=True)
  acquiredPlace = models.CharField(max_length=100, blank=True, null=True)
  storagePlace = models.CharField(max_length=100, blank=True, null=True)
  color = models.CharField(max_length=20, blank=True, null=True)
  comment = models.CharField(max_length=1000, blank=True, null=True)
  isComplete = models.BooleanField(default=False)
  image = models.ImageField(blank=True, null=True)
  class Meta:
    ordering = ('-created',)

class Found(models.Model):
  user = models.ForeignKey(User, related_name='my_found', on_delete=models.CASCADE)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  title = models.CharField(max_length=100, blank=True, null=True)
  itemType = models.CharField(max_length=100, blank=True, null=True)
  acquiredDate = models.CharField(max_length=20, blank=True, null=True)
  acquiredTime = models.CharField(max_length=20, blank=True, null=True)
  acquiredPlace = models.CharField(max_length=100, blank=True, null=True)
  storagePlace = models.CharField(max_length=100, blank=True, null=True)
  color = models.CharField(max_length=20, blank=True, null=True)
  comment = models.CharField(max_length=1000, blank=True, null=True)
  isComplete = models.BooleanField(default=False)
  image = models.ImageField(blank=True, null=True)
  class Meta:
    ordering = ('-created',)
