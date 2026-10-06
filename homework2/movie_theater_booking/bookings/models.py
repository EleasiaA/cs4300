from django.db import models
from django.conf import settings

# Create your models here.


#title, description, release date, duration
class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text='Duration in minutes')

    def __str__(self):
        return self.title

#seat number, booking status
class Seat(models.Model):
    seat_number = models.CharField(max_length=5, unique=True)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return self.seat_number

#movie, seat, user, booking date
class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT)
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.movie} - Seat {self.seat}"