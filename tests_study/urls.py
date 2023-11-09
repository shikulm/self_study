from django.urls import path
from rest_framework.routers import DefaultRouter

from tests_study.apps import TestsConfig
from tests_study.views import QuestionCreateAPIView, QuestionUpdateAPIView, QuestionDestroyAPIView, \
    TestGeneratePartView, TestGenerateSubjectView, TestAnswerViewUpdateAPIView, SubjectStatListAPIView, \
    PartStatListAPIView, UserStatListAPIView

app_name = TestsConfig.name

router = DefaultRouter()


urlpatterns = [
    # Question
    path('question/create/', QuestionCreateAPIView.as_view(), name='question-create'),
    path('question/update/<int:pk>/', QuestionUpdateAPIView.as_view(), name='question-update'),
    path('question/delete/<int:pk>/', QuestionDestroyAPIView.as_view(), name='question-delete'),
    # Test
    path('create/part/<int:parent_id>/', TestGeneratePartView.as_view(), name='test-part-create'),
    path('create/subject/<int:parent_id>/', TestGenerateSubjectView.as_view(), name='test-subject-create'),
    path('<int:pk>/answer/', TestAnswerViewUpdateAPIView.as_view(), name='test-user_answer-update'),
    # Statistics
    path('statistics/subject/', SubjectStatListAPIView.as_view(), name='test-subject-statistics'),
    path('statistics/part/', PartStatListAPIView.as_view(), name='test-part-statistics'),
    path('statistics/user/', UserStatListAPIView.as_view(), name='test-part-statistics'),
] + router.urls

