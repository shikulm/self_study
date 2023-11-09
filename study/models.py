from django.db import models
from users.models import NULLABLE, NOT_NULLABLE, User


class Subject(models.Model):
    """
    Модель для описания предметов
    """
    title = models.CharField(verbose_name='Предмет', max_length=200, help_text="Предмет", **NOT_NULLABLE)
    description = models.TextField(verbose_name='Описание', help_text="Описание", **NULLABLE)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='автор', **NULLABLE, related_name='subject', help_text='Автор')
    access_users = models.ManyToManyField(User, through='AccessSubjectGroup', related_name='accessible_subjects')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['title',]


class AccessSubjectGroup(models.Model):
    """
    Модель списка пользователей, имеющих доступ к изучению дисциплины
    """
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, verbose_name='предмет', **NOT_NULLABLE, related_name='access', help_text='Предмет')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='студент', **NOT_NULLABLE, related_name='access', help_text='студент')


    def __str__(self):
        return f'{self.subject} - {self.user}'


    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['subject', 'user']
        unique_together = ('subject', 'user',)


class Part(models.Model):
    """
    Модель с разделами предмета
    """
    title = models.CharField(verbose_name='Раздел', max_length=200, help_text="Раздел", **NOT_NULLABLE, unique=True)
    description = models.TextField(verbose_name='Описание', help_text="Описание", **NULLABLE)
    content = models.TextField(verbose_name='Материалы', help_text="Материалы", **NULLABLE)
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, verbose_name='предмет', **NOT_NULLABLE,
                                related_name='part', help_text='Предмет')
    order_id = models.PositiveIntegerField(verbose_name='Порядковый номер', help_text="Порядковый номер", **NULLABLE)
    date_create =  models.DateTimeField(auto_now_add=True, verbose_name='дата добавления раздела', **NULLABLE)
    last_update = models.DateTimeField(auto_now=True, verbose_name='дата обновления раздела', **NULLABLE)
    quest_to_test = models.PositiveIntegerField(verbose_name='Вопросов в тест', help_text="Количество вопросов включаемых в тест", default=0, **NULLABLE)

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Раздел предмета'
        verbose_name_plural = 'Разделы предмета'
        ordering = ['subject', 'order_id']



class UsefulLink(models.Model):
    """
    Модель списка полезных ссыок на дополнительные материалы по разделу
    """
    title = models.CharField(verbose_name='Название источника', max_length=200, help_text="Название источника дополнительных материалов по разделу", **NOT_NULLABLE, unique=True)
    url_link = models.URLField(verbose_name='URL', help_text='URL к дополнительными материалами', **NULLABLE)
    description = models.TextField(verbose_name='Описание', help_text="Описание", **NULLABLE)
    part = models.ForeignKey(to=Part, on_delete=models.CASCADE, verbose_name='Раздел', **NULLABLE, related_name='links', help_text='Раздел')

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Ссылка на дополнительные материалы'
        verbose_name_plural = 'Ссылки на дополнительные материалы'




