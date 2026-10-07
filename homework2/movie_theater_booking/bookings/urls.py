from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import MovieViewSet, SeatViewSet, BookingViewSet

router = DefaultRouter()
router.register(r"movies", MovieViewSet)
router.register(r"seats", SeatViewSet)
router.register(r"bookings", BookingViewSet, basename='booking')


urlpatterns = [path('', include(router.urls))]