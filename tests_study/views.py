from django.db.models import Min, Max, Avg
from django.shortcuts import render
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from serializers.statistics import SubjectStatisticSerializer, StatisticsSerializer, PartStatisticSerializer, \
    UserStatisticSerializer
from serializers.tests_study import QuestionSerializer, TestSerializer, TestUserResultSerializer, \
    TestUserAnswerSerializer
from study.models import Part, Subject
from study.permissions import IsOwner, IsSubscribedUser, IsSelfTestUser
from tests_study.models import Question, Test, QuestionTest, AnswerTest
from tests_study.services import generate_test, check_test
from users.models import User


# Create your views here.
###### Question APIView
class QuestionCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания вопросов с вариантами ответов через API.
    Создавать вопросы могут автор предмета и администратор.
    Варианты ответов можно передавать в виде стандартного словаря answer или в виде списка строк через запятую answers_input.
    Для второго варианта перед верным вариантом ответа ставится восклицательный знак.
    Пример для первого варианта "answers":
    [ {"title": "ответ1", "correct": false}, {"title": "правильный ответ", "correct": True},...]
    answers_input["ответ1", "ответ2", "!правильный ответ"]
    Пример API-запроса POST: http://127.0.0.1:8000/api/tests/question/create/"""
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsOwner|IsAdminUser]

    def get_object(self):
        """Возвращает ссылку на создаваемый объект. Если объект не получается создать, то возвращает None.
        Метод используется для проверки разрешения IsOwner"""

        # Получаем переданные пользователем параметры
        request_data = self.request.data
        # Сохраняем значения создаваемого объекта в переменные
        title = request_data.get("title", None)
        difficulty = request_data.get("difficulty", None)
        part = request_data.get("part", None)
        # Проверяем существование указанного раздела предмета
        try:
            part = Part.objects.get(pk=part)
        except Part.DoesNotExist:
            return None

        # Создаем или получаем вопрос раздела
        try:
            question = Question.objects.get(title=title, part=part)
        except Question.DoesNotExist:
        # Если объект не найден, то создаем его
            question = Question(title=title, difficulty=difficulty, part=part)
        return question


class  QuestionUpdateAPIView(generics.UpdateAPIView, generics.RetrieveUpdateAPIView):
    """Контроллер для обновления информации по вопросам с вариантами ответов для тестирования через API.
    Обновлять данные могут только авторы предмета и администраторы"""
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = [IsAuthenticated, IsOwner|IsAdminUser]


class  QuestionDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления информации по вопросам с вариантами ответов для тестирования через API.
    Удалять данные могут только авторы предмета и администраторы"""
    queryset = Question.objects.all()
    permission_classes = [IsAuthenticated, IsOwner|IsAdminUser]


class TestGeneratePartView(APIView):
    """Контроллер генерации теста для промежуточного тестирования по разделу через API.
    Пример API-запроса POST: http://127.0.0.1:8000/api/tests/create/part/<part_id>"""

    permission_classes = [IsAuthenticated, IsAdminUser | IsOwner | IsSubscribedUser]
    type_test = Test.TYPE_INTERMEDIATE

    def post(self, request, parent_id):
        """Генерирует тест для post-запроса и возвращает результат"""
        # Определяем параметры теста
        user = request.user

        # Перед егенрацией теста проверяем не нарушаются разрешения
        test = self.get_object()
        self.check_object_permissions(self.request, test)


        # Вызов функции для генерации промежуточного теста
        test = generate_test(user=user.pk, type=self.type_test, parent_id=parent_id)

        # Использование сериализатора для преобразования объекта в данные
        serializer = TestSerializer(test)
        # Проверка валидности данных
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get_object(self):
        """Возвращает ссылку на созданный объект test. Если объект не может быть создан, то возвращает None.
        Метод используется для проверки разрешения IsOwner"""
        user = self.request.user
        parent_id = self.kwargs.get("parent_id")
        if self.type_test == Test.TYPE_INTERMEDIATE:
            test=Test(user=user, type=self.type_test, part_id=parent_id)
        else:
            test=Test(user=user, type=self.type_test, subject_id=parent_id)

        print("test in get_object =",test)
        print("test.__dict__ =", test.__dict__)

        return test


class TestGenerateSubjectView(TestGeneratePartView):
    """Контроллер генерации теста для итогового тестирования по предмету через API.
    Основной код наследуется от класса TestGeneratePartView
    Пример API-запроса POST: http://127.0.0.1:8000/api/tests/create/subject/<subject_id>"""

    permission_classes = [IsAuthenticated, IsAdminUser | IsOwner | IsSubscribedUser]
    type_test = Test.TYPE_FINAL



class  TestAnswerViewUpdateAPIView(generics.UpdateAPIView, generics.RetrieveUpdateAPIView):
    """Контроллер для ввода ответов пользователя на вопросы теста и вывода резульатов через API.
    От пользователя данные принимаем в формате:
    [{"pk_question": pk_question, "pk_answer": pk_answer}, {...}, ...]
    Пример API-запроса PATCH: http://127.0.0.1:8000/api/tests/<pk_test>/answer/"""

    serializer_class = TestUserResultSerializer
    queryset = Test.objects.all()
    permission_classes = [IsAuthenticated, IsSelfTestUser]


    def partial_update(self, request, *args, **kwargs):

        # Получаем объект Test, исходя из переданного test_id
        test = self.get_object()

        # Получаем данные от пользователя по ответам на вопросы в формате [{"pk_question": pk_question, "pk_answer": pk_answer}, {...}, ...]
        user_answers = request.data
        try:
            # Пытаемся в цикле сохранить полученные данные
            for user_answer in user_answers:
                pk_question = user_answer['pk_question']
                pk_answer_test = user_answer['pk_answer']
                pk_answer = AnswerTest.objects.get(pk=pk_answer_test).answer_id

                # Обновляем запись в модели QuestionTest user_answer для pk=pk_question
                question_test = QuestionTest.objects.get(pk=pk_question)
                question_test.user_answer_id = pk_answer
                question_test.save()

            # Вычисляем пезультат
            check_test(test)
            # Вычисляем и выводим результат
            test.refresh_from_db()
            serializer = self.get_serializer(test)
            test_result=serializer.data
            test_result['user_answer'] = TestUserAnswerSerializer(QuestionTest.objects.filter(test_id=test.pk), many=True).data
            print("serializer.data['user_answer']", serializer.data.__dict__)
            return Response(test_result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


### Статистика с результатами тестирования студентов
class SubjectStatListAPIView(generics.ListAPIView):
    """Контроллер для вывода стастики с итогами тестирования по предметам через API.
    Просматривать списки могут любые авторизованные пользователи.
    Админимтартор будет видеть статистику по всем предметам, автор - по своим
    Результат можно фильровать и сортировать с помощью параметров:
     - search=<текст> - ищет текст в поле title
     - <поле>=<значение> - ищет в <поле> <значение>. В качестве полей можно указать  id (код предмета), title (название предмета)
     - ordering=<поле1>,<поле2>,... - сортирует по перечисленным полям. В качестве полей можно указывать id, title.
     Пример API-запроса GET: http://127.0.0.1:8000/api/tests/statistics/subject/?search=теория&id=1&ordering=title
    """
    serializer_class = SubjectStatisticSerializer

    permission_classes = [IsAuthenticated]

    # Поиск в результирующем наборе
    # filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    # search_fields = ["title",] # Для SearchFilter
    # filterset_fields = ["id", "title", ]  # Для DjangoFilterBackend
    # ordering_fields = ["id", "title",]   # Для OrderingFilter

    def get_queryset(self):
        """Для администраторов возвращает все предметы, а для остальных пользоватлей - только предметы, принадлежащие пользователю"""
        if self.request.user.is_staff:
            queryset = Subject.objects.all()
        else:
            queryset = Subject.objects.filter(author=self.request.user)

        # Дополняем полученные данные статистикой по результатам тестирования
        for subject in queryset:
            tests_count = subject.test.count()
            min_ball = subject.test.aggregate(Min("ball")).get("ball__min",0)
            max_ball = subject.test.aggregate(Max("ball")).get("ball__max",0)
            avg_ball = subject.test.aggregate(Avg("ball")).get("ball__avg",0)

            statistics_serializer = StatisticsSerializer(data={
                'tests_count': tests_count,
                'min_ball': min_ball if max_ball else 0,
                'max_ball': max_ball if min_ball else 0,
                'avg_ball': avg_ball if avg_ball else 0,
            })
            statistics_serializer.is_valid(raise_exception=True)

            subject.statistics = statistics_serializer.data

        return queryset


class PartStatListAPIView(generics.ListAPIView):
    """Контроллер для вывода стастики с итогами тестирования по разделам через API.
    Просматривать списки могут любые авторизованные пользователи.
    Админимтартор будет видеть статистику по всем разделам, автор - по своим
    Результат можно фильровать и сортировать с помощью параметров:
     - search=<текст> - ищет текст в поле title
     - <поле>=<значение> - ищет в <поле> <значение>. В качестве полей можно указать  id (код раздела), title (название раздела)
     - ordering=<поле1>,<поле2>,... - сортирует по перечисленным полям. В качестве полей можно указывать id, title.
     Пример API-запроса GET: http://127.0.0.1:8000/api/tests/statistics/part/?search=теория&id=1&ordering=title
    """
    serializer_class = PartStatisticSerializer
    permission_classes = [IsAuthenticated]

    # Поиск в результирующем наборе
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["title",] # Для SearchFilter
    filterset_fields = ["id", "title", ]  # Для DjangoFilterBackend
    ordering_fields = ["id", "title",]   # Для OrderingFilter

    def get_queryset(self):
        """Для администраторов возвращает все предметы, а для остальных пользоватлей - только предметы, принадлежащие пользователю"""

        if self.request.user.is_staff:
            # Для администраторов получаем полный набор записей
            queryset =  Part.objects.all()
        else:
            # Для остальных пользователей только разделы, на которые они подписаны, либо у которых они являются авторами
            queryset =  Part.objects.filter(subject__author=self.request.user)

        # Дополняем полученные данные статистикой по результатам тестирования
        for part in queryset:
            tests_count = part.test.count()
            min_ball = part.test.aggregate(Min("ball")).get("ball__min",0)
            max_ball = part.test.aggregate(Max("ball")).get("ball__max",0)
            avg_ball = part.test.aggregate(Avg("ball")).get("ball__avg",0)

            statistics_serializer = StatisticsSerializer(data={
                'tests_count': tests_count,
                'min_ball': min_ball if max_ball else 0,
                'max_ball': max_ball if min_ball else 0,
                'avg_ball': avg_ball if avg_ball else 0,
            })
            statistics_serializer.is_valid(raise_exception=True)

            part.statistics = statistics_serializer.data

        return queryset


class UserStatListAPIView(generics.ListAPIView):
    """Контроллер для вывода стастики с итогами тестирования студентов через API.
    Просматривать списки могут любые авторизованные пользователи.
    Админимтартор будет видеть статистику по всем разделам, автор - по своим
    Результат можно фильровать и сортировать с помощью параметров:
     - search=<текст> - ищет текст в поле title
     - <поле>=<значение> - ищет в <поле> <значение>. В качестве полей можно указать  id (код пользователя), email (почта пользователя)
     - ordering=<поле1>,<поле2>,... - сортирует по перечисленным полям. В качестве полей можно указывать id, email.
     Пример API-запроса GET: http://127.0.0.1:8000/api/tests/statistics/user/?search=Ивановя&id=1&ordering=email
    """
    serializer_class = UserStatisticSerializer
    permission_classes = [IsAuthenticated]

    # Поиск в результирующем наборе
    # filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    # search_fields = ["title",] # Для SearchFilter
    # filterset_fields = ["id", "title", ]  # Для DjangoFilterBackend
    # ordering_fields = ["id", "title",]   # Для OrderingFilter

    def get_queryset(self):
        """Для администраторов возвращает все пользователи,
        а для остальных пользоватлей - только студенты, которые проходили тестирование по предметам, автором которых является пользователь"""

        if self.request.user.is_staff:
            # Для администраторов получаем полный набор записей
            queryset =  User.objects.all()
        else:
            # Для остальных пользователей только предметы, на которые они подписаны, либо у которых они являются авторами
            queryset =  User.objects.filter(test__subject__author=self.request.user)

        # Дополняем полученные данные статистикой по результатам тестирования
        for user in queryset:
            tests_count = user.test.count()
            min_ball = user.test.aggregate(Min("ball")).get("ball__min",0)
            max_ball = user.test.aggregate(Max("ball")).get("ball__max",0)
            avg_ball = user.test.aggregate(Avg("ball")).get("ball__avg",0)

            statistics_serializer = StatisticsSerializer(data={
                'tests_count': tests_count,
                'min_ball': min_ball if max_ball else 0,
                'max_ball': max_ball if min_ball else 0,
                'avg_ball': avg_ball if avg_ball else 0,
            })
            statistics_serializer.is_valid(raise_exception=True)

            user.statistics = statistics_serializer.data

        return queryset