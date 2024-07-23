from django.shortcuts import render
from .models import User
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import generics, status
from rest_framework.views import APIView


# Create your views here.
class UserSignUpView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request: Request):
        data = request.data

        serialized = self.serializer_class(data=data)

        if serialized.is_valid():
            serialized.save()

            response: dict = {
                "message": "data saved successfully",
                "data": serialized.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serialized.data, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """

    """
    def post(self, request: Request) -> Response:
        username = request.data.get('username')
        password = request.data.get("password")

        print(username, password)
        user = authenticate(username=username, password=password)

        print(f'user = {user}')
        if user is not None:
            response: dict = {
                "message": "Login successful",
                "token": user.auth_token.key
            }
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid username (or) password"})

    def get(self, request: Request) -> Response:
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)





