from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

##### Subject test
from study.models import Subject, AccessSubjectGroup, Part, UsefulLink
from users.models import User


class SubjectTestCase(APITestCase):
    """Тестирование CRUD предметов"""

    def setUp(self) -> None:
        self.user = User.objects.create(email='test@mail.ru', is_staff=True, is_superuser=True)
        self.client.force_authenticate(self.user)
        self.subject = Subject.objects.create(title='test', author=self.user)

    def test_list_subject(self):
        """Тестировние вывода списка предметов"""
        response = self.client.get(reverse('study:subject-list'))
        # print(response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_200_OK)
        #  Проверка корректности данных
        self.assertEquals(response.json().get('results')[0].get('title'), self.subject.title)

    def test_list_me_subject(self):
        """Тестировние вывода списка предметов"""
        response = self.client.get(reverse('study:subject-list-me'))
        # print(response.json())
        # Проверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_200_OK)
        #  Проверка корректности данных
        self.assertEquals(response.json().get('results')[0].get('title'), self.subject.title)

    def test_retrive_subject(self):
        """Тестировние вывода детальных данных по отдельному предмету"""
        response = self.client.get(reverse('study:subject-detail', args=[self.subject.pk]))
        # print(response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_200_OK)
        #  Проверка корректности данных
        self.assertEquals(response.json().get('title'), self.subject.title)
        self.assertEquals(response.json().get('author').get('pk'), self.user.pk)

    def test_create_subject(self):
        """Тестировние создания предмета"""
        data = {"title": 'test2'}
        response = self.client.post(reverse('study:subject-create'), data)
        # print(response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_201_CREATED)
        #  Проверка корректности данных
        self.assertEquals(Subject.objects.all().count(), 2)

        # Проверка подставновки по умолчанию текущего пользователя
        self.assertEquals(response.json().get('author').get('pk'), self.user.pk)

    def test_update_subject(self):
        """Тестировние обновления предмета"""
        data = {"title": 'test3'}
        response = self.client.patch(reverse('study:subject-update', args=[self.subject.pk]), data)
        # print(response.json())
        # Прверяем статус обновления
        self.assertEquals(response.status_code,
                          status.HTTP_200_OK)

        # Проверка изменения значения в поле с названием
        self.assertEquals(response.json().get("title"), "test3")

    def test_delete_subject(self):
        """Тестировние удаления предмета"""
        response = self.client.delete(reverse('study:subject-delete', args=[self.subject.pk]))
        # print(response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code,
                          status.HTTP_204_NO_CONTENT)
        #  Проверка корректности данных
        self.assertEquals(Subject.objects.all().count(), 0)


class AccessSubjectGroupTestCase(APITestCase):
    """Тестирование CRUD списка пользователей, имеющих доступ к предмету (модель AccessSubjectGroup)"""

    def setUp(self) -> None:
        self.user1 = User.objects.create(email='test1@mail.ru', is_staff=True, is_superuser=True)
        self.user2 = User.objects.create(email='test2@mail.ru', is_staff=False, is_superuser=False)
        self.client.force_authenticate(self.user1)
        self.subject = Subject.objects.create(title='test', author=self.user1)

    def test_access_user_subject(self):
        """Тестировние предоставление и запрета доступа к предмету"""
        # Предоставление доступа пользователю user2
        response = self.client.post(reverse('study:subject-grantuser', args=[self.subject.pk, self.user2.pk]))
        # print(response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        #  Проверка корректности данных
        self.assertEquals(response.json().get("user").get("pk"), self.user2.pk)

        # Проверка запрета доступа
        response = self.client.delete(reverse('study:subject-denyuser', args=[self.subject.pk, self.user2.pk]))
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        #  Проверка корректности данных
        self.assertEquals(AccessSubjectGroup.objects.filter(subject_id=self.subject.pk, user_id=self.user2.pk).count(),
                          0)

    def test_subject_access_list(self):
        """Тестировние вывода списка подписанных на предмет пользователей"""
        # Предоставление доступа пользователю user2
        response = self.client.post(reverse('study:subject-grantuser', args=[self.subject.pk, self.user2.pk]))
        # Получение списка пользователей с правами доступа
        response = self.client.get(reverse('study:subject-access-list'))
        # print(response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        #  Проверка корректности данных
        self.assertEquals(response.json().get('results')[0].get('access_users')[0].get('pk'), self.user2.pk)


class PartTestCase(APITestCase):
    """Тестирование CRUD предметов"""

    def setUp(self) -> None:
        self.user = User.objects.create(email='test@mail.ru', is_staff=True, is_superuser=True)
        self.client.force_authenticate(self.user)
        self.subject = Subject.objects.create(title='test', author=self.user)
        self.part = Part.objects.create(title='test', subject=self.subject, order_id=1)

    def test_list_part(self):
        """Тестировние вывода списка предметов"""
        response = self.client.get(reverse('study:part-list'))
        # print(response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        #  Проверка корректности данных
        self.assertEquals(response.json().get('results')[0].get('title'), self.part.title)

    def test_list_me_part(self):
        """Тестировние вывода списка предметов"""
        response = self.client.get(reverse('study:part-list-me'))
        # print(response.json())
        # Проверяем статус вывода списка
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        #  Проверка корректности данных
        self.assertEquals(response.json().get('results')[0].get('title'), self.part.title)

    def test_retrive_part(self):
        """Тестировние вывода детальных данных по отдельному предмету"""
        response = self.client.get(reverse('study:part-detail', args=[self.part.pk]))
        # print(response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        #  Проверка корректности данных
        self.assertEquals(response.json().get('title'), self.part.title)

    def test_create_part(self):
        """Тестировние создания предмета"""
        data = {"title": 'test2', 'subject': self.subject.pk}
        response = self.client.post(reverse('study:part-create'), data)
        # print("response.json()", response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        #  Проверка корректности данных
        self.assertEquals(Part.objects.all().count(), 2)

    def test_update_part(self):
        """Тестировние обновления предмета"""
        data = {"title": 'test3'}
        response = self.client.patch(reverse('study:part-update', args=[self.part.pk]), data)
        # print(response.json())
        # Прверяем статус обновления
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # Проверка изменения значения в поле с названием
        self.assertEquals(response.json().get("title"), "test3")

    def test_delete_part(self):
        """Тестировние удаления предмета"""
        response = self.client.delete(reverse('study:part-delete', args=[self.part.pk]))
        # print("response.json()=", response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        #  Проверка корректности данных
        self.assertEquals(Part.objects.all().count(), 0)


class UsefulLinkTestCase(APITestCase):
    """Тестирование CRUD ссылок на полезные материалы для раздела"""

    def setUp(self) -> None:
        self.user = User.objects.create(email='test@mail.ru', is_staff=True, is_superuser=True)
        self.client.force_authenticate(self.user)
        self.subject = Subject.objects.create(title='test_subj', author=self.user)
        self.part = Part.objects.create(title='test_part', subject=self.subject, order_id=1)
        self.link = UsefulLink.objects.create(title='test_link', part=self.part)

    def test_create_link(self):
        """Тестировние создания ссылок на полезные материалы для раздела"""
        data = {"title": 'test_link2', 'part': self.part.pk}
        response = self.client.post(reverse('study:links-create'), data)
        # print("response.json()", response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        #  Проверка корректности данных
        self.assertEquals(UsefulLink.objects.all().count(), 2)

    def test_update_link(self):
        """Тестировние обновления ссылок на полезные материалы для раздела"""
        data = {"title": 'test_link2'}
        response = self.client.patch(reverse('study:links-update', args=[self.link.pk]), data)
        # print(response.json())
        # Прверяем статус обновления
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # Проверка изменения значения в поле с названием
        self.assertEquals(response.json().get("title"), "test_link2")

    def test_delete_link(self):
        """Тестировние удаления ссылок на полезные материалы для раздела"""
        response = self.client.delete(reverse('study:links-delete', args=[self.link.pk]))
        # print("response.json()=", response.json())
        # Прверяем статус вывода списка
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        #  Проверка корректности данных
        self.assertEquals(UsefulLink.objects.all().count(), 0)
