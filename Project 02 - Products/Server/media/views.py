from django.shortcuts import render

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework import status, generics, mixins
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .models import Media
from . import serializers


@api_view(['GET'])
def list_media(request: Request) -> Response:
    """
    Read all data from the DB and list it
    :param request:
    :return:
    """
    instance = Media.objects.all()
    data = serializers.ListMediaSerializer(instance, many=True)

    return Response(data.data)


@api_view(['GET'])
def get_by_id(request: Request, media_id: int) -> Response:
    """
    Read the requested data from DB using Primary Key id
    :param request:
    :param media_id:
    :return:
    """
    if request.method == 'POST':
        return Response(data={'data': 'Error Occurred',
                              'message': 'Post method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    data = {}
    instance = Media.objects.get(pk=media_id)  # We using primary key many=True not allowed
    try:
        data = serializers.ListAllMediaSerializer(instance).data
    except Exception as e:
        print(e)
        return Response(data={'data': 'Error Occurred',
                              'message': e}, status=status.HTTP_400_BAD_REQUEST)

    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_media(request: Request) -> Response:
    """
    Create the entry in DB
    :param request:
    :return:
    """
    serialized_data = serializers.ListAllMediaSerializer(data=request.data, many=True)

    if serialized_data.is_valid():
        serialized_data.save()
    else:
        print('data not valid')

    response = {'message': 'Data successfully added',
                'data': serialized_data.data}

    return Response(data=response, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def update_media(request: Request, movie_id: int) -> Response:
    """
    Update the data in DB
    :param request:
    :param movie_id:
    :return:
    """
    movie = Media.objects.get(pk=movie_id)

    serializer = serializers.ListAllMediaSerializer(instance=movie, data=request.data)
    if serializer.is_valid():
        serializer.save()

        response = {
            'message': 'Media updated successfully',
            'data': serializer.data,
        }

        return Response(data=response, status=status.HTTP_200_OK)

    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_media(request: Request, media_id: int) -> Response:
    """
    Delete the data in DB
    :param request:
    :param media_id:
    :return:
    """
    instance = get_object_or_404(Media, pk=media_id)
    instance.delete()

    return Response(data={"message": "The media has been deleted"}, status=status.HTTP_204_NO_CONTENT)


# Class based views of class as views ...
class ListAddView(APIView):
    """
    A class as a view for creating and listing the media

    Automatically detect the request method and redirect to respective function
    """
    serializer_class = serializers.ListAllMediaSerializer
    permission_classes = [IsAuthenticated]
    media = Media.objects.all()

    def get(self, request: Request, *args, **kwargs) -> Response:
        serialized = self.serializer_class(instance=self.media, many=True)
        return Response(data=serialized.data, status=status.HTTP_200_OK)

    def post(self, request: Request, *args, **kwargs) -> Response:
        data = request.data
        serialized = self.serializer_class(data=data, many=True)
        if serialized.is_valid():
            serialized.save()

            response: dict = {
                'message': 'Data inserted successfully',
                'data': serialized.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

        response: dict = {
            'message': 'Some error occurred',
            'data': serialized.errors
        }

        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# Class based view with generics and mixins to ease the work ...
class ListAddGenericView(generics.GenericAPIView,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):

    serializer_class = serializers.ListAllMediaSerializer
    queryset = Media.objects.all()

    def get(self, request: Request, *args, **kwargs) -> Response:
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.create(request, *args, **kwargs)

