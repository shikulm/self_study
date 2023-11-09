from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from users.models import User
from serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        # if user.is_valid():
        #     user.save()
        #     return Response(user, status=status.HTTP_200_OK)
        # return Response(user.errors)



