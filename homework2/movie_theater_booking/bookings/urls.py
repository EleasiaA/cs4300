from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import MovieViewSet, SeatViewSet

router = DefaultRouter()
router.register(r"movies", MovieViewSet)
router.register(r"seats", SeatViewSet)


urlpatterns = [path('', include(router.urls))]