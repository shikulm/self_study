from django.db import models
from django.db.models import Max, Q
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, viewsets, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from study.models import Subject, Part, UsefulLink, AccessSubjectGroup
from serializers.study import SubjectSerializer, AccessSubjectGroupSerializer, SubjectAccessSerializer, PartForAuthorSerializer, PartForStudentSerializer
    # AccessSubjectOnlyUserSerializer
# AccessSubjectUserSerializer
from study.permissions import IsOwner, IsSubscribedUser
from users.models import User


###### Subject APIView
class SubjectCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания предмета через API.
    Создавать предметы может любой авторизованный пользователь.
    Пользователь, создающий предмет, становится его автором и владельцем.
    Пример API-запроса POST: http://127.0.0.1:8000/api/subject/create/"""
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Назначение автора при создании предмета"""
        new_subject = serializer.save()
        new_subject.author = self.request.user
        new_subject.save()


class SubjectListAPIView(generics.ListAPIView):
    """Контроллер для получения списка всех предметов через API.
    Просматривать списки могут любые авторизованные пользователи.
    Результат можно фильровать и сортировать с помощью параметров:
     - search=<текст> - ищет текст в полях title, description
     - <поле>=<значение> - ищет в <поле> <значение>. В качестве полей можно указать  id, title, description
     - ordering=<поле1>,<поле2>,... - сортирует по перечисленным полям. В качестве полей можно указывать id, title.
     Пример API-запроса GET: http://127.0.0.1:8000/api/subject?search=теория&id=1&ordering=title
    """
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()
    permission_classes = [IsAuthenticated]

    # Поиск в результирующем наборе
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["title", "description",] # Для SearchFilter
    filterset_fields = ["id", "title", "description", ]  # Для DjangoFilterBackend
    ordering_fields = ["id", "title",]   # Для OrderingFilter


class SubjectListMeAPIView(generics.ListAPIView):
    """Контроллер для получения списка всех предметов авторизованного пользователяв через API.
    Просматривать спсики могут любые авторизованные пользователи.
    Пример API-запроса GET: http://127.0.0.1:8000/api/subject/me/"""
    serializer_class = SubjectSerializer
    # queryset = Subject.objects.filter()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subject.objects.filter(author=self.request.user)


class  SubjectRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для получения детальной информации по предмету через API.
    Просматривать детализированные данные по конкретному предмету могут только его авторы и подписанные пользователи"""
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()
    permission_classes = [IsAuthenticated, IsOwner|IsSubscribedUser]
    # permission_classes = [IsOwner|IsSubscribedUser]


class  SubjectUpdateAPIView(generics.UpdateAPIView, generics.RetrieveUpdateAPIView):
    """Контроллер для обновления информации по предмету через API.
    Обновлять данные по конкретному предмету могут только его авторы"""
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class  SubjectDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления информации по предмету через API.
    Удалять данные по конкретному предмету могут только его авторы"""
    queryset = Subject.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


# class SubjectViewSet(viewsets.ModelViewSet):
#     """Контроллер для работы с предметами через API (ViewSet).
#     Просматривать и создавать информацию могут все пользователи,
#     редактировать и удалять - только авторы курса и администарторы
#     """
#     queryset = Subject.objects.all()
#     serializer_class = SubjectSerializer
#
#     def get_permissions(self):
#         """Определение прав доступа"""
#         if self.action in ('create', 'list'):
#             permission_classes = [IsAuthenticated]
#         elif self.action == 'retrieve':
#             permission_classes = [IsAuthenticated, IsOwner]
#         elif self.action in ('update', 'destroy'):
#             permission_classes = [IsAuthenticated, IsOwner]
#         return [permission() for permission in permission_classes]
#
#
#     def perform_create(self, serializer):
#         """Назначение владельца при создании курса"""
#         new_subject = serializer.save()
#         new_subject.author = self.request.user
#         new_subject.save()


####### AccessSubjectGroup APIView
class GrantUserAPIView(APIView):
    """Контроллер для предоставления пользователю доступа к предмету.
    Предоставлять доступ к предмету могут только его авторы"""
    permission_classes = [IsAuthenticated, IsOwner]
    def post(self, request, pk_subject, pk_user):
        """Обработка api-запроса на добавление пользователя в модель AccessSubjectGroup"""
        access_group = self.get_object()
        if access_group is None:
            # Объект не получилось создать
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AccessSubjectGroupSerializer(access_group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


        # try:
        #     subject = Subject.objects.get(pk=pk_subject)
        #     user = User.objects.get(pk=pk_user)
        # except (Subject.DoesNotExist, User.DoesNotExist):
        #     return Response(status=status.HTTP_404_NOT_FOUND)
        #
        # access_group = AccessSubjectGroup(subject=subject, user=user)
        # access_group.save()
        #
        # serializer = AccessSubjectGroupSerializer(access_group)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_object(self):
        """Возвращает ссылку на созданный объект. Если объект не может быть создан, то возвращает None.
        Метод используется для проверки разрешения IsOwner"""
        pk_subject=self.kwargs.get("pk_subject")
        pk_user=self.kwargs.get("pk_user")

        # Проверяем существование предмета и пользователя, указанных в параметрах
        try:
            subject = Subject.objects.get(pk=pk_subject)
            user = User.objects.get(pk=pk_user)
        except (Subject.DoesNotExist, User.DoesNotExist):
            return None

        # Пробуем найти запись с переданными параметрами в модели AccessSubjectGroup
        try:
            access_group = AccessSubjectGroup.objects.get(subject=subject, user=user)
        except (AccessSubjectGroup.DoesNotExist):
        # Если объект не найден, то создаем его
            access_group = AccessSubjectGroup(subject=subject, user=user)
            access_group.save()
        return access_group

class DenyUserAPIView(APIView):
    """Контроллер для запрета пользователю доступа к предмету.
    Удалить пользщователя из спсика подписки могут только его авторы."""
    permission_classes = [IsAuthenticated, IsOwner]
    def delete(self, request, pk_subject, pk_user):
        """Обработка api-запроса на удаление пользователя из модели AccessSubjectGroup"""
        access_group = self.get_object()
        if access_group is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Проверка доступа с использованием has_object_permission()
        self.check_object_permissions(request, access_group)
        # has_object_permission(self, request, view, obj)

        access_group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


        # try:
        #     access_group = AccessSubjectGroup.objects.get(subject__pk=pk_subject, user__pk=pk_user)
        # except AccessSubjectGroup.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
        #
        # access_group.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        """Возвращает ссылку на удаляемый объект. Если объект не существует, то возвращает None.
        Метод используется для проверки разрешения IsOwner"""
        pk_subject=self.kwargs.get("pk_subject")
        pk_user=self.kwargs.get("pk_user")

        # Проверяем существование предмета и пользователя, указанных в параметрах
        try:
            subject = Subject.objects.get(pk=pk_subject)
            user = User.objects.get(pk=pk_user)
        except (Subject.DoesNotExist, User.DoesNotExist):
            return None

        # Пробуем найти запись с переданными параметрами в модели AccessSubjectGroup
        try:
            access_group = AccessSubjectGroup.objects.get(subject=subject, user=user)
        except AccessSubjectGroup.DoesNotExist:
        # Если объект не найден, то создаем его без сохранения (сохранять не требуется, т.к. в итоге объект удаляется)
            access_group = AccessSubjectGroup(subject=subject, user=user)
            # access_group.save()
        return access_group


class SubjectAccessListAPIView(generics.ListAPIView):
    """Контроллер для получения списка предметов и подписанных на них пользоатлей через API.
    Просматривать инфомацию по всем предметам могут только администраторы (is_staff=True), авторы предметов получают информацию только по своим предметам.
    Результат можно фильровать и сортировать с помощью параметров:
     - search=<текст> - ищет текст в полях title, description, author__email, access_users__email
     - <поле>=<значение> - ищет в поле значение. В качестве полей можно указать  id, title, description, author__email, access_users__email
     - ordering=<поле1>,<поле2>,... - сортирует по перечисленным полям. В качестве полей можно указывать id, title, author__email.
     Пример API-запроса GET: http://127.0.0.1:8000/api/subject/access?search=теория&id=1&ordering=author__email
     """
    serializer_class = SubjectAccessSerializer
    permission_classes = [IsAuthenticated]

    # Поиск в результирующем наборе
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["title", "description", "author__email", "access_users__email",] # Для SearchFilter
    filterset_fields = ["id", "title", "description", "author__email", "access_users__email", ]  # Для DjangoFilterBackend
    ordering_fields = ["id", "title", "author__email"]   # Для OrderingFilter
    def get_queryset(self):
        """Для администраторов возвращает все предметы, а лдля остальных пользоватлей - только предметы, принадлежащие пользователю"""
        if self.request.user.is_staff:
            return Subject.objects.all()
        else:
            return Subject.objects.filter(author=self.request.user)


# class AccessSubjectUserSerializerAPIView(generics.ListAPIView):
#     """Контроллер для получения списка предметов и подписанных на них пользоатлей через API.
#     Просмтаривать инфомацию по всем предметам могут только администраторы, авторы предметов получают информацию толоько по своим курсам"""
#     serializer_class = AccessSubjectOnlyUserSerializer
#     # queryset = Subject.objects.all()
#     # permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         # return AccessSubjectGroup.objects.all()
#         return AccessSubjectGroup.objects.all()


###### Part APIView
class PartCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания раздела предмета через API.
    Создавать разделы может автор предмета.
    Пример API-запроса POST: http://127.0.0.1:8000/api/part/create/"""
    serializer_class = PartForAuthorSerializer
    # queryset = Part.objects.all()
    permission_classes = [IsOwner|IsAdminUser]

    def get_new_order_id(self, subject):
        """Вычисляет порядковый номер добавляемого объекта (номер должен быть на 1 больше предыдущего раздела предмета)"""
        last_order_id = Part.objects.filter(subject=subject).aggregate(order_id_last=Max('order_id')).get('order_id_last')
        return last_order_id+1 if last_order_id else 1


    def perform_create(self, serializer):
        """Вычисление порядкового номера добавляемого раздела (максимальный для предмета + 1)"""
        if serializer.is_valid():
            new_part = serializer.save()
            # last_order_id = Part.objects.filter(subject=new_part.subject).aggregate(order_id_last=Max('order_id')).get('order_id_last')
            # new_part.order_id = last_order_id+1 if last_order_id else 1
            new_part.order_id = self.get_new_order_id(new_part.subject)
            # new_part.order_id = Part.objects.filter(subject=new_part.subject).aggregate(order_id_last=Max('order_id')).get('order_id_last')+1
            # new_part.order_id = Part.objects.filter(subject=new_part.subject__id).max()
            new_part.save()


    def get_object(self):
        """Возвращает ссылку на создаваемый объект. Если объект не получается создать, то возвращает None.
        Метод используется для проверки разрешения IsOwner"""

        # Получаем переданные пользователем параметры
        request_data = self.request.data
        # Сохраняем значения создаваемого объекта в переменные
        title = request_data.get("title", None)
        description = request_data.get("description", None)
        content = request_data.get("content", None)
        subject = request_data.get("subject", 0)
        order_id = self.get_new_order_id(subject)
        quest_to_test = request_data.get("quest_to_test", None)
        # Проверяем существование указанного предмета
        try:
            subject = Subject.objects.get(pk=subject)
        except Subject.DoesNotExist:
            return None

        # Создаем или получаем объект раздела предмета
        try:
            part = Part.objects.get(title=title, subject=subject)
        except Part.DoesNotExist:
        # Если объект не найден, то создаем его без сохранения (сохранять не требуется, т.к. в итоге объект удаляется)
            part = Part(title=title, description=description, content=content, subject=subject, order_id=order_id, quest_to_test=quest_to_test)
        return part



class PartListAPIView(generics.ListAPIView):
    """Контроллер для получения списка всех разделов через API.
    Просматривать списки могут любые авторизованные пользователи.
    Для администраторов (is_staff==True) выводятся разделы по всем предметам,
    для остальных пользователей - только разделы предметов, на которые они подписаны или авторами которых являются
    Результат можно фильровать и сортировать с помощью параметров:
     - search=<текст> - ищет текст в полях title, description, content
     - <поле>=<значение> - ищет в <поле> <значение>. В качестве полей можно указать  id, subject (т.е. код предмета), title, description
     - ordering=<поле1>,<поле2>,... - сортирует по перечисленным полям. В качестве полей можно указывать id, subject, title, order_id.
     Пример API-запроса GET: http://127.0.0.1:8000/api/part/?search=проект&subject=1&ordering=subject,order_id
    """
    # serializer_class = PartForStudentSerializer
    # queryset = Part.objects.all()
    permission_classes = [IsAuthenticated]

    # Поиск в результирующем наборе
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["title", "description", 'content', ] # Для SearchFilter
    filterset_fields = ["id", 'subject', "title", "description", ]  # Для DjangoFilterBackend
    ordering_fields = ["id", 'subject', "title", "order_id", ]   # Для OrderingFilter
    def get_queryset(self):
        """Формириует результирующий набор данных"""
        if self.request.user.is_staff:
            # Для администраторов получаем полный набор записей
            return Part.objects.all()
        else:
            # Для остальных пользователей только предметы, на которые они подписаны, либо у которых они являются авторами
            # return Part.objects.filter(Q(subject__access_users__user=self.request.user)|Q(subject__author=self.request.user))
            # return Part.objects.filter(subject__access_users__user=self.request.user)
            return Part.objects.filter(Q(subject__access__user=self.request.user)|Q(subject__author=self.request.user))


    def get_serializer_class(self):
        """Выбирает сериализатор для раздела (в зависимости от роли пользователя)"""
        if self.request.user.is_staff:
            # Для администраторов выводим подробную информацию по разделам
            return PartForAuthorSerializer
        else:
            # Для остальных пользователей только информацию необходимую для обучения
            return PartForStudentSerializer


class PartListMeAPIView(generics.ListAPIView):
    """Контроллер для получения через API списка всех разделов предметов, автором которых является авторизованный пользователь.
    Просматривать списки могут любые авторизованные пользователи.
    Результат можно фильровать и сортировать с помощью параметров:
     - search=<текст> - ищет текст в полях title, description, content
     - <поле>=<значение> - ищет в <поле> <значение>. В качестве полей можно указать  id, subject (т.е. код предмета), title, description
     - ordering=<поле1>,<поле2>,... - сортирует по перечисленным полям. В качестве полей можно указывать id, subject, title, order_id.
    Пример API-запроса GET: http://127.0.0.1:8000/api/part/me/?search=проект&subject=1&ordering=subject,order_id"""
    serializer_class = PartForAuthorSerializer
    # queryset = Subject.objects.filter()
    permission_classes = [IsAuthenticated]

    # Поиск в результирующем наборе
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["title", "description", 'content', ] # Для SearchFilter
    filterset_fields = ["id", 'subject', "title", "description", ]  # Для DjangoFilterBackend
    ordering_fields = ["id", 'subject', "title", "order_id", ]   # Для OrderingFilter

    def get_queryset(self):
        return Part.objects.filter(subject__author=self.request.user)


class  PartRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для получения детальной информации по разделу предмету через API.
    Просматривать детализированные данные по конкретному предмету могут только его авторы, админситраторы и подписанные пользователи.
    Авторы и администраторы также могут видеть настройки для генерации тестов"""
    # serializer_class = SubjectSerializer
    queryset = Part.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser|IsOwner|IsSubscribedUser]

    def get_serializer_class(self):
        """Выбирает сериализатор для раздела (в зависимости от роли пользователя)"""
        if self.request.user.is_staff or self.get_object().subject.author==self.request.user:
            # Для администраторов и авторов выводим подробную информацию по разделам
            return PartForAuthorSerializer
        else:
            # Для остальных пользователей только информацию необходимую для обучения
            return PartForStudentSerializer


class  PartUpdateAPIView(generics.UpdateAPIView, generics.RetrieveUpdateAPIView):
    """Контроллер для обновления информации по разделу предмета через API.
    Обновлять данные по конкретному разделу могут только авторы предмета"""
    serializer_class = PartForAuthorSerializer
    queryset = Part.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class  PartDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления информации по разделу предмета через API.
    Удалять данные по конкретному разделу могут только авторы предмета"""
    queryset = Part.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_destroy(self, instance):
        subject = instance.subject
        order_id = instance.order_id

        # Уменьшаем order_id для всех остальных объектов с тем же subject и большим значением order_id
        Part.objects.filter(subject=subject, order_id__gt=order_id).update(order_id=models.F('order_id') - 1)

        # Удаляем объект instance
        # instance.delete()
        return super().perform_destroy(instance)


