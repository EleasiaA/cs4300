from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer

# Create your views here.

class MovieViewSet(viewsets.ModelViewSet):
    #CRUD operations for movies
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class SeatViewSet(viewsets.ModelViewSet):
    #Seat availability and management
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

class BookingViewSet(viewsets.ModelViewSet):
    #Create bookings and view the logged-in user's booking history
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer

    def get_queryset(self):
        #Only return the current user's bookings
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        #Save the booking and mark seat as boooked together
        with transaction.atomic():
            booking = serializer.save(user=self.request.user)
            booking.seat.is_booked = True
            booking.seat.save()

