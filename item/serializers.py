from rest_framework import serializers

from user.models import User
from item.models import *
from user.serializers import *

class LostSerializer(serializers.ModelSerializer):
  image = serializers.ImageField(use_url=True, required=False)
  class Meta:
    model = Lost
    fields = ('id', 'user', 'created', 'updated', 'title', 'itemType',
    'acquiredDate', 'acquiredTime', 'storagePlace',
    'acquiredPlace', 'color', 'comment', 'isComplete', 'image', 'latitude', 'longitude')

class FoundSerializer(serializers.ModelSerializer):
  image = serializers.ImageField(use_url=True, required=False)
  class Meta:
    model = Found
    fields = ('id', 'user', 'created', 'updated', 'title', 'itemType',
    'acquiredDate', 'acquiredTime', 'storagePlace',
    'acquiredPlace', 'color', 'comment', 'isComplete', 'image', 'latitude', 'longituded')
