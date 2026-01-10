from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apps import HabitConfig
from .views import HabitViewSet, PublicHabitViewSet


app_name = HabitConfig.name

router = DefaultRouter()
router.register(r'my', HabitViewSet, basename='my_habits')
router.register(r'public', PublicHabitViewSet, basename='public_habits')

urlpatterns = [
    path('', include(router.urls)),
]