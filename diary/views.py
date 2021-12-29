import datetime
# from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from diary.models import Diary
from diary.models_data import DbUploader
from diary.serializers import DiarySerializer


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def process(request):
    return JsonResponse({'process': 'SUCCESS'})


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def find(request, user_id, year, month, day):
    print("********** find START **********")
    print(f'date : {year}-{month}-{day}')
    try:
        diary = Diary.objects.filter(user_id=int(user_id), diary_date__year= year, diary_date__month=month, diary_date__day=day).values()[0]
        print("성공")
        print(diary)
        serializer = DiarySerializer(diary)
        print("시리얼라이즈 성공")
        return JsonResponse(data=serializer.data, safe=False)
    except:
        diary = Diary.objects.filter(user_id=int(user_id), diary_date__year=year, diary_date__month=month,
                                     diary_date__day=day)
        print("실패")
        print(diary)
        return JsonResponse({'diary_date': f'{year}-{month}-{day}','process': 'Nothing'})
    # print(diary)
    # print("********** serializer **********")
    # print(serializer.data)


@api_view(['PUT'])
@parser_classes([JSONParser])
def modify_memo(request):
    print("********** modify MEMO START **********")
    edit = request.data
    print(f"edit :: {edit}")
    diary = Diary.objects.get(pk=edit['id'])
    db = Diary.objects.filter(pk=edit['id']).values()[0]
    print(f"diary :: {diary}")
    db['memo'] = edit['memo']
    db['diary_date'] = str(db['diary_date'])
    print(f"수정한 db :: {db}")
    # db['log_id'] = edit['log_id']
    serializer = DiarySerializer(data=db)
    print(f"serializer :: {serializer}")
    if serializer.is_valid():
        serializer.update(diary, db)
        return JsonResponse(data=serializer.data, safe=False)
    print(serializer.errors)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def upload(request, user_id):
    print("********** NEW diary upload START **********")
    print(f"오늘은 {datetime.date.today().year} {datetime.date.today().month} {datetime.date.today().day}")

    check = Diary.objects.filter(diary_date__year=datetime.date.today().year,
                                 diary_date__month=datetime.date.today().month,
                                 diary_date__day=datetime.date.today().day,
                                 user_id=user_id)
    # print(check)
    check_exist = check.exists()
    print(check_exist)
    if check_exist == True:
        print("********** modify diary START **********")
        print(check.values()[0])
        check = check.values()[0]
        new = DbUploader().modify_data(user_id)
        print(new.keys())
        for i in new.keys():
            # print(f"i :: {i}")
            # print(f"check 변경전 :: {check[str(i)]}")
            # print(f"new :: {new[str(i)]}")
            check[str(i)] = new[str(i)]
            # print(f"check 변경후 :: {check[str(i)]}")
        check["diary_date"] = str(check["diary_date"])
        # check["log_id"] = str(check["log_id"])
        serializer = DiarySerializer(data=check)
        # print("*************Serializer")
        # print(serializer)
        if serializer.is_valid():
            check_orm = Diary.objects.get(pk=check['id'])
            serializer.update(check_orm, check)
            return JsonResponse({'Modify diary': 'SUCCESS'})
        print(serializer.errors)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        DbUploader().insert_data(user_id)
        print("create")
    return JsonResponse({'NEW diary': 'SUCCESS'})


# @api_view(['PUT'])
# @parser_classes([JSONParser])
# def modify_memo(request):
#     print("********** modify START **********")
#     edit = request.data
#     # print(edit)
#     diary = Diary.objects.get(pk=edit['id'])
#     db = Diary.objects.filter(pk=edit['id']).values()[0]
#     # print(diary)
#     db['memo'] = edit['memo']
#     db['diary_date'] = edit['diary_date']
#     db['log_id'] = edit['log_id']
#     serializer = DiarySerializer(data=db)
#     if serializer.is_valid():
#         serializer.update(diary, db)
#         return JsonResponse(data=serializer.data, safe=False)
#     return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

