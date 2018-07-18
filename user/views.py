from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from user.models import User
from user.serializers import *

@api_view(['POST'])
def user_signup(request):
  data = request.data
  username = data.get('username', None)
  password = data.get('password', None)
  email = data.get('email', None)
  nickname = data.get('nickname', None)
  address= data.get('address', None)
  contact = data.get('contact', None)
  if len(username) < 6:
    return Response(
      data = {'message': 'invalid username, must be at least 6 charactors long'},
      status = status.HTTP_403_FORBIDDEN,
    )

  if len(password) < 8:
    return Response(
      data = {'message': '비밀번호는 8자 이상이어야 합니다'},
      status = status.HTTP_403_FORBIDDEN,
    )

  if not nickname:
    return Response(
      data = {'message': '닉네임을 입력하여 주십시오'},
      status = status.HTTP_403_FORBIDDEN,
    )

  user, created = User.objects.get_or_create(username=username)
  if created:
    user.email = email
    user.set_password(password)
    user.nickname = nickname
    token = Token.objects.create(user=user)
    user.confirmationToken = token.key
    print(token)
    user.address = address
    user.contact = contact
    user.save()
    return Response(
      data = {'message': '회원가입이 성공적으로 완료되었습니다.'},
      status = status.HTTP_201_CREATED,
    )
  return Response(
    data = {'message': 'duplicate username'},
    status = status.HTTP_403_FORBIDDEN,
  )

@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes((IsAuthenticated,))
def get_user(request):
  if request.method == 'GET':
    user_serializer = UserSerializer(request.user)
    return Response(user_serializer.data)

  elif request.method in ['PUT', 'PATCH']:
    user = request.user
    data = request.data
    if data.get('password', None) is not None:
      user.set_password(data.get('password', None))
    if data.get('nickname', None) is not None:
      user.nickname = data.get('nickname', None)
    user.save()
    return Response(
      data = {'message': '회원정보 변경이 완료되었습니다'},
      status = status.HTTP_200_OK,
    )
class UserList(generics.ListAPIView):
  queryset = User.objects.all()
  serializer_class = UserListSerializer

@api_view(['POST'])
def duplicate_username(request):
  username = request.data
  if User.objects.filter(username=username):
    return Response(
      data = {'message': '중복되는 아이디가 존재합니다'},
      status = status.HTTP_403_FORBIDDEN,
    )
  return Response(
    data = {'message': '사용할 수 있는 아이디입니다'},
    status = status.HTTP_200_OK,
  )
