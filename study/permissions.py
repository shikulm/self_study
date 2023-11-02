from rest_framework.permissions import BasePermission

from study.models import Subject, AccessSubjectGroup, Part, UsefulLink


class IsOwner(BasePermission):
    """Класс Permission для предосталения доступа владельцу предмета"""

    def has_permission(self, request, view):
        """Если пользователь автор предмета, возвращет True, иначе False"""
        # Определяем проверяемый объект
        obj = view.get_object()
        # Получаем автора предмета. Запрс к автору зависит от типа модели объекта
        author = None
        if isinstance(obj, Subject):
            author = obj.author
        elif isinstance(obj, (AccessSubjectGroup, Part)):
            author = obj.subject.author
        elif isinstance(obj, UsefulLink):
            author = obj.part.subject.author
        return request.user == author