from datetime import date

from io import StringIO
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Movie, Seat, Booking

User = get_user_model()


def make_movie(**kwargs):
    """Create a Movie with sensible defaults for tests."""
    data = dict(title="Inception", description="A heist in dreams.", release_date=date(2010, 7, 16), duration=148)
    data.update(kwargs)
    return Movie.objects.create(**data)


# ---------- Model unit tests ----------
class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", password="pw12345")
        self.movie = make_movie()
        self.seat = Seat.objects.create(seat_number="A1")

    def test_movie_str(self):
        self.assertEqual(str(self.movie), "Inception")

    def test_seat_str_and_default_unbooked(self):
        self.assertEqual(str(self.seat), "A1")
        self.assertFalse(self.seat.is_booked)

    def test_seat_number_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Seat.objects.create(seat_number="A1")

    def test_booking_str_and_auto_date(self):
        booking = Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        self.assertIn("Inception", str(booking))
        self.assertIsNotNone(booking.booking_date)

    def test_cannot_delete_movie_with_bookings(self):
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        with self.assertRaises(ProtectedError):
            self.movie.delete()

    def test_deleting_user_deletes_their_bookings(self):
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        self.user.delete()
        self.assertEqual(Booking.objects.count(), 0)


# ---------- HTML page tests ----------
class MovieListViewTest(TestCase):
    def test_saved_movie_appears_on_the_page(self):
        make_movie()
        response = self.client.get(reverse("movie_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inception")
        self.assertContains(response, "A heist in dreams.")

    def test_empty_state_shown_when_no_movies_exist(self):
        response = self.client.get(reverse("movie_list"))
        self.assertContains(response, "No movies in the database yet")


class PageBookingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", password="pw12345")
        self.other = User.objects.create_user("bob", password="pw12345")
        self.movie = make_movie()
        self.seat = Seat.objects.create(seat_number="A1")

    def test_book_page_requires_login(self):
        response = self.client.get(reverse("book_seat", args=[self.movie.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_book_page_lists_available_seats(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("book_seat", args=[self.movie.id]))
        self.assertContains(response, "A1")

    def test_book_page_unknown_movie_is_404(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("book_seat", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_post_creates_booking_and_marks_seat(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse("book_seat", args=[self.movie.id]),
                                    {"seat": self.seat.id})
        self.assertEqual(response.status_code, 302)
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.is_booked)
        self.assertEqual(Booking.objects.filter(user=self.user).count(), 1)

    def test_post_for_booked_seat_is_rejected(self):
        self.seat.is_booked = True
        self.seat.save()
        self.client.force_login(self.user)
        response = self.client.post(reverse("book_seat", args=[self.movie.id]),
                                    {"seat": self.seat.id})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Booking.objects.count(), 0)

    def test_history_requires_login(self):
        response = self.client.get(reverse("booking_history"))
        self.assertEqual(response.status_code, 302)

    def test_history_shows_only_own_bookings(self):
        other_seat = Seat.objects.create(seat_number="B1")
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        Booking.objects.create(movie=self.movie, seat=other_seat, user=self.other)
        self.client.force_login(self.user)
        response = self.client.get(reverse("booking_history"))
        self.assertContains(response, "A1")
        self.assertNotContains(response, "B1")

    def test_history_empty_message(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("booking_history"))
        self.assertContains(response, "haven't booked anything yet")


# ---------- API integration tests ----------
class MovieAPITests(APITestCase):
    def setUp(self):
        self.movie = make_movie()

    def test_list_movies(self):
        response = self.client.get("/api/movies/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]["title"], "Inception")

    def test_retrieve_movie(self):
        response = self.client.get(f"/api/movies/{self.movie.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["duration"], 148)

    def test_create_movie(self):
        payload = {"title": "Dune", "description": "Sand.",
                   "release_date": "2021-10-22", "duration": 155}
        response = self.client.post("/api/movies/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 2)

    def test_create_movie_invalid_returns_400(self):
        response = self.client.post("/api/movies/", {"title": ""}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_movie(self):
        response = self.client.patch(f"/api/movies/{self.movie.id}/",
                                     {"title": "Renamed"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, "Renamed")

    def test_delete_movie(self):
        response = self.client.delete(f"/api/movies/{self.movie.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movie.objects.count(), 0)

    def test_missing_movie_is_404(self):
        self.assertEqual(self.client.get("/api/movies/9999/").status_code, 404)


class SeatAPITests(APITestCase):
    def test_create_and_list_seats(self):
        response = self.client.post("/api/seats/", {"seat_number": "A1"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertFalse(response.json()["is_booked"])
        listing = self.client.get("/api/seats/")
        self.assertEqual(len(listing.json()), 1)

    def test_duplicate_seat_number_returns_400(self):
        Seat.objects.create(seat_number="A1")
        response = self.client.post("/api/seats/", {"seat_number": "A1"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("seat_number", response.json())


class BookingAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("alice", password="pw12345")
        self.other = User.objects.create_user("bob", password="pw12345")
        self.movie = make_movie()
        self.seat = Seat.objects.create(seat_number="A1")

    def test_requires_authentication(self):
        response = self.client.get("/api/bookings/")
        self.assertIn(response.status_code, (401, 403))

    def test_create_booking_sets_user_and_marks_seat(self):
        self.client.force_login(self.user)
        response = self.client.post("/api/bookings/",
                                    {"movie": self.movie.id, "seat": self.seat.id},
                                    format="json")
        self.assertEqual(response.status_code, 201)
        booking = Booking.objects.get()
        self.assertEqual(booking.user, self.user)
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.is_booked)

    def test_client_cannot_choose_user(self):
        self.client.force_login(self.user)
        self.client.post("/api/bookings/",
                         {"movie": self.movie.id, "seat": self.seat.id,
                          "user": self.other.id}, format="json")
        self.assertEqual(Booking.objects.get().user, self.user)

    def test_double_booking_returns_400(self):
        self.client.force_login(self.user)
        payload = {"movie": self.movie.id, "seat": self.seat.id}
        self.client.post("/api/bookings/", payload, format="json")
        response = self.client.post("/api/bookings/", payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Booking.objects.count(), 1)

    def test_history_only_shows_own_bookings(self):
        other_seat = Seat.objects.create(seat_number="B1")
        Booking.objects.create(movie=self.movie, seat=self.seat, user=self.user)
        Booking.objects.create(movie=self.movie, seat=other_seat, user=self.other)
        self.client.force_login(self.user)
        response = self.client.get("/api/bookings/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_deleting_booking_frees_seat(self):
        self.client.force_login(self.user)
        self.client.post("/api/bookings/",
                         {"movie": self.movie.id, "seat": self.seat.id}, format="json")
        booking = Booking.objects.get()
        response = self.client.delete(f"/api/bookings/{booking.id}/")
        self.assertEqual(response.status_code, 204)
        self.seat.refresh_from_db()
        self.assertFalse(self.seat.is_booked)

    def test_booking_cannot_be_edited(self):
        self.client.force_login(self.user)
        self.client.post("/api/bookings/", {"movie": self.movie.id, "seat": self.seat.id}, format="json")
        booking = Booking.objects.get()
        other = Seat.objects.create(seat_number="B1")
        response = self.client.patch(f"/api/bookings/{booking.id}/", {"seat": other.id}, format="json")
        self.assertEqual(response.status_code, 405)

class SeedCommandTests(TestCase):
    def test_seed_loads_data_and_is_repeatable(self):
        call_command("seed_movies", stdout=StringIO())
        call_command("seed_movies", stdout=StringIO())  # second run adds nothing
        self.assertEqual(Movie.objects.count(), 15)
        self.assertEqual(Seat.objects.count(), 32)
        self.assertFalse(Seat.objects.filter(is_booked=True).exists())