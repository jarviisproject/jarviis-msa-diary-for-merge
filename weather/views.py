from django.http import JsonResponse

# Create your views here.
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from weather.models import Weather


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def weather_test(request):
    Weather().process()
    return JsonResponse({'Weather TEST': 'SUCCESS'})

@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def process(request):
    # Weather().weather_pre()
    return JsonResponse(Weather().weather_pre())