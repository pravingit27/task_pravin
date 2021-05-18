from django.urls import path,include
from django.conf.urls import url
from .serializers import studentserializer,markserializer
from . import views
from .views import StudentViewSet,Listmark,Detailmark,GradeViewSet,TotalCountAPIView
from rest_framework import routers
router = routers.DefaultRouter()

router.register(r'students', views.StudentViewSet)
router.register(r'student/results',views.GradeViewSet)

urlpatterns = [
    path('add-mark',Listmark.as_view(),name='marklist'),
    path('add-mark/<int:pk>',Detailmark.as_view(),name='singlelist'),
    path('count',TotalCountAPIView.as_view(),name='totalcount'),
    #path('count',views.count,name='count.add'),
    path(r'',include(router.urls))
]