from rest_framework import serializers

from user.models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'email', 'nickname', 'isConfirmed', 'created', 'updated', 'confirmationToken',
    'address', 'contact')

class NicknameSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'nickname')

class UserListSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('username', 'created', 'updated', 'address', 'contact')
