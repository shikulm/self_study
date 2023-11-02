from django.urls import path
from rest_framework.routers import DefaultRouter

from study.apps import StudyConfig
# from study.views import SubjectViewSet
from study.views import SubjectCreateAPIView, SubjectListAPIView, SubjectRetrieveAPIView, SubjectUpdateAPIView, \
    SubjectDestroyAPIView, SubjectListMeAPIView, GrantUserAPIView, DenyUserAPIView, SubjectAccessListAPIView
    # AccessSubjectUserSerializerAPIView

# AccessSubjectUserSerializerAPIView

app_name = StudyConfig.name

router = DefaultRouter()
# router.register(r'subject', SubjectViewSet, basename='subject')

urlpatterns = [
    # Subject
    path('api/subject/', SubjectListAPIView.as_view(), name='subject-list'),
    path('api/subject/me/', SubjectListMeAPIView.as_view(), name='subject-list-me'),
    path('api/subject/create/', SubjectCreateAPIView.as_view(), name='subject-create'),
    path('api/subject/<int:pk>/', SubjectRetrieveAPIView.as_view(), name='subject-detail'),
    path('api/subject/update/<int:pk>/', SubjectUpdateAPIView.as_view(), name='subject-update'),
    path('api/subject/delete/<int:pk>/', SubjectDestroyAPIView.as_view(), name='subject-delete'),
    # AccessSubjectGroup
    path('api/subject/access/', SubjectAccessListAPIView.as_view(), name='subject-access-list'),
    # path('api/subject/access/', AccessSubjectUserSerializerAPIView.as_view(), name='subject-access-list'),
    path('api/subject/<int:pk_subject>/grantuser/<int:pk_user>/', GrantUserAPIView.as_view(), name='subject-grantuser'),
    path('api/subject/<int:pk_subject>/denyuser/<int:pk_user>/', DenyUserAPIView.as_view(), name='subject-denyuser'),



    # path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    # path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name = 'lesson-one'),
    # path('lessons/create/', LessonCreateAPIView.as_view(),name = 'lesson-create'),
    # path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(),name = 'lesson-update'),
    # path('lessons/delete/<int:pk>/', LessonDestroyAPIView.as_view(),name = 'lesson-delete'),
    #
    # path('payment/', PaymentListAPIView.as_view(), name='payment-list'),
    # path('course/payment/create/', PaymentCourceCreateAPIView.as_view(), name='payment-course-create'),
    # path('course/payment/update/<int:pk>/', PaymentCourceUpdateAPIView.as_view(), name='payment-course-update'),
    #
    # path('subscripe/', SubscriptionListAPIView.as_view(), name='subscripe-list'),
    # path('subscripe/<int:pk>/', SubscriptionRetrieveAPIView.as_view(), name='subscripe-one'),
    # path('subscripe/create/', SubscriptionCreateAPIView.as_view(), name='subscripe-create'),
    # path('subscripe/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='subscripe-delete'),
] + router.urls

