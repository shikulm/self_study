from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from study.models import Subject, Part
from tests_study.models import Question, Answer
from users.models import User


# Create your tests here.

class QuestionTestCase(APITestCase):
    """Тестирование CRUD вопросов по разделу с вариантами ответов"""

    def setUp(self) -> None:
        self.user = User.objects.create(email='test@mail.ru', is_staff=True, is_superuser=True)
        self.client.force_authenticate(self.user)
        self.subject = Subject.objects.create(title='test_subj', author=self.user)
        self.part = Part.objects.create(title='test_part', subject=self.subject, order_id=1)
        self.question = Question.objects.create(title='test_q1', difficulty=1, part=self.part)
        self.answer1 = Answer.objects.create(title='answer1', correct=True, question=self.question)
        self.answer2 = Answer.objects.create(title='answer2', correct=False, question=self.question)

    def test_create_question(self):
        """Тестировние создания вопросов по разделу с вариантами ответов"""
        data = {"title": 'test_q2', 'part': self.part.pk, 'difficulty': 1, "answers_input": ["!a1", "a2", "a3", "a4"]}
        response = self.client.post(reverse('tests_study:question-create'), data)
        # print("response.json()", response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        #  Проверка корректности данных
        self.assertEquals(Question.objects.all().count(), 2)
        self.assertEquals(response.json().get("title"), "test_q2")
        self.assertEquals(Answer.objects.filter(question_id=response.json().get("pk")).count(), 4)
        self.assertEquals(response.json().get("answers")[0].get('title'), "a1")
        self.assertEquals(response.json().get("answers")[0].get('correct'), True)
        self.assertEquals(response.json().get("answers")[1].get('title'), "a2")
        self.assertEquals(response.json().get("answers")[1].get('correct'), False)


    def test_update_question(self):
        """Тестировние обновления вопросов по разделу с вариантами ответов"""
        data = {"title": 'test_q2', 'part': self.part.pk, 'difficulty': 1, "answers_input": ["!a1", "a2", "a3", "a4"]}
        response = self.client.patch(reverse('tests_study:question-update', args=[self.question.pk]), data)
        # print(response.json())
        # Прверяем статус обновления
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # Проверка изменения значений
        self.assertEquals(response.json().get("title"), "test_q2")
        self.assertEquals(Answer.objects.filter(question_id=response.json().get("pk")).count(), 4)
        self.assertEquals(response.json().get("answers")[0].get('title'), "a1")
        self.assertEquals(response.json().get("answers")[0].get('correct'), True)
        self.assertEquals(response.json().get("answers")[1].get('title'), "a2")
        self.assertEquals(response.json().get("answers")[1].get('correct'), False)


    def test_delete_question(self):
        """Тестировние удаления вопросов по разделу"""
        response = self.client.delete(reverse('tests_study:question-delete', args=[self.question.pk]))
        # print("response.json()=", response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        #  Проверка корректности данных
        self.assertEquals(Question.objects.all().count(), 0)