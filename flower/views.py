from django.http import JsonResponse

# Create your views here.
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from flower.models import Flower
from flower.serializers import FlowerSerializer


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def test(request):
    return JsonResponse({'Flower TEST': 'SUCCESS'})


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def list_by_id(request, user_id):
    print("********** list by date **********")
    flower = Flower.objects.filter(user_id=user_id)
    serializer = FlowerSerializer(flower, many=True)
    print(serializer.data)
    return JsonResponse(data = serializer.data, safe=False)