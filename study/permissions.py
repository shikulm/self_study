from rest_framework.permissions import BasePermission

from study.models import Subject, AccessSubjectGroup, Part, UsefulLink
from tests_study.models import Question, Test


class MixinPermission:
    """Класс-миксин для вспомогательных функций, необходимых для проверки прав пользоватлей"""

    def get_subject(self, obj):
        """Метод возвращает экземпляр предмета, которому принадлежит объекта модели obj (предмет, раздел и т.д.)"""
        subject = None
        if isinstance(obj, Subject):
            subject = obj
        elif isinstance(obj, (AccessSubjectGroup, Part)):
            subject = obj.subject
        elif isinstance(obj, (UsefulLink, Question)):
            subject = obj.part.subject
        elif isinstance(obj, Test):
            subject = obj.part.subject if obj.part else obj.subject
        return subject


    def check_owner(self, obj, user):
        """Проверяет принадлежит ли объект obj автору user"""
        subj = self.get_subject(obj)
        author = subj.author if subj else None
        return user == author


    def check_subscribed_user(self, obj, user):
        """Проверяет подписан ли пользователь user на объект obj"""
        subj = self.get_subject(obj)
        return AccessSubjectGroup.objects.filter(user=user, subject=subj).exists()


class IsOwner(BasePermission, MixinPermission):
    """Класс Permission для предосталения доступа владельцу предмета"""

    def has_permission(self, request, view):
        """Если пользователь автор предмета, возвращет True, иначе False"""
        # Определяем проверяемый объект
        if request.method == 'POST':
            # Для запросов POST данные по создаваемому объекту формируются программно с помощью метода get_object() в представлении, поэтому обращаемся к нему.
            # В остальных случаях используется has_object_permission, для которого параметр obj содержит данные проверяемого объекта
            obj = view.get_object()
            return self.check_owner(obj=obj, user=request.user)
        return True

    def has_object_permission(self, request, view, obj):
        """Если пользователь автор предмета, возвращет True, иначе False"""
        # Получаем автора предмета. Запрос к автору зависит от типа модели объекта
        return self.check_owner(obj=obj, user=request.user)


class IsSubscribedUser(BasePermission, MixinPermission):
    """Класс Permission для предосталения доступа подписанным на предмет пользователям"""

    def has_permission(self, request, view):
        """Если пользователь подписан на предмет, возвращет True, иначе False"""
        # Определяем проверяемый объект
        print("request.method", request.method)
        if request.method == 'POST':
            # Для запросов POST данные по создаваемому объекту формируются программно с помощью метода get_object() в представлении, поэтому обращаемся к нему.
            # В остальных случаях используется параметр obj в методе has_object_permission, который вернет данные проверяемого объекта
            # obj = view.serializer_class.Meta.model
            obj = view.get_object()
            print("obj=", obj)
            ret = self.check_subscribed_user(obj=obj, user=request.user)
            print("ret=", ret)
            # return self.check_owner(obj=obj, user=request.user)
        return True

    def has_object_permission(self, request, view, obj):
        """Если пользователь автор предмета, возвращет True, иначе False"""
        return self.check_subscribed_user(obj=obj, user=request.user)

class IsSelfTestUser(BasePermission):
    """Класс Permission для предосталения доступа пользователю возможности отправки ответов на вопросы его теста"""

    def has_object_permission(self, request, view, obj):
        """Если пользователь отвечает на вопросы своего теста, возвращет True, иначе False"""
        return request.user==obj.user





    # def has_permission(self, request, view):
    #     """Если пользователь автор предмета, возвращет True, иначе False"""
    #     # Определяем проверяемый объект
    #     obj = view.get_object()
    #     # Получаем предмет. Запрос к предмету зависит от типа модели объекта
    #     subject = None
    #     if isinstance(obj, Subject):
    #         subject = obj
    #     elif isinstance(obj, (AccessSubjectGroup, Part)):
    #         subject = obj.subject
    #     elif isinstance(obj, UsefulLink):
    #         subject = obj.part.subject
    #     return AccessSubjectGroup.objects.filter(user=request.user, subject=subject).exists()

# class IsOwner(BasePermission):
#     """Класс Permission для предосталения доступа владельцу предмета"""
#     def has_permission(self, request, view):
#         """Если пользователь автор предмета, возвращет True, иначе False"""
#         # Определяем проверяемый объект
#         if request.method == 'POST':
#             # Для запросов POST данные по создаваемому объекту формируются проагрммно с помощью метода get_object() в представлении, поэтому обращаемся к нему.
#             # В остальных случаях obj вернет данные проверяемого объекта
#             # obj = view.serializer_class.Meta.model
#             obj = view.get_object()
#         # Получаем автора предмета. Запрос к автору зависит от типа модели объекта
#             author = None
#             if isinstance(obj, Subject):
#                 author = obj.author
#             elif isinstance(obj, (AccessSubjectGroup, Part)):
#                 author = obj.subject.author
#             elif isinstance(obj, UsefulLink):
#                 author = obj.part.subject.author
#             return request.user == author
#         return True
#
#
#
#     def has_object_permission(self, request, view, obj):
#         """Если пользователь автор предмета, возвращет True, иначе False"""
#         # Получаем автора предмета. Запрос к автору зависит от типа модели объекта
#         author = None
#         if isinstance(obj, Subject):
#             author = obj.author
#         elif isinstance(obj, (AccessSubjectGroup, Part)):
#             author = obj.subject.author
#         elif isinstance(obj, UsefulLink):
#             author = obj.part.subject.author
#         return request.user == author
#
#
#     # def has_permission(self, request, view):
#     #     """Если пользователь автор предмета, возвращет True, иначе False"""
#     #     # Определяем проверяемый объект
#     #     # obj = view.serializer_class.Meta.model
#     #     obj = view.get_object()
#     #     # Получаем автора предмета. Запрос к автору зависит от типа модели объекта
#     #     author = None
#     #     if isinstance(obj, Subject):
#     #         author = obj.author
#     #     elif isinstance(obj, (AccessSubjectGroup, Part)):
#     #         author = obj.subject.author
#     #     elif isinstance(obj, UsefulLink):
#     #         author = obj.part.subject.author
#     #     return request.user == author
#
#
# class IsSubscribedUser(BasePermission):
#     """Класс Permission для предосталения доступа подписанным на предмет пользователям"""
#
#     def has_permission(self, request, view):
#         """Если пользователь автор предмета, возвращет True, иначе False"""
#         # Определяем проверяемый объект
#         if request.method == 'POST':
#             # Для запросов POST данные по создаваемому объекту формируются проагрммно с помощью метода get_object() в представлении, поэтому обращаемся к нему.
#             # В остальных случаях obj ернет данные проверяемого объекта
#             # obj = view.serializer_class.Meta.model
#             obj = view.get_object()
#
#             # Получаем предмет. Запрос к предмету зависит от типа модели объекта
#             subject = None
#             if isinstance(obj, Subject):
#                 subject = obj
#             elif isinstance(obj, (AccessSubjectGroup, Part)):
#                 subject = obj.subject
#             elif isinstance(obj, UsefulLink):
#                 subject = obj.part.subject
#             return AccessSubjectGroup.objects.filter(user=request.user, subject=subject).exists()
#         return True
#
#
#     def has_object_permission(self, request, view, obj):
#         """Если пользователь автор предмета, возвращет True, иначе False"""
#         # Определяем проверяемый объект
#         if request.method == 'POST':
#             # Для запросов POST данные по создаваемому объекту формируются проагрммно с помощью метода get_object() в представлении, поэтому обращаемся к нему.
#             # В остальных случаях obj ернет данные проверяемого объекта
#             # obj = view.serializer_class.Meta.model
#             obj = view.get_object()
#
#         # Получаем предмет. Запрос к предмету зависит от типа модели объекта
#         subject = None
#         if isinstance(obj, Subject):
#             subject = obj
#         elif isinstance(obj, (AccessSubjectGroup, Part)):
#             subject = obj.subject
#         elif isinstance(obj, UsefulLink):
#             subject = obj.part.subject
#         return AccessSubjectGroup.objects.filter(user=request.user, subject=subject).exists()
#
#     # def has_permission(self, request, view):
#     #     """Если пользователь автор предмета, возвращет True, иначе False"""
#     #     # Определяем проверяемый объект
#     #     obj = view.get_object()
#     #     # Получаем предмет. Запрос к предмету зависит от типа модели объекта
#     #     subject = None
#     #     if isinstance(obj, Subject):
#     #         subject = obj
#     #     elif isinstance(obj, (AccessSubjectGroup, Part)):
#     #         subject = obj.subject
#     #     elif isinstance(obj, UsefulLink):
#     #         subject = obj.part.subject
#     #     return AccessSubjectGroup.objects.filter(user=request.user, subject=subject).exists()
