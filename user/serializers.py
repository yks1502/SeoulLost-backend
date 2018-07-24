from rest_framework import serializers

from user.models import User
from item.models import *

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'email', 'nickname', 'isConfirmed', 'created', 'updated', 'confirmationToken',
    'address', 'contact')

  def get_alarm_count(self, user):
    sale_alarm_count = SaleAlarm.objects.filter(user=user).count()
    purchase_alarm_count = PurchaseAlarm.objects.filter(user=user).count()
    return sale_alarm_count + purchase_alarm_count

class NicknameSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'nickname')

class UserListSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('username', 'created', 'updated', 'address', 'contact')

class UserLostSerializer(serializers.ModelSerializer):
  user = NicknameSerializer()

  class Meta:
    model = Lost
    fields = ('id', 'created', 'updated', 'title', 'user', 'itemType', 'acquiredDate',
    'lostPlace', 'color', 'content', 'isComplete', 'image', 'latitude', 'longitude')

class UserFoundSerializer(serializers.ModelSerializer):
  user = NicknameSerializer()

  class Meta:
    model = Found
    fields = ('id', 'created', 'updated', 'title', 'user', 'itemType', 'acquiredDate', 'storagePlace',
    'acquiredPlace', 'color', 'content', 'isComplete', 'image', 'latitude', 'longitude')

class UserItemSerializer(serializers.ModelSerializer):
  my_lost = UserLostSerializer(many=True)
  my_found = UserFoundSerializer(many=True)

  class Meta:
    model = User
    fields = ('my_lost', 'my_found')

class UserLostAlarmSerializer(serializers.ModelSerializer):
  lost = UserLostSerializer()

  class Meta:
    model = LostAlarm
    fields = ('id', 'user', 'lost')
    read_only_fields = ('user', 'lost',)

class UserFoundAlarmSerializer(serializers.ModelSerializer):
  found = UserFoundSerializer()

  class Meta:
    model = FoundAlarm
    fields = ('id', 'user', 'found')
    read_only_fields = ('user', 'found',)

class UserAlarmSerializer(serializers.ModelSerializer):
  lost_alarm = UserLostAlarmSerializer(many=True)
  found_alarm = UserFoundAlarmSerializer(many=True)

  class Meta:
    model = User
    fields = ('lost_alarm', 'found_alarm',)
