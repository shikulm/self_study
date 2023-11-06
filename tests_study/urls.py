from django.urls import path
from rest_framework.routers import DefaultRouter

from tests_study.apps import TestsConfig
from tests_study.views import QuestionCreateAPIView, QuestionUpdateAPIView, QuestionDestroyAPIView

app_name = TestsConfig.name

router = DefaultRouter()
# router.register(r'subject', SubjectViewSet, basename='subject')

urlpatterns = [
    # Question
    path('question/create/', QuestionCreateAPIView.as_view(), name='question-create'),
    path('question/update/<int:pk>/', QuestionUpdateAPIView.as_view(), name='question-update'),
    path('question/delete/<int:pk>/', QuestionDestroyAPIView.as_view(), name='question-delete'),

    # # Subject
    # path('api/subject/', SubjectListAPIView.as_view(), name='subject-list'),
    # path('api/subject/me/', SubjectListMeAPIView.as_view(), name='subject-list-me'),
    # path('api/subject/create/', SubjectCreateAPIView.as_view(), name='subject-create'),
    # path('api/subject/<int:pk>/', SubjectRetrieveAPIView.as_view(), name='subject-detail'),
    # path('api/subject/update/<int:pk>/', SubjectUpdateAPIView.as_view(), name='subject-update'),
    # path('api/subject/delete/<int:pk>/', SubjectDestroyAPIView.as_view(), name='subject-delete'),
    # # AccessSubjectGroup
    # path('api/subject/access/', SubjectAccessListAPIView.as_view(), name='subject-access-list'),
    # # path('api/subject/access/', AccessSubjectUserSerializerAPIView.as_view(), name='subject-access-list'),
    # path('api/subject/<int:pk_subject>/grantuser/<int:pk_user>/', GrantUserAPIView.as_view(), name='subject-grantuser'),
    # path('api/subject/<int:pk_subject>/denyuser/<int:pk_user>/', DenyUserAPIView.as_view(), name='subject-denyuser'),
    # # Part
    # path('api/part/', PartListAPIView.as_view(), name='part-list'),
    # path('api/part/me/', PartListMeAPIView.as_view(), name='part-list-me'),
    # path('api/part/create/', PartCreateAPIView.as_view(), name='part-create'),
    # path('api/part/<int:pk>/',PartRetrieveAPIView.as_view(), name='part-detail'),
    # path('api/part/update/<int:pk>/', PartUpdateAPIView.as_view(), name='part-update'),
    # path('api/part/delete/<int:pk>/', PartDestroyAPIView.as_view(), name='part-delete'),
    # # UsefulLink
    # path('api/links/create/', UsefulLinkCreateAPIView.as_view(), name='links-create'),
    # path('api/links/update/<int:pk>/', UsefulLinkUpdateAPIView.as_view(), name='links-update'),
    # path('api/links/delete/<int:pk>/', UsefulLinkDestroyAPIView.as_view(), name='links-delete'),
] + router.urls

