from rest_framework import serializers

from serializers import UserSerializer
from serializers.tests_study import QuestionSerializer
from study.models import Subject, AccessSubjectGroup, Part, UsefulLink


class SubjectSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с общими характеристикаими предметов"""

    author = UserSerializer(read_only=True)

    class Meta:
        model = Subject
        # fields = '__all__'
        fields = ['pk', 'title', 'description', 'author']


class AccessSubjectGroupSerializer(serializers.ModelSerializer):
    """Сериалайзер для просмотра, добавления и удаления пользователй, имеющих доступ к предмету.
    Выводит id доступа, предмет и пользователя"""

    user = UserSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = AccessSubjectGroup
        # fields = '__all__'
        fields = ['pk', 'subject', 'user']


class SubjectAccessSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода спсика пользоватлей, имеющих доступ к предметам"""

    author = UserSerializer(read_only=True)
    access_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Subject
        # fields = '__all__'
        fields = ['pk', 'title', 'description', 'author', 'access_users',]


class UsefulLinkSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с дополнительными материалами раздела"""

    class Meta:
        model = UsefulLink
        fields = '__all__'
        # fields = ['pk', 'title', 'url_link', 'description', 'part']


class PartForStudentSerializer(serializers.ModelSerializer):
    """Сериалайзер для просмотра разделов предметов студентами (не включает информацию для генерации тестов)"""

    subject_info = SubjectSerializer(read_only=True, source="subject")
    links = UsefulLinkSerializer(read_only=True, many=True)

    class Meta:
        model = Part
        # fields = '__all__'
        fields = ['pk', 'title', 'subject', 'subject_info', 'description', 'content', 'order_id', 'date_create', 'last_update', 'links']
        read_only_fields = ('pk', 'order_id', 'date_create', 'last_update')


class PartForAuthorSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с разделами предметов"""

    subject_info = SubjectSerializer(read_only=True, source="subject")
    links = UsefulLinkSerializer(read_only=True, many=True)
    # Количество вопросов для раздела
    questions_count = serializers.IntegerField(source='questions.count', read_only=True)
    questions = QuestionSerializer(read_only=True, many=True)
    # read_only_fields = ('pk', 'order_id', 'date_create', 'last_update')
    class Meta:
        model = Part
        # fields = '__all__'
        fields = ['pk', 'title', 'subject', 'subject_info', 'description', 'content', 'order_id', 'date_create', 'last_update', 'links', 'quest_to_test',  'questions_count', 'questions']



