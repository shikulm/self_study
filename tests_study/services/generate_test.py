import random
from django.db import IntegrityError
from rest_framework import status

from study.models import Part, Subject
from tests_study.models import Test, Question, QuestionTest, Answer, AnswerTest


def generate_answer(question_test: QuestionTest):
    """Перемешивает случайным образом ответы на вопрос question. Перемешанные ответы сохраняет в таблицу AnswerTest"""
    answers = Answer.objects.filter(question=question_test.question)
    answers_test_list = []
    if answers:
        answers_list = list(answers)
        random.shuffle(answers_list)
        # Перемешивание и сохранение ответов
        order_id_a = 0
        for answer in answers_list:
            order_id_a += 1
            answer_test = AnswerTest(question_test=question_test, answer=answer, order_id=order_id_a)
            answer_test.save()
            answers_test_list.append(answer_test)
    return answers_test_list


def generate_inter_test(test: Test, part_id: int):
    """Генерация теста для промежуточного тестирования по разделу"""
    # Извлекаем информацию по разделу
    print("generate_inter_test.part_id=", part_id)
    try:
        part = Part.objects.get(pk=part_id)
    except Part.DoesNotExist:
        #  Указан несуществующий раздел
        return {"result": f"Part {part_id} Not Exist", "status_code": status.HTTP_404_NOT_FOUND}

    # Извлекаем все вопросы раздела
    questions = Question.objects.filter(part=part)
    questions_test_list = []

    ## Получаем перемешанный список вопросов, которые будут включены в тест
    # Количество вопросов теста соответсвующее настройкам раздела или (если вопросов не хватает) всем вопросам введенным для раздела
    if questions:
        cnt_quest = min(questions.count(), part.quest_to_test)
        questions_list = random.sample(list(questions), cnt_quest)

        # Сохраняем вопросы в БД
        order_id_q = 0
        for question in questions_list:
            order_id_q += 1
            question_test = QuestionTest(test=test, question=question, order_id=order_id_q)
            question_test.save()
            questions_test_list.append(question_test)

            # Перемешиваем и сохраняем варианты ответов на вопросы
            generate_answer(question_test)
    return questions_test_list


def create_inter_test(user: int, part_id: int):
    """Формирование теста для промежуточного тестирования с вопросами и ответами"""
    #  Создание теста
    try:
        test = Test(type=Test.TYPE_INTERMEDIATE, part_id=part_id, user_id=user)
        test.save()

        # Генерируем вопросы тесты
        generate_inter_test(test=test, part_id=part_id)
        return test
    except IntegrityError:
        return {"result": f"Error create test for user {user} and part {part_id}", "status_code": status.HTTP_404_NOT_FOUND}


def generate_final_test(test: Test, subject_id: int):
    """Генерация теста для итогового тестирования по разделу"""
    # Извлекаем информацию по предмету
    try:
        subject = Subject.objects.get(pk=subject_id)
    except Subject.DoesNotExist:
        #  Указан несуществующий раздел
        return {"result": f"Subject {subject_id} Not Exist", "status_code": status.HTTP_404_NOT_FOUND}
    # Генерируем тесты для всех разделов предмета
    parts = Part.objects.filter(subject_id=subject_id)
    questions_test_list = []
    for part in parts:
        questions_test_list += generate_inter_test(test=test, part_id= part.pk)

    return questions_test_list


def create_final_test(user: int, subject_id: int):
    """Формирование теста для итогового тестирования с вопросами и ответами"""
    #  Создание теста
    try:
        test = Test(type=Test.TYPE_FINAL, subject_id=subject_id, user_id=user)
        test.save()

        # Генерируем вопросы тесты
        generate_final_test(test=test, subject_id=subject_id)
        return test
    except IntegrityError:
        return {"result": f"Error create test for user {user} and subject {subject_id}",
                "status_code": status.HTTP_404_NOT_FOUND}


def generate_test(user: int, type: str, parent_id: int):
    """
    Функция для генерации тестов
    ПарметрыL
    user - код тестируемого пользователя
    type - тип теста (inter - промежуточный, final - итоговый)
    parent_id - код объекта, для которого генерируется тест. Для промежуточного part_id, для итогового - subject_id
    """

    if type==Test.TYPE_INTERMEDIATE:
        # Промежуточное тестирование
        return create_inter_test(user=user, part_id=parent_id)
    else:
        # Итоговое тестирование
        return create_final_test(user=user, subject_id=parent_id)


