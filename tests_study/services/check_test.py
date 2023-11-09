from django.db.models import Sum

from tests_study.models import Test, QuestionTest, Answer, Question


def count_ball(test_obj):
    """Вычисление и сохранение балла за прохождение теста"""
    # Вычисляем максимальный балл, оторый можно получить за тест в абсалютных единицах
    max_sum_ball = Question.objects.filter(questions_test__test=test_obj).aggregate(max_sum_ball=Sum('difficulty')).get("max_sum_ball", 0)
    # Вычисляем балл, который набрал студент
    real_sum_ball = Question.objects.filter(questions_test__test=test_obj, questions_test__isCorrect=True).aggregate(real_sum_ball=Sum('difficulty')).get("real_sum_ball", 0)
    # Вычисляем балл стиудента в процентах от максимума
    ball = real_sum_ball/max_sum_ball * 100

    # Сохранем балл студента в БД
    test_obj.ball = ball
    test_obj.save()
    return ball

def check_user_answer(question_test: QuestionTest):
    """Проверка правильности ответа пользователя"""
    # Извлекаем правильный ответ на вопрос
    correct_answer = Answer.objects.filter(question=question_test.question, correct=True).first()
    # Проверка правильности ответа
    isCorrect = False
    if correct_answer:
        isCorrect = question_test.user_answer==correct_answer
    # Сохранение рехзульатат проверки в бд
    question_test.isCorrect = isCorrect
    question_test.save()
    return isCorrect


def check_test(test_obj: Test) -> None:
    """Проверяет резульаты тестирования и сохраняет в БД"""
    #  Получаем список вопросов с ответами пользователя
    questions_test = QuestionTest.objects.filter(test=test_obj)
    #  Проверяем ответ пользователя
    for question_test in questions_test:
        check_user_answer(question_test)

    # Вычисление итогового балла
    count_ball(test_obj)