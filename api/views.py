from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def writeModuleStarted(request):
    return Response("Write Module Started!")