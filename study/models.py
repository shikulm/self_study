from django.db import models
from users.models import NULLABLE, NOT_NULLABLE, User

# Create your models here.
class Subject(models.Model):
    title = models.CharField(verbose_name='Предмет', max_length=200, help_text="Предмет", **NOT_NULLABLE)
    description = models.TextField(verbose_name='Описание', help_text="Описание", **NULLABLE)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='автор', **NULLABLE, related_name='subject', help_text='Автор')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['title',]


class AccessGroup(models.Model):
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, verbose_name='предмет', **NOT_NULLABLE, related_name='access', help_text='Предмет')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='студент', **NOT_NULLABLE, related_name='access', help_text='студент')


    def __str__(self):
        return f'{self.subject} - {self.user}'


    class Meta:
        verbose_name = 'Подписанный пользователь'
        verbose_name_plural = 'Подписанные пользователи'
        ordering = ['subject', 'user']
        unique_together = ('subject', 'user',)


class Part(models.Model):
    title = models.CharField(verbose_name='Раздел', max_length=200, help_text="Раздел", **NOT_NULLABLE)
    description = models.TextField(verbose_name='Описание', help_text="Описание", **NULLABLE)
    content = models.TextField(verbose_name='Материалы', help_text="Материалы", **NULLABLE)
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, verbose_name='предмет', **NOT_NULLABLE,
                                related_name='part', help_text='Предмет')
    order_id = models.PositiveIntegerField(verbose_name='Порядковый номер', help_text="Порядковый номер", **NULLABLE)
    date_add =  models.DateTimeField(auto_now_add=True, verbose_name='дата добавления раздела', **NULLABLE)
    last_update = models.DateTimeField(auto_now=True, verbose_name='дата обновления раздела', **NULLABLE)
    quest_to_test = models.PositiveIntegerField(verbose_name='Вопросов в тест', help_text="Количество вопросов включаемых в тест", default=0, **NULLABLE)


