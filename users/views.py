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


# from rest_framework import viewsets, permissions
#
# from users.models import User
# from serializers.users import UserSerialaizer
# from users.permissions import IsOwnProfile
#
#
# # Create your views here.
#
# class UserModelViewSet(viewsets.ModelViewSet):
#     """Контроллер для работы с пользователями через API (ViewSet)"""
#     serializer_class = UserSerialaizer
#     queryset = User.objects.all()
#
#     # def get_serializer_class(self):
#     #     """Изменяет Serializer в зависимости от того работает ли пользователь со своим профилем.
#     #     Для собсвенного профиля пользователоя выводится более развернутая информация"""
#     #     if self.action == 'list' or not self.request.user == self.get_object():
#     #         # Пользователь просматривает чужой профиль или весь список пользователей
#     #         return UserOtherSerialaizer
#     #     else:
#     #         # Пользователь просматривает собственный профиль
#     #         return UserSerialaizer
#
#     def get_permissions(self):
#         # if self.action in ('update', 'destroy'):
#         if self.action in ('update', 'partial_update'):
#             self.permission_classes = [permissions.IsAuthenticated, IsOwnProfile]
#         else:
#             self.permission_classes = [permissions.IsAuthenticated]
#         return super().get_permissions()
#
#
#
#
#
