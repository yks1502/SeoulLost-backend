from django.db import transaction
from django.db.models import Q

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from item.models import *
from item.serializers import *
from user.models import User
from user.permissions import IsOwner, IsOwnerOrReadOnly
from django.http import QueryDict
from django.db import transaction

import datetime

@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated,))
@transaction.atomic
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
      relatedUsers = Found.objects.filter(itemType=serializer.data.get('itemType'), isComplete=False).values_list('user', 'created').order_by('user').distinct()
      for relatedUser in relatedUsers:
        if relatedUser[0] != request.user.id:
          foundDate = relatedUser[1]
          if lostDate - foundDate < oneWeek:
            user = User.objects.get(id=relatedUser[0])
            lostAlarm, created = LostAlarm.objects.get_or_create(user=user, lost=newLost)
            if created:
              lostAlarm.save()
      return Response(
        data = {'message': 'Lost list에 추가되었습니다'},
        status = status.HTTP_201_CREATED,
      )
    return Response(
      data = {'message': '오류'},
      status = status.HTTP_403_FORBIDDEN,
    )
  elif request.method == 'GET':
    paginator = api_settings.DEFAULT_PAGINATION_CLASS()
    queryset = Lost.objects.all()
    page = paginator.paginate_queryset(queryset, request)
    serializers = LostRetrieveSerializer(page, many=True)
    return paginator.get_paginated_response(serializers.data)

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
    lostSerializer = LostSerializer(lost)
    return Response(lostSerializer.data)
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

@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated,))
@transaction.atomic
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
      relatedUsers = Lost.objects.filter(itemType=serializer.data.get('itemType'), isComplete=False).values_list('user', 'created').order_by('user').distinct()
      for relatedUser in relatedUsers:
        if relatedUser[0] != request.user.id:
          lostDate = relatedUser[1]
          if foundDate - lostDate < oneWeek:
            user = User.objects.get(id=relatedUser[0])
            foundAlarm, created = FoundAlarm.objects.get_or_create(user=user, found=newFound)
            if created:
              foundAlarm.save()
      return Response(
        data = {'message': 'Found list에 추가되었습니다'},
        status = status.HTTP_201_CREATED,
      )
    return Response(
      data = {'message': '오류'},
      status = status.HTTP_403_FORBIDDEN,
    )
  elif request.method == 'GET':
    paginator = api_settings.DEFAULT_PAGINATION_CLASS()
    queryset = Found.objects.all()
    page = paginator.paginate_queryset(queryset, request)
    serializers = FoundRetrieveSerializer(page, many=True)
    return paginator.get_paginated_response(serializers.data)

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
    foundSerializer = FoundSerializer(found)
    return Response(foundSerializer.data)
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
  lostAlarms = LostAlarm.objects.filter(user=user)
  if request.method == 'GET':
    alarmSerializer = LostAlarmSerializer(lostAlarms, many=True)
    return Response(alarmSerializer.data)
  elif request.method == 'DELETE':
    lostAlarms.delete()

@api_view(['GET', 'DELETE'])
@permission_classes((IsAuthenticated,))
def getFoundAlarms(request):
  user = request.user
  foundAlarms = FoundAlarm.objects.filter(user=user)
  if request.method == 'GET':
    alarmSerializer = FoundAlarmSerializer(foundAlarms, many=True)
    return Response(alarmSerializer.data)
  elif request.method == 'DELETE':
    foundAlarms.delete()
