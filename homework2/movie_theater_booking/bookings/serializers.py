from rest_framework import serializers
from .models import Movie

"""Converts Movie objects to and from JSON"""
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'