from django.http import JsonResponse

# Create your views here.
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from location.models_process import Location


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def getLatLng(request):
    Location().getLatLng("서울특별시 서초구 강남대로 373 홍우빌딩 1층")
    return JsonResponse({'getlatlng': 'SUCCESS'})


