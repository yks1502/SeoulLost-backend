from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  nickname = models.CharField(max_length=20, blank=True)
  isConfirmed = models.BooleanField(default=False)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  address = models.CharField(max_length=100, blank=True, null=True)
  contact = models.CharField(max_length=11, blank=True, null=True)
  confirmationToken = models.CharField(max_length=100, default='')


  class Meta:
    ordering = ('id',)
