from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import UserManager

NULLABLE = {'blank': True, 'null': True}
NOT_NULLABLE = {'blank': False, 'null': False}

# Create your models here.
class User(AbstractUser):
    """Хранит данные о пользователях"""
    objects = UserManager()

    username = None
    email = models.EmailField(max_length=150, verbose_name='Email', **NOT_NULLABLE, unique=True, help_text="Эл. почта. Нужна для верификации")
    first_name = models.CharField(verbose_name='Имя', max_length=150, blank=True, help_text="Имя")
    last_name = models.CharField(verbose_name='Фамилия', max_length=150, blank=True, help_text="Фамилия")
    # phone = models.CharField(max_length=50, verbose_name='телефон', **NULLABLE, help_text="Телефон")
    # city = models.CharField(max_length=150, verbose_name='город', **NULLABLE, help_text="Город")
    avatar = models.ImageField(upload_to='users/', verbose_name='аватарка', **NULLABLE, help_text="Аватарка")


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        """Выводит информацию о пользоавтеле при печати (email)"""
        return f"{self.last_name} {self.first_name} {self.email}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('email',)