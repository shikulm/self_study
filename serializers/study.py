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

    # def validate(self, attrs):
    #     """Проверка совпадаения паролей"""
    #     data = super().validate(attrs)
    #     if data['password'] != data['password2']:
    #         raise serializers.ValidationError('Пароли не совпадают')
    #     del data['password2']
    #     return data
    #
    # def create(self, validated_data):
    #     user = User(email=validated_data['email'], last_name=validated_data['last_name'], first_name=validated_data['first_name'])
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user


    # def update(self, user, validated_data):
    #     user.name = validated_data['name']
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user



class AccessSubjectGroupSerializer(serializers.ModelSerializer):
    """Сериалайзер для просмотра, добавления и удаления пользователй, имеющих доступ к предмету.
    Выводит id доступа, предмет и пользователя"""

    user = UserSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = AccessSubjectGroup
        # fields = '__all__'
        fields = ['pk', 'subject', 'user']
        # fields = ['subject', 'user']


# class AccessSubjectOnlyUserSerializer(serializers.ModelSerializer):
#     """Сериалайзер для просмотра пользователей, имеющих доступ к предмету.
#     Выводит только данные пользователя"""
#
#     # user = UserSerializer(read_only=True)
#     # subject = SubjectSerializer(read_only=True)
#
#     class Meta:
#         model = AccessSubjectGroup
#         # fields = '__all__'
#         # fields = ['pk', 'subject', 'user']
#         fields = ['user']
#         depth = 1


class SubjectAccessSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода спсика пользоватлей, имеющих доступ к предметам"""

    author = UserSerializer(read_only=True)
    # access_users = AccessSubjectGroupSerializer(many=True, read_only=True)
    # access_users = AccessSubjectUserSerializer(many=True, read_only=True, source='access_users.user')
    # access_users = AccessSubjectOnlyUserSerializer(many=True, read_only=True)
    access_users = UserSerializer(many=True, read_only=True)
    # (many=True, source='access_users.user')
    class Meta:
        model = Subject
        # fields = '__all__'
        fields = ['pk', 'title', 'description', 'author', 'access_users',]
        # fields = ['author', 'access_users',]



# from rest_framework import serializers
#
# from users.models import User
#
#
# # class PaymentSerialaizerForUser(serializers.ModelSerializer):
# #     """Сериалайзер по оплате за обучение. Используется для включения в сериализвтор с пользователями."""
# #     class Meta:
# #         model = Payment
# #         # fields = '__all__'
# #         fields = ("id", "date_pay", "course", "lesson", "payment_amount", "payment_method")
#
#
#
# class UserSerialaizer(serializers.ModelSerializer):
#     """Сериалайзер для пользователя (используется для вывода детальной информации о пользователе).
#     Выводит поля по пользователю ("id", "email", "last_name", "first_name", "avatar")"""
#     # payments = PaymentSerialaizerForUser(many=True, read_only=True)
#
#     class Meta:
#         model = User
#         # fields = '__all__'
#         fields = ("id", "email", "last_name", "first_name", "avatar")
#
# # class UserOtherSerialaizer(serializers.ModelSerializer):
# #     """Сериалайзер для вывода основных данных про другим пользователям.
# #     Выводит поля по пользователяю ("id", "email", "phone", "city", "payments")"""
# #
# #     class Meta:
# #         model = User
# #         # fields = '__all__'
# #         fields = ("id", "email", "phone", "city")
#

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
    # RКоличество вопросов для раздела
    questions_count = serializers.IntegerField(source='questions.count', read_only=True)
    questions = QuestionSerializer(read_only=True, many=True)
    # read_only_fields = ('pk', 'order_id', 'date_create', 'last_update')
    class Meta:
        model = Part
        # fields = '__all__'
        fields = ['pk', 'title', 'subject', 'subject_info', 'description', 'content', 'order_id', 'date_create', 'last_update', 'links', 'quest_to_test',  'questions_count', 'questions']
        # fields = ['pk', 'title', 'subject', 'description', 'content', 'order_id', 'date_create', 'last_update', 'quest_to_test']
        # read_only_fields = ('pk', 'order_id', 'date_create', 'last_update')



