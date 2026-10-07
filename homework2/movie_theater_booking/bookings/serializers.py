from rest_framework import serializers
from .models import Movie, Seat, Booking

"""Converts Movie objects to and from JSON"""
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
    
"""Converts Movie objects to and from JSON"""
class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'
