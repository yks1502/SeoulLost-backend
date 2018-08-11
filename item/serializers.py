from rest_framework import serializers

from user.models import User
from item.models import *
from user.serializers import *

class LostSerializer(serializers.ModelSerializer):
  image = serializers.ImageField(use_url=True, required=False)

  class Meta:
    model = Lost
    fields = ('id', 'user', 'created', 'updated', 'title', 'itemType',
    'acquiredDate',
    'lostPlace', 'color', 'content', 'isComplete', 'image', 'latitude', 'longitude')

class LostRetrieveSerializer(LostSerializer):
  user = NicknameSerializer()

class FoundSerializer(serializers.ModelSerializer):
  image = serializers.ImageField(use_url=True, required=False)

  class Meta:
    model = Found
    fields = ('id', 'user', 'created', 'updated', 'title', 'itemType',
    'acquiredDate', 'storagePlace',
    'acquiredPlace', 'color', 'content', 'isComplete', 'image', 'latitude', 'longitude')

class FoundRetrieveSerializer(FoundSerializer):
  user = NicknameSerializer()

class LostAlarmSerializer(serializers.ModelSerializer):
  class Meta:
    model = LostAlarm
    fields = ('id', 'user', 'lost')
    read_only_fields = ('user', 'lost')

class FoundAlarmSerializer(serializers.ModelSerializer):
  class Meta:
    model = FoundAlarm
    fields = ('id', 'user', 'found')
    read_only_fields = ('user', 'found')
