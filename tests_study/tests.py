from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from study.models import Subject, Part
from tests_study.models import Question, Answer, Test, QuestionTest, AnswerTest
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


class GenerateTestCase(APITestCase):
    """Тестирование генерации тестов"""

    def setUp(self) -> None:
        self.user = User.objects.create(email='test@mail.ru', is_staff=True, is_superuser=True)
        self.client.force_authenticate(self.user)
        self.subject = Subject.objects.create(title='test_subj', author=self.user)

        self.part1 = Part.objects.create(title='test_part1', subject=self.subject, order_id=1, quest_to_test=2)
        self.p1q1 = Question.objects.create(title='test_p1q1', difficulty=1, part=self.part1)
        self.p1q1a1 = Answer.objects.create(title='p1q1a1', correct=True, question=self.p1q1)
        self.p1q1a2 = Answer.objects.create(title='p1q1a2', correct=False, question=self.p1q1)
        self.p1q2 = Question.objects.create(title='test_p1q2', difficulty=1, part=self.part1)
        self.p1q2a1 = Answer.objects.create(title='p1q2a1', correct=True, question=self.p1q2)
        self.p1q2a2 = Answer.objects.create(title='p1q2a2', correct=False, question=self.p1q2)
        self.p1q3 = Question.objects.create(title='test_p1q3', difficulty=1, part=self.part1)
        self.p1q3a1 = Answer.objects.create(title='p1q3a1', correct=True, question=self.p1q3)
        self.p1q3a2 = Answer.objects.create(title='p1q3a2', correct=False, question=self.p1q3)

        self.part2 = Part.objects.create(title='test_part2', subject=self.subject, order_id=2, quest_to_test=5)
        self.p2q1 = Question.objects.create(title='test_p2q1', difficulty=1, part=self.part2)
        self.p2q1a1 = Answer.objects.create(title='p2q1a1', correct=True, question=self.p2q1)
        self.p2q1a2 = Answer.objects.create(title='p2q1a2', correct=False, question=self.p2q1)
        self.p2q2 = Question.objects.create(title='test_p2q2', difficulty=1, part=self.part2)
        self.p2q2a1 = Answer.objects.create(title='p2q2a1', correct=True, question=self.p2q2)
        self.p2q2a2 = Answer.objects.create(title='p2q2a2', correct=False, question=self.p2q2)

    def test_generate_inter(self):
        """Тестирование генерации промежуточного теста по разделу"""
        # data = {"title": 'test_q2', 'part': self.part.pk, 'difficulty': 1, "answers_input": ["!a1", "a2", "a3", "a4"]}
        response = self.client.post(reverse('tests_study:test-part-create', args=[self.part1.pk]))
        # print("response.json()", response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        #  Проверка корректности данных
        # Создание теста
        self.assertEquals(Test.objects.all().count(), 1)
        self.assertEquals(response.json().get("type"), "Промежуточный")
        #  Создание вопросов теста
        self.assertEquals(QuestionTest.objects.all().count(), 2)

    def test_generate_inter(self):
        """Тестирование генерации итогового теста по предмету"""
        # data = {"title": 'test_q2', 'part': self.part.pk, 'difficulty': 1, "answers_input": ["!a1", "a2", "a3", "a4"]}
        response = self.client.post(reverse('tests_study:test-subject-create', args=[self.subject.pk]))
        # print("response.json()", response.json())
        # Проверяем статус вывода списка
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        #  Проверка корректности данных
        # Создание теста
        self.assertEquals(Test.objects.all().count(), 1)
        self.assertEquals(response.json().get("type"), "Итоговый")
        #  Создание вопросов теста
        self.assertEquals(QuestionTest.objects.all().count(), 4)


class UserAnswerForTestCase(APITestCase):
    """Тестирование сохранения ответов пользователя на вопросы теста и проверки резульатов"""

    def setUp(self) -> None:
        self.user = User.objects.create(email='test@mail.ru', is_staff=True, is_superuser=True)
        self.client.force_authenticate(self.user)
        self.subject = Subject.objects.create(title='test_subj', author=self.user)

        self.part1 = Part.objects.create(title='test_part1', subject=self.subject, order_id=1, quest_to_test=1)
        self.p1q1 = Question.objects.create(title='test_p1q1', difficulty=3, part=self.part1)
        self.p1q1a1 = Answer.objects.create(title='p1q1a1', correct=True, question=self.p1q1)
        self.p1q1a2 = Answer.objects.create(title='p1q1a2', correct=False, question=self.p1q1)
        # self.p1q2 = Question.objects.create(title='test_p1q2', difficulty=1, part=self.part1)
        # self.p1q2a1 = Answer.objects.create(title='p1q2a1', correct=True, question=self.p1q2)
        # self.p1q2a2 = Answer.objects.create(title='p1q2a2', correct=False, question=self.p1q2)
        # self.p1q3 = Question.objects.create(title='test_p1q3', difficulty=1, part=self.part1)
        # self.p1q3a1 = Answer.objects.create(title='p1q3a1', correct=True, question=self.p1q3)
        # self.p1q3a2 = Answer.objects.create(title='p1q3a2', correct=False, question=self.p1q3)

        self.part2 = Part.objects.create(title='test_part2', subject=self.subject, order_id=2, quest_to_test=1)
        self.p2q1 = Question.objects.create(title='test_p2q1', difficulty=2, part=self.part2)
        self.p2q1a1 = Answer.objects.create(title='p2q1a1', correct=True, question=self.p2q1)
        self.p2q1a2 = Answer.objects.create(title='p2q1a2', correct=False, question=self.p2q1)
        # self.p2q2 = Question.objects.create(title='test_p2q2', difficulty=1, part=self.part2)
        # self.p2q2a1 = Answer.objects.create(title='p2q2a1', correct=True, question=self.p2q2)
        # self.p2q2a2 = Answer.objects.create(title='p2q2a2', correct=False, question=self.p2q2)

        #  Генерируем тест из двух вопрсов (по 1 на раздел) и получаем ссылку на созданный тест
        response = self.client.post(reverse('tests_study:test-subject-create', args=[self.subject.pk]))
        pk_test = response.json().get("pk_test")
        self.test = Test.objects.get(pk=pk_test)
        # Получаем коды вопросов из QuestionTest и коды ответов на них из AnswerTest для отправки ответов пользователем
        self.question_test1 = QuestionTest.objects.get(question=self.p1q1)
        print("self.question_test1 = ", self.question_test1)
        self.question_test2 = QuestionTest.objects.get(question=self.p2q1)
        self.answer_test1 = AnswerTest.objects.get(answer=self.p1q1a1) # Для первого вопроса выбираем правильный ответ
        self.answer_test2 = AnswerTest.objects.get(answer=self.p2q1a2) # Для второго вопроса выбираем неправильный ответ


    def test_user_answer(self):
        """Тестирование сохранения и проверки пользовательских ответов на вопросы теста"""

        data = [{"pk_question": self.question_test1.pk, "pk_answer":self.answer_test1.pk},
                {"pk_question": self.question_test2.pk, "pk_answer":self.answer_test2.pk}]
        response = self.client.patch(reverse('tests_study:test-user_answer-update', args=[self.test.pk]), data, format='json')


        # Прверяем статус обновления
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        # Проверяем правильность сохранения данных
        self.assertEquals(response.json().get("user_answer")[0].get("pk_question"), self.question_test1.pk)
        self.assertEquals(response.json().get("user_answer")[0].get("user_answer"), self.p1q1a1.title)
        self.assertEquals(response.json().get("user_answer")[1].get("pk_question"), self.question_test2.pk)
        self.assertEquals(response.json().get("user_answer")[1].get("user_answer"), self.p2q1a2.title)

        # Проверяем правильность проверки ответов пользователя
        self.assertEquals(response.json().get("user_answer")[0].get("result"), True)
        self.assertEquals(response.json().get("user_answer")[1].get("result"), False)

        # Проверяем правильность вычисления балла студента
        self.test.refresh_from_db()
        #  С учетом сложности вопросов должен быть балл 60
        self.assertEquals(self.test.ball, 60)
