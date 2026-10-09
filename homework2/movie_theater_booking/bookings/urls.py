from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r"movies", views.MovieViewSet)
router.register(r"seats", views.SeatViewSet)
router.register(r"bookings", views.BookingViewSet, basename='booking')


urlpatterns = [
    #HTML pages
    path('', views.movie_list, name='movie_list'),
    path('book/<int:movie_id>/', views.book_seat, name='book_seat'),
    path('bookings/history/', views.booking_history, name='booking_history'),
    #REST API
    path('api/', include(router.urls)),
    ]