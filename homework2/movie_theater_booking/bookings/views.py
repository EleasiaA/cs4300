from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.contrib.auth.decorators import login_required

from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer

# Create your views here.

def movie_list(request):
    #Render the page listing all movies
    movies = Movie.objects.all()
    return render(request, 'bookings/movie_list.html', {'movies': movies})

@login_required
def book_seat(request, movie_id):
    #Render the page where user books seat
    movie = get_object_or_404(Movie, pk=movie_id)
    available_seats = Seat.objects.filter(is_booked=False)
    
    if request.method == 'POST':
        #Only accept a seat that is still unbooked
        seat = get_object_or_404(Seat, pk=request.POST.get('seat'), is_booked=False)

        #Create the booking and mark the seat as booked together
        with transaction.atomic():
            Booking.objects.create(movie=movie, seat=seat, user=request.user)
            seat.is_booked = True
            seat.save()
        # Change to 'booking_history' once that page exists
        return redirect('booking_history')

    return render(request, 'bookings/seat_booking.html', {'movie': movie, 'seats': available_seats})

@login_required
def booking_history(request):
    #Render the page listing booking history
    bookings = Booking.objects.filter(user=request.user).select_related('movie', 'seat').order_by('-booking_date')
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})


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

