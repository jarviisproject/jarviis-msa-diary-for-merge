from datetime import datetime

import requests
from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from rest_framework import viewsets, permissions, generics, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, parser_classes

from location.models_process import Location
from userlog.models import UserLog
from userlog.models_data import DbUploader
from userlog.models_process import LogData
from userlog.serializers import UserLogSerializer
from weather.models import Weather


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def process(request):
    LogData().process()
    return JsonResponse({'process Upload': 'SUCCESS'})


@api_view(['GET'])
@parser_classes([JSONParser])
def upload(request):
    DbUploader().insert_data()
    return JsonResponse({'LogData Upload': 'SUCCESS'})


@api_view(['GET'])
@parser_classes([JSONParser])
def test(request):
    # LogData().dummy_from_db()
    return JsonResponse({'test': 'SUCCESS'})

# ===== react api =====


@api_view(['PUT'])
@parser_classes([JSONParser])
def modify(request):
    print("********** modify **********")
    edit = request.data
    print(edit)
    log = UserLog.objects.get(pk=edit['id'])
    db = UserLog.objects.all().filter(id=edit['id']).values()[0]
    db["log_date"] = str(db["log_date"])
    x, y, address = Location().getAddress(db['location'])
    db['address'] = address
    db['x'] = x
    db['y'] = y
    print(f" edit.keys() :: {edit.keys()}")
    print(f' 변경 전 : {db}')
    for i in edit.keys():
        print(f"{i}")
        db[f"{i}"] = edit[f"{i}"]
    db['location'] = str(db['location'])
    # db['location'] = edit['location'] if edit['location'] != "" else db['location']
    # x, y, address = Location().getAddress(db['location'])
    # db['address'] = address
    # db['x'] = x
    # db['y'] = y
    # db['log_date'] = edit['log_date'] if edit['log_date'] != "" else db['log_date']
    # db['weather'] = edit['weather'] if edit['weather'] != "" else db['weather']
    # db['log_type'] = edit['log_type'] if edit['log_type'] != "" else db['log_type']
    # db['contents'] = edit['contents'] if edit['contents'] != "" else db['contents']
    # db['item'] = edit['item']
    print(f' 변경 후 : {db}')
    serializer = UserLogSerializer(data=db)
    # print(f'db type : {type(db)}  // serializer type : {type(serializer)}')
    print(db)
    print(serializer)
    if serializer.is_valid():
        serializer.update(log, db)
        return JsonResponse(data=serializer.data, safe=False)
    print(f"ERROR :: {serializer.errors}")
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@parser_classes([JSONParser])
def remove(request, pk):
    print("********** remove **********")
    print(f'pk : {pk}')
    db = UserLog.objects.get(pk=pk)
    db.delete()
    return JsonResponse({'User Log': 'DELETE SUCCESS'})


@api_view(['POST'])
@parser_classes([JSONParser])
def create(request):
    print("********** create **********")
    new = request.data
    print(f'new : {new}')
    if new['address'] == '':
        if new['location'] == "":
            new['address'] = ""
            new['x'] = ""
            new['y'] = ""
        else:
            x, y, address = Location().getAddress(new['location'])
            new['address'] = address
            new['x'] = x
            new['y'] = y
    else:
        print(new['address'])
        x, y = Location().getLatLng(addr=new['address'])
        new['x'] = x
        new['y'] = y
    UserLog.objects.create(location=new['location'] if new['log_date'] != "" else "장소 없음",
                           address=new['address'],
                           x=new['x'],
                           y=new['y'],
                           log_date=new['log_date'] if new['log_date'] != "" else datetime.now(),
                           weather=new['weather'] if new['weather'] != "" else Weather().process(),
                           log_type=new['log_type'] if new['log_type'] != "" else "normal",
                           contents=new['contents'],
                           # item=new['item'],
                           user_id=new['user_id'])
    return JsonResponse({'USER LOG': 'CREATE SUCCESS'})


@api_view(['POST'])
@parser_classes([JSONParser])
def create_event_log(request):
    url = '혬띠 서버'
    params = '?'
    # completion이 True인 것만 가져와야한다.
    response = requests.get(url, params=params)
    print(response.content)
    events = response.content
    print(f'new : {events}')
    if events['location'] == '':
        pass
    else:
        x, y, address = Location().getAddress(events['location'])
        events['address'] = address
        events['x'] = x
        events['y'] = y
    UserLog.objects.create(location=events['location'],
                           address=events['address'],
                           x=events['x'],
                           y=events['y'],
                           log_date=events['update'],
                           weather=Weather().process(),
                           log_type="events",
                           contents=events['description'],
                           user_id=events['user_id'])


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def find(request):
    return JsonResponse({'getlatlng': 'SUCCESS'})


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def list_by_date(request, user_id, year, month, day):
    print("********** list by date **********")
    print(f'date : {year}-{month}-{day}')
    userlog = UserLog.objects.filter(log_date__year= year, log_date__month=month, log_date__day=day, user_id=user_id)
    serializer = UserLogSerializer(userlog, many=True)
    print(serializer.data)
    return JsonResponse(data = serializer.data, safe=False)

@api_view(['POST'])
@parser_classes([JSONParser])
def list(request):
    print("********** list by date **********")
    post = request.data
    print(post)
    user_id = post['user_id']
    date = post['date']
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    print(f'date : {year}-{month}-{day}')
    userlog = UserLog.objects.filter(log_date__year= year, log_date__month=month, log_date__day=day, user_id=user_id)
    print(userlog)
    serializer = UserLogSerializer(userlog, many=True)
    print(serializer.data)
    return JsonResponse(data = serializer.data, safe=False)


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def search(request, keyword):
    print("********** search **********")
    print(f'keyword : {keyword}')
    userlog = UserLog.objects.filter(contents__icontains= keyword)
    serializer = UserLogSerializer(userlog, many=True)
    print(serializer.data)
    return JsonResponse(data = serializer.data, safe=False)