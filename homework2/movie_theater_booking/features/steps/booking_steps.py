from datetime import date

from behave import given, when, then
from django.contrib.auth import get_user_model
from django.urls import reverse

from bookings.models import Movie, Seat, Booking

User = get_user_model()


@given('a movie "{title}" exists')
def step_movie(context, title):
    Movie.objects.create(title=title, description="Test", release_date=date(2010, 7, 16), duration=120)


@given('a seat "{number}" is available')
def step_seat_available(context, number):
    Seat.objects.create(seat_number=number, is_booked=False)


@given('a seat "{number}" is already booked')
def step_seat_booked(context, number):
    Seat.objects.create(seat_number=number, is_booked=True)


@given('I am logged in as "{username}"')
def step_login(context, username):
    user = User.objects.create_user(username, password="pw12345")
    context.test.client.force_login(user)


@when('I book seat "{number}" for "{title}"')
def step_book(context, number, title):
    movie = Movie.objects.get(title=title)
    seat = Seat.objects.get(seat_number=number)
    context.response = context.test.client.post(
        reverse("book_seat", args=[movie.id]), {"seat": seat.id})


@then('seat "{number}" is marked as booked')
def step_seat_is_booked(context, number):
    assert Seat.objects.get(seat_number=number).is_booked


@then('the booking is rejected')
def step_rejected(context):
    assert context.response.status_code == 404, context.response.status_code


@then('"{username}" has {count:d} booking')
@then('"{username}" has {count:d} bookings')
def step_booking_count(context, username, count):
    assert Booking.objects.filter(user__username=username).count() == count