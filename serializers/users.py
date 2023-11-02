from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации пользователя"""
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['pk', 'email', 'last_name', 'first_name', 'password', 'password2']

    def validate(self, attrs):
        """Проверка совпадаения паролей"""
        data = super().validate(attrs)
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Пароли не совпадают')
        del data['password2']
        return data

    def create(self, validated_data):
        user = User(email=validated_data['email'], last_name=validated_data['last_name'], first_name=validated_data['first_name'])
        user.set_password(validated_data['password'])
        user.save()
        return user


    # def update(self, user, validated_data):
    #     user.name = validated_data['name']
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user





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
