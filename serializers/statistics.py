####Сериалайзеры для статистики по результатм тестирования
from rest_framework import serializers

from serializers import SubjectSerializer, UserSerializer
from serializers.tests_study import TestUserResultSerializer
from study.models import Subject, Part
from users.models import User


class StatisticsSerializer(serializers.Serializer):
    """Сериалайзер для получения стастики для тестирования пользователей (количество тестов, минимальный, максимальный и средний балл).
     Значения показтелей вычисляются в представлении на уровне студентов, предметов и разделов"""
    tests_count = serializers.IntegerField() # Количество тестов
    min_ball = serializers.FloatField()  # Минимальный балл
    max_ball = serializers.FloatField() # Максимальный балл
    avg_ball = serializers.FloatField()  # Средний балл


class SubjectStatisticSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода статистки по предмету"""
    statistics = StatisticsSerializer(read_only=True) # Стастистика
    detail = TestUserResultSerializer(read_only=True, many=True) # Подробная информация по тестам
    author = UserSerializer(read_only=True)

    class Meta:
        model = Subject
        # fields = '__all__'
        fields = ['id', 'title', 'description', 'author', 'statistics', 'detail']


class PartStatisticSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода статистки по разделу"""
    subject_info = SubjectSerializer(read_only=True, source="subject")
    questions_count = serializers.IntegerField(source='questions.count', read_only=True)

    statistics = StatisticsSerializer(read_only=True)  # Стастистика
    detail = TestUserResultSerializer(read_only=True, many=True)  # Полробна информация по тестам

    class Meta:
        model = Part
        # fields = '__all__'
        fields = ['id', 'title', 'subject_info', 'date_create', 'last_update', 'questions_count', 'statistics', 'detail']


class UserStatisticSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода статистки по разделу"""

    statistics = StatisticsSerializer(read_only=True)  # Стастистика
    detail = TestUserResultSerializer(read_only=True, many=True)  # Полробна информация по тестам

    class Meta:
        model = User
        # fields = '__all__'
        fields = ['id', 'email', 'last_name', 'first_name', 'statistics', 'detail']