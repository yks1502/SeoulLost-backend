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

@api_view(['POST','GET'])
@permission_classes((IsAuthenticated,))
def lostList(request):
  if request.method == 'POST':
    dictData = request.data.dict()
    dictData['user']=request.user.id
    modifiedQueryDict = QueryDict('',mutable =True)
    modifiedQueryDict.update(dictData)
    serializer = LostSerializer(data=modifiedQueryDict)
    if serializer.is_valid():
      serializer.save()
      return Response(
        data={'message': 'Lost list에 추가되었습니다'},
        status = status.HTTP_200_OK,
      )
    print(serializer.errors)
    return Response(
      data = {'message':'오류'},
      status = status.HTTP_403_FORBIDDEN,
    )
  elif request.method == 'GET':
    queryset = Lost.objects.all()
    serializers = LostSerializer(queryset, many=True)
    print(serializers.data)
    return Response(serializers.data)

@api_view(['GET','DELETE','PUT'])
@permission_classes((IsAuthenticated,))
def lostDetail(request,pk):
  user = request.user
  lost = Lost.objects.get(pk=pk)
  if user != lost.user:
    return Response(
    data={'message':'권한이 없습니다'}
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
    dictData['user']=request.user.id
    modifiedQueryDict = QueryDict('',mutable =True)
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
def complete_lost(request,pk):
  user = request.user
  lost = Lost.objects.get(pk=pk)
  if user != lost.user:
    return Response(
      data = {'message':'권한이 없습니다'}
    )
  lost.isComplete = True
  lost.save()
  return Response(
    data = {'message': '주인에게 물건이 돌아갔습니다.'},
    status = status.HTTP_200_OK,
  )

@api_view(['POST','GET'])
@permission_classes((IsAuthenticated,))
def foundList(request):
  if request.method == 'POST':
    dictData = request.data.dict()
    dictData['user'] = request.user.id
    modifiedQueryDict = QueryDict('',mutable =True)
    modifiedQueryDict.update(dictData)
    serializer = FoundSerializer(data=modifiedQueryDict)
    if serializer.is_valid():
      serializer.save()
      return Response(
        data = {'message': 'Found list에 추가되었습니다'},
        status = status.HTTP_200_OK,
      )
    print(serializer.errors)
    return Response(
      data = {'message':'오류'},
      status = status.HTTP_403_FORBIDDEN,
    )
  elif request.method == 'GET':
    queryset = Found.objects.all()
    serializers = FoundSerializer(queryset, many=True)
    print(serializers.data)
    return Response(serializers.data)

@api_view(['GET','DELETE','PUT'])
@permission_classes((IsAuthenticated,))
def foundDetail(request,pk):
  user = request.user
  found = Found.objects.get(pk=pk)
  if user != found.user:
    return Response(
    data = {'message':'권한이 없습니다'}
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
    modifiedQueryDict = QueryDict('',mutable =True)
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
def complete_found(request,pk):
  user = request.user
  found = Found.objects.get(pk=pk)
  if user != found.user:
    return Response(
      data = {'message':'권한이 없습니다'}
    )
  found.isComplete = True
  found.save()
  return Response(
    data = {'message': '주인에게 물건이 돌아갔습니다.'},
    status = status.HTTP_200_OK,
  )
