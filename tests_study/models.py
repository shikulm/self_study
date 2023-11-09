from django.db import models
from users.models import NULLABLE, NOT_NULLABLE, User
from study.models import Part, Subject
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Question(models.Model):
    """
    Модель c вопросами для тестирования по разделу
    """
    title = models.TextField(verbose_name='Вопрос', help_text="Вопрос", **NOT_NULLABLE)
    difficulty = models.PositiveIntegerField(verbose_name='Сложность вопроса', help_text="Сложность вопроса от 1 до 5 (по умолчанию 1)",
                                             default=1, **NOT_NULLABLE, validators=[MaxValueValidator(5), MinValueValidator(1)])
    part = models.ForeignKey(to=Part, on_delete=models.CASCADE, verbose_name='Раздел', **NULLABLE, related_name='questions', help_text='Раздел')

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Вопрос теста по разделу'
        verbose_name_plural = 'Вопросы тестов по разделам предмета'
        ordering = ['title',]


class Answer(models.Model):
    """
    Модель c вараинтами ответов на вопросы для тестирования
    """
    title = models.TextField(verbose_name='Ответ', help_text="Вариант ответа", **NOT_NULLABLE)
    correct = models.BooleanField(verbose_name='Правильный?', help_text="Признак правильного ответа", **NOT_NULLABLE, default=False)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE, verbose_name='Вариант ответа', **NULLABLE,
                                 related_name='answers', help_text='Вариант ответа')


    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Вариант ответа на вопрос теста'
        verbose_name_plural = 'Варианты ответов на вопросы теста'



class Test(models.Model):
    """
    Модель c тестами студента. Может содержать результаты промежуточного (по разделу) и итогового (по предмету) теста
    """
    TYPE_INTERMEDIATE = 'inter'
    TYPE_FINAL = 'final'
    TYPE = ((TYPE_INTERMEDIATE, 'Промежуточный'),(TYPE_FINAL, 'Итоговый'))

    type = models.CharField(max_length=50, verbose_name='тип теста', help_text='тип теста (промежуточный/итоговый)', choices=TYPE, default=TYPE_INTERMEDIATE,
                              **NOT_NULLABLE)
    part = models.ForeignKey(to=Part, on_delete=models.CASCADE, verbose_name='Раздел', **NULLABLE, related_name='test', help_text='Раздел')
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, verbose_name='Предмет', **NULLABLE, related_name='test', help_text='Предмет')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='студент', **NOT_NULLABLE, related_name='test', help_text='студент')
    ball = models.FloatField(verbose_name='Балл', **NULLABLE, help_text='Балл', default=0)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='дата и время тестирования', **NULLABLE)

    def __str__(self):
        about = self.part if self.type == self.TYPE_INTERMEDIATE else self.subject
        return f'{self.user} - {about} ({self.type}): {self.ball}'


    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        ordering = ['-date_create',]


class QuestionTest(models.Model):
    """
    Модель c вопросами теста и выбранными студентом ответами
    """
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE, verbose_name='Вопрос', **NOT_NULLABLE, related_name='questions_test', help_text='Вопрос')
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE, verbose_name='Тест', **NOT_NULLABLE, related_name='questions_test', help_text='Тест')
    user_answer = models.ForeignKey(to=Answer, on_delete=models.SET_NULL, verbose_name='Выбранный ответ', **NULLABLE, related_name='questions_test', help_text='Выбранный студентом ответ')
    order_id = models.PositiveIntegerField(verbose_name='Номер вопроса', help_text="Порядковый номер вопроса в тесте", **NULLABLE)
    isCorrect = models.BooleanField(verbose_name='Признак правильного ответа', help_text="Признак правильного ответа (True - правильный, False - неправильный)", default=False, **NULLABLE)


    def __str__(self):
        return f'{self.test} - {self.question}'


    class Meta:
        verbose_name = 'Вопрос теста'
        verbose_name_plural = 'Вопросы и результаты теста'
        ordering = ['test', 'order_id']


class AnswerTest(models.Model):
    """
    Модель c вариантами ответов на вопросы, добавленные в тест конкретного студенто
    """
    question_test = models.ForeignKey(to=QuestionTest, on_delete=models.CASCADE, verbose_name='Вопрос', **NOT_NULLABLE, related_name='answers_test', help_text='Вопрос теста')
    answer = models.ForeignKey(to=Answer, on_delete=models.CASCADE, verbose_name='Ответ', **NOT_NULLABLE, related_name='answer_test', help_text='Вариант ответа')
    order_id = models.PositiveIntegerField(verbose_name='Номер ответа', help_text="Порядковый номер ответа в тесте", **NULLABLE)


    def __str__(self):
        return f'{self.question_test} - {self.answer}'


    class Meta:
        verbose_name = 'Вариант ответа теста'
        verbose_name_plural = 'Варианты ответа теста'
        ordering = ['question_test', 'order_id']