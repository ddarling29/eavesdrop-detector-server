from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from . import tasks
import os
import json


@api_view(['POST'])
def detect_eavesdrop(request):
    data = request.data
    scanning = data.get('scanning')
    image = data.get('image')

    if scanning is None or image is None:
        return Response('Malformed request', status=status.HTTP_400_BAD_REQUEST)

    extension = None

    try:
        filename = str(datetime.now())
        extension = os.path.splitext(str(image))[1]
        with open('data/' + filename + extension, 'wb+') as f:
            f.write(image.file.read())
    except:
        return Response('Invalid post parameters', status=status.HTTP_400_BAD_REQUEST)

    try:
        scanning = scanning.upper()
    except:
        return Response('Invalid post parameters', status=status.HTTP_400_BAD_REQUEST)

    result = None

    if scanning == 'TRUE':
        result = tasks.detect_eavesdrop(True, filename, extension)
        return Response(json.dumps({'eavesdrop': result}))
    elif scanning == 'FALSE':
        result = tasks.detect_eavesdrop(False, filename, extension)
        return Response(json.dumps({'eavesdrop': result}))
    else:
        return Response('Invalid post parameters', status=status.HTTP_400_BAD_REQUEST)
