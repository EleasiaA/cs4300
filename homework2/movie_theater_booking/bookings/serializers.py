from rest_framework import serializers
from .models import Movie, Seat, Booking

"""Converts Movie objects to and from JSON"""
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
    
"""Converts Seat objects to and from JSON"""
class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'

"""Converts Booking objects to and from JSON"""
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    #Rejects booking if the seat is already taken
    def validate_seat(self, seat):
        if seat.is_booked:
            raise serializers.ValidationError("This seat is already booked.")
        return seat       