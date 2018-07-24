from django.db import transaction
from django.db.models import Q

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from item.models import *
from item.serializers import *
from user.models import User
from user.permissions import IsOwner, IsOwnerOrReadOnly
from django.http import QueryDict
from django.db import transaction

import datetime

@transaction.atomic
@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated,))
def lostList(request):
  if request.method == 'POST':
    dictData = request.data.dict()
    dictData['user'] = request.user.id
    modifiedQueryDict = QueryDict('', mutable=True)
    modifiedQueryDict.update(dictData)
    serializer = LostSerializer(data=modifiedQueryDict)
    if serializer.is_valid():
      serializer.save()
      newLost = Lost.objects.get(id=serializer.data.get('id'))
      lostDate = newLost.created
      oneWeek = datetime.timedelta(days=7)
      related_users = Found.objects.filter(itemType=serializer.data.get('itemType'), isComplete=False).values_list('user', 'created').order_by('user').distinct()
      for related_user in related_users:
        if related_user[0] != request.user.id:
          foundDate = related_user[1]
          if lostDate-foundDate<oneWeek:
            user = User.objects.get(id=related_user[0])
            lost_alarm, created = LostAlarm.objects.get_or_create(user=user, lost=new_lost)
            if created:
              lost_alarm.save()
      return Response(
        data = {'message': 'Lost list에 추가되었습니다'},
        status = status.HTTP_201_CREATED,
      )
    print(serializer.errors)
    return Response(
      data = {'message': '오류'},
      status = status.HTTP_403_FORBIDDEN,
    )
  elif request.method == 'GET':
    queryset = Lost.objects.all()
    serializers = LostSerializer(queryset, many=True)
    return Response(serializers.data)

@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes((IsAuthenticated,))
def lostDetail(request, pk):
  user = request.user
  lost = Lost.objects.get(pk=pk)
  if user != lost.user:
    return Response(
    data={'message': '권한이 없습니다'}
  )
  if request.method == 'GET':
    lost_serializer = LostSerializer(lost)
    return Response(lost_serializer.data)
  elif request.method == 'DELETE':
    lost.delete()
    return Response(
      data = {'message': '삭제가 완료됐습니다.'}
    )
  elif request.method == 'PUT':
    dictData = request.data.dict()
    dictData['user'] = request.user.id
    modifiedQueryDict = QueryDict('', mutable=True)
    modifiedQueryDict.update(dictData)
    serializer = LostSerializer(lost, data=modifiedQueryDict)
    if serializer.is_valid():
      serializer.save()
      return Response(
        data = {'message': 'Lost(잃어버린물건) 정보 변경이 완료되었습니다'},
        status = status.HTTP_200_OK,
      )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def completeLost(request, pk):
  user = request.user
  lost = Lost.objects.get(pk=pk)
  if user != lost.user:
    return Response(
      data = {'message': '권한이 없습니다'}
    )
  lost.isComplete = True
  lost.save()
  return Response(
    data = {'message': '주인에게 물건이 돌아갔습니다.'},
    status = status.HTTP_200_OK,
  )

@transaction.atomic
@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated,))
def foundList(request):
  if request.method == 'POST':
    dictData = request.data.dict()
    dictData['user'] = request.user.id
    modifiedQueryDict = QueryDict('', mutable=True)
    modifiedQueryDict.update(dictData)
    serializer = FoundSerializer(data=modifiedQueryDict)
    if serializer.is_valid():
      serializer.save()
      newFound = Found.objects.get(id=serializer.data.get('id'))
      foundDate = newFound.created
      oneWeek = datetime.timedelta(days=7)
      related_users = Lost.objects.filter(itemType=serializer.data.get('itemType'), isComplete=False).values_list('user','created').order_by('user').distinct()
      for related_user in related_users:
        if related_user[0] != request.user.id:
          lostDate = related_user[1]
          if foundDate-lostDate<oneWeek:
            user = User.objects.get(id=related_user[0])
            found_alarm, created = FoundAlarm.objects.get_or_create(user=user, found=new_found)
            if created:
              found_alarm.save()
      return Response(
        data = {'message': 'Found list에 추가되었습니다'},
        status = status.HTTP_201_CREATED,
      )
    return Response(
      data = {'message': '오류'},
      status = status.HTTP_403_FORBIDDEN,
    )
  elif request.method == 'GET':
    queryset = Found.objects.all()
    serializers = FoundSerializer(queryset, many=True)
    return Response(serializers.data)

@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes((IsAuthenticated,))
def foundDetail(request, pk):
  user = request.user
  found = Found.objects.get(pk=pk)
  if user != found.user:
    return Response(
    data = {'message': '권한이 없습니다'}
  )
  if request.method == 'GET':
    found_serializer = FoundSerializer(found)
    return Response(found_serializer.data)
  elif request.method == 'DELETE':
    found.delete()
    return Response(
      data = {'message': '삭제가 완료됐습니다.'}
    )
  elif request.method == 'PUT':
    dictData = request.data.dict()
    dictData['user'] = request.user.id
    modifiedQueryDict = QueryDict('', mutable=True)
    modifiedQueryDict.update(dictData)
    serializer = FoundSerializer(found, data=modifiedQueryDict)
    if serializer.is_valid():
      serializer.save()
      return Response(
        data = {'message': 'Found(잃어버린물건) 정보 변경이 완료되었습니다'},
        status = status.HTTP_200_OK,
      )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def completeFound(request, pk):
  user = request.user
  found = Found.objects.get(pk=pk)
  if user != found.user:
    return Response(
      data = {'message': '권한이 없습니다'}
    )
  found.isComplete = True
  found.save()
  return Response(
    data = {'message': '주인에게 물건이 돌아갔습니다.'},
    status = status.HTTP_200_OK,
  )

@api_view(['GET', 'DELETE'])
@permission_classes((IsAuthenticated,))
def getLostAlarms(request):
  user = request.user
  lost_alarms = LostAlarm.objects.filter(user=user)
  if request.method == 'GET':
    alarm_serializer = LostAlarmSerializer(lost_alarms, many=True)
    return Response(alarm_serializer.data)
  elif request.method == 'DELETE':
    lost_alarms.delete()

@api_view(['GET', 'DELETE'])
@permission_classes((IsAuthenticated,))
def getFoundAlarms(request):
  user = request.user
  found_alarms = FoundAlarm.objects.filter(user=user)
  if request.method == 'GET':
    alarm_serializer = FoundAlarmSerializer(found_alarms, many=True)
    return Response(alarm_serializer.data)
  elif request.method == 'DELETE':
    found_alarms.delete()
