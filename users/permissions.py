from rest_framework.permissions import BasePermission


class IsOwnProfile(BasePermission):
    """Класс Permission для запрета доступа у чужому профилю"""
    def has_object_permission(self, request, view, obj):
        """Если пользователь работает с собственным профилем возвращается  True, иначе False"""
        return request.user == obj
