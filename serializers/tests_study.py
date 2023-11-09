from rest_framework import serializers

from serializers import UserSerializer
from tests_study.models import Question, Answer, AnswerTest, QuestionTest, Test



#### Сериалайзеры ввода вопросов с ответами для последующего тестирования

class AnswerSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с вариантами ответов на вопросы для теста"""

    class Meta:
        model = Answer
        # fields = '__all__'
        fields = ['pk', 'title', 'correct', 'question']



class QuestionSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с вопросами с варантами ответов для теста.
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
        question = instance
        question.title = validated_data.get('title', instance.title)
        question.difficulty = validated_data.get('difficulty', instance.difficulty)
        question.part = validated_data.get('part', instance.part)
        question.save()

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


#### Генерация тестов

class AnswerTestSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода пользователю вариантов ответа теста"""

    pk_answer = serializers.IntegerField(source='pk', read_only=True)
    answer = serializers.CharField(read_only=True, source="answer.title")

    class Meta:
        model = AnswerTest
        # fields = '__all__'
        fields = ['pk_answer', 'order_id', 'answer']

class QuestionTestSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода пользователю вопросов теста"""

    pk_question = serializers.IntegerField(source='pk', read_only=True)
    question = serializers.CharField(read_only=True, source='question.title')
    answers_test = AnswerTestSerializer(read_only=True, many=True)

    class Meta:
        model = QuestionTest
        # fields = '__all__'
        fields = ['pk_question', 'order_id', 'question', 'answers_test']



class TestSerializer(serializers.ModelSerializer):
    """Сериалайзер для вывода теста пользователю"""

    pk_test = serializers.IntegerField(source='pk', read_only=True)
    type = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    topic = serializers.SerializerMethodField()
    questions_count = serializers.IntegerField(source='questions_test.count', read_only=True)
    questions_test = QuestionTestSerializer(read_only=True, many=True)

    def get_type(self, instance):
        return Test.TYPE[0][1] if instance.type==Test.TYPE[0][0] else Test.TYPE[1][1]

    def get_topic(self, instance):
        return instance.subject.title if instance.subject else instance.part.title

    class Meta:
        model = Test
        # fields = '__all__'
        fields = ['pk_test', 'type', 'user',  'date_create', 'topic', 'questions_count', 'questions_test']


#### Получение от пользователя ответов на тесты и выдача результатов

class TestUserAnswerSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения ответов пользователя на вопросы теста"""

    # Для ввода пользоватлем
    pk_question = serializers.IntegerField(source='pk')
    pk_answer = serializers.IntegerField(write_only=True, source='user_answer')

    #  Для вывода результатов
    question = serializers.CharField(read_only=True, source="question.title")
    difficulty = serializers.IntegerField(read_only=True, source="question.difficulty")
    user_answer = serializers.CharField(read_only=True, source="user_answer.title")
    correct_answer = serializers.SerializerMethodField(read_only=True)
    result = serializers.SerializerMethodField(read_only=True)

    def get_correct_answer(self, instance):
        correct_answer_obj = Answer.objects.filter(correct=True, answer_test__question_test=instance).first()
        return correct_answer_obj.title if correct_answer_obj else None


    def get_result(self, instance):
        return instance.user_answer.title == self.get_correct_answer(instance)


    class Meta:
        model = QuestionTest
        # fields = '__all__'
        fields = ['pk_question', 'pk_answer', 'question', 'difficulty', 'user_answer', 'correct_answer', 'result']


class TestUserResultSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения ответов пользоваетля на тест и вывода резульатов.
    От пользователя данные примаем в формате:
    "user_answer":[{"pk_question": pk_question, "pk_answer": pk_answer}, {...}, ...] """

    # Поля для вывода результатов тестирования пользователю
    pk_test = serializers.IntegerField(source='pk', read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    user = UserSerializer(read_only=True)
    topic = serializers.SerializerMethodField(read_only=True)

    # Список для ввода ответов пользователя и вывода результатов
    user_answer = TestUserAnswerSerializer(many=True, read_only=True)

    def get_type(self, instance):
        return Test.TYPE[0][1] if instance.type==Test.TYPE[0][0] else Test.TYPE[1][1]

    def get_topic(self, instance):
        return instance.subject.title if instance.subject else instance.part.title

    class Meta:
        model = Test
        # fields = '__all__'
        fields = ['pk_test', 'type', 'user',  'date_create', 'topic', 'ball', "user_answer"]

