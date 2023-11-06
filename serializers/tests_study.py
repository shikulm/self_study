from rest_framework import serializers

from tests_study.models import Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с вариантами ответов на вопросы для теста"""

    class Meta:
        model = Answer
        # fields = '__all__'
        fields = ['pk', 'title', 'correct', 'question']


class QuestionSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с опросами с варантами ответов для теста.
    Варианты ответов можно передавать в виде стандартного словаря answer или в виде списка строк через запятую answers_input
     Для второго варианта перед верным вариантом ответа ставится восклицательный знак:
        answers_input["ответ1", "ответ2", "!правильный ответ"] """

    answers = AnswerSerializer(many=True, required=False)
    answers_input = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)

    class Meta:
        model = Question
        # fields = '__all__'
        fields = ['pk', 'title', 'difficulty', 'part', 'answers', 'answers_input']

    def create(self, validated_data):
        """Создание нового вопроса и ответов на нее"""
        answer_dict = validated_data.pop('answers', None)
        answer_input = validated_data.pop('answers_input', None)
        question = Question.objects.create(**validated_data)
        if answer_input:
            for answer in answer_input:
                # Answer.objects.create(question=question, **answer)
                # Если перед вариантом ответа стоит символ восклицательного знака, то значит ответ правильный
                correct = True if answer[0] == "!" else False
                title = answer[1:] if answer[0] == "!" else answer
                Answer.objects.create(question=question, title=title, correct=correct)
        elif answer_dict:
            for answer in answer_dict:
                Answer.objects.create(question=question, **answer)
        return question

    def update(self, instance, validated_data):
        """Обновление вопроса и вариантов его ответов.
        Варианты ответов обновляются, если передан параметр 'answers'
         Если параметр 'answers' передан, то варианты ответов полностью заменят старые.
         Варианты ответов перечисляются через запятую Перед верным вариантом ответа ставится восклицательный знак:
         answers["ответ1", "ответ2", "!правильный ответ"] """
        # Извлекаем варианты ответов
        answer_dict = validated_data.pop('answers', None)
        answer_input = validated_data.pop('answers_input', None)
        # Обновление вопроса
        # question = Question.objects.filter(pk=self._kwargs('pk') validated_data.get('pk', 0)).update(**validated_data)
        # question = Question.objects.filter(pk=self.context['view'].kwargs.get('pk')).update(**validated_data)

        question = instance
        question.title = validated_data.get('title', instance.title)
        question.difficulty = validated_data.get('difficulty', instance.difficulty)
        question.part = validated_data.get('part', instance.part)
        question.save()

        # instance.save()
        # question = Question.objects.filter(pk=validated_data.get('pk')).update(**validated_data)

        # Обновление вариантов ответов
        if (answer_dict or answer_input) and question:
            Answer.objects.filter(question=question).delete()
            if answer_input:
                for answer in answer_input:
                    # Answer.objects.create(question=question, **answer)
                    # Если перед вариантом ответа стоит символ восклицательного знака, то значит ответ правильный
                    correct = True if answer[0] == "!" else False
                    title = answer[1:] if answer[0] == "!" else answer
                    Answer.objects.create(question=question, title=title, correct=correct)
            else:
                for answer in answer_dict:
                    Answer.objects.create(question=question, **answer)
        return question

    # def update(self, user, validated_data):
    #     """Обновление вопроса и вариантов его ответов.
    #     Варианты ответов обновляются, если передан параметр 'answers'
    #      Если параметр 'answers' передан, то варианты ответов полностью заменят старые.
    #      Варианты ответов перечисляются через запятую Перед верным вариантом ответа ставится восклицательный знак:
    #      answers["ответ1", "ответ2", "!правильный ответ"] """
    #     # Извлекаем варианты ответов
    #     answer_data = validated_data.pop('answers', None)
    #     # Обновление вопроса
    #     question = Question.objects.filter(pk=validated_data.get('pk',0)).update(**validated_data)
    #     # Обновление вариантов ответов
    #     if answer_data:
    #         Answer.objects.filter(question=validated_data.get('pk',0)).delete()
    #         for answer in answer_data:
    #             # Answer.objects.create(question=question, **answer)
    #             # Если перед вариантом ответа стоит символ восклицательного знака, то значит ответ правильный
    #             correct = True if answer[0]=="!" else False
    #             title = answer[1:] if answer[0]=="!" else answer
    #             Answer.objects.create(question=question, title=title, correct=correct)
    #     return question

    # def validate(self, attrs):
    #     """Проверка совпадаения паролей"""
    #     data = super().validate(attrs)
    #     if data['password'] != data['password2']:
    #         raise serializers.ValidationError('Пароли не совпадают')
    #     del data['password2']
    #     return data
    #

    # def update(self, user, validated_data):
    #     user.name = validated_data['name']
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user
