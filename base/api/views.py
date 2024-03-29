from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    return Response(routes)

@api_view(['GET'])
def get_rooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['Get'])
def get_room(request, primary_key):
    room = Room.objects.get(id=primary_key)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)