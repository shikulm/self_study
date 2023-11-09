from django.urls import path
from rest_framework.routers import DefaultRouter

from study.apps import StudyConfig
from study.views import SubjectCreateAPIView, SubjectListAPIView, SubjectRetrieveAPIView, SubjectUpdateAPIView, \
    SubjectDestroyAPIView, SubjectListMeAPIView, GrantUserAPIView, DenyUserAPIView, SubjectAccessListAPIView, \
    PartCreateAPIView, PartListAPIView, PartListMeAPIView, PartRetrieveAPIView, PartUpdateAPIView, PartDestroyAPIView, \
    UsefulLinkCreateAPIView, UsefulLinkUpdateAPIView, UsefulLinkDestroyAPIView



app_name = StudyConfig.name

router = DefaultRouter()
# router.register(r'subject', SubjectViewSet, basename='subject')

urlpatterns = [
    # Subject
    path('subject/', SubjectListAPIView.as_view(), name='subject-list'),
    path('subject/me/', SubjectListMeAPIView.as_view(), name='subject-list-me'),
    path('subject/create/', SubjectCreateAPIView.as_view(), name='subject-create'),
    path('subject/<int:pk>/', SubjectRetrieveAPIView.as_view(), name='subject-detail'),
    path('subject/update/<int:pk>/', SubjectUpdateAPIView.as_view(), name='subject-update'),
    path('subject/delete/<int:pk>/', SubjectDestroyAPIView.as_view(), name='subject-delete'),
    # AccessSubjectGroup
    path('subject/access/', SubjectAccessListAPIView.as_view(), name='subject-access-list'),
    # path('api/subject/access/', AccessSubjectUserSerializerAPIView.as_view(), name='subject-access-list'),
    path('subject/<int:pk_subject>/grantuser/<int:pk_user>/', GrantUserAPIView.as_view(), name='subject-grantuser'),
    path('subject/<int:pk_subject>/denyuser/<int:pk_user>/', DenyUserAPIView.as_view(), name='subject-denyuser'),
    # Part
    path('part/', PartListAPIView.as_view(), name='part-list'),
    path('part/me/', PartListMeAPIView.as_view(), name='part-list-me'),
    path('part/create/', PartCreateAPIView.as_view(), name='part-create'),
    path('part/<int:pk>/',PartRetrieveAPIView.as_view(), name='part-detail'),
    path('part/update/<int:pk>/', PartUpdateAPIView.as_view(), name='part-update'),
    path('part/delete/<int:pk>/', PartDestroyAPIView.as_view(), name='part-delete'),
    # UsefulLink
    path('links/create/', UsefulLinkCreateAPIView.as_view(), name='links-create'),
    path('links/update/<int:pk>/', UsefulLinkUpdateAPIView.as_view(), name='links-update'),
    path('links/delete/<int:pk>/', UsefulLinkDestroyAPIView.as_view(), name='links-delete'),


] + router.urls

