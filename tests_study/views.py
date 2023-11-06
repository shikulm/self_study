from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from serializers.tests_study import QuestionSerializer
from study.models import Part
from study.permissions import IsOwner
from tests_study.models import Question


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