# Movie Theater Booking Application

A Django and Django REST Framework application for browsing movies, booking seats, and viewing booking history. It has a REST API and a Bootstrap-styled web interface that work on the same data.

**Live site (Render):** https://cs4300-27rz.onrender.com

> Note: the site runs on Render's free tier, so the first load after a period of inactivity can take about a minute.

## Features

- View movie listings (web page and API)
- Book an available seat for a movie (web page and API)
- View your own booking history (web page and API)
- Full CRUD for movies through the API
- Login and logout from the navigation bar
- Validation that prevents booking a seat that is already taken
-The interface uses the Bootswatch "Darkly" theme, Boostrap Icons, and a card grid for movies.

## Project Structure

The Django project folder (the one containing `manage.py`) sits inside `homework2`, and the `bookings` app is inside it, next to the settings package.

```
homework2/
    README.md
    .gitignore
    venv_hw2/                      (virtual environment, not committed)
    movie_theater_booking/         (project folder, contains manage.py)
        manage.py
        build.sh                   (Render build script)
        requirements.txt
        movie_theater_booking/     (settings package)
            settings.py
            urls.py
            wsgi.py
            asgi.py
        bookings/                  (the app)
            models.py              (Movie, Seat, Booking)
            serializers.py         (DRF serializers)
            views.py               (viewsets and template views)
            urls.py                (page and API routes)
            tests.py               (unit and integration tests)
            migrations/
            templates/bookings/
                base.html
                movie_list.html
                seat_booking.html
                booking_history.html
        features/                  (Behave BDD tests)
            booking.feature
            steps/booking_steps.py
            management/commands
               seed_movies.py
```

## Models

| Model | Fields |
|---|---|
| **Movie** | title, description, release_date, duration (minutes) |
| **Seat** | seat_number (unique), is_booked |
| **Booking** | movie, seat, user, booking_date (set automatically) |

`on_delete` choices: a movie or seat cannot be deleted while bookings reference it (`PROTECT`), and deleting a user deletes their bookings (`CASCADE`).

## Setup Instructions

All commands are run from the folder that contains `manage.py` (`homework2/movie_theater_booking/`).

1. Create and activate a virtual environment (from `homework2/`):
   ```bash
   python3 -m venv venv_hw2 --system-site-packages
   source venv_hw2/bin/activate
   ```
2. Install dependencies:
   ```bash
   cd movie_theater_booking
   pip install -r requirements.txt
   ```
3. Create the database tables:
   ```bash
   python manage.py migrate
   ```
4. Create an admin user:
   ```bash
   python manage.py createsuperuser
   ```
5. Start the server:
   ```bash
   python manage.py runserver 0.0.0.0:3000
   ```
   In DevEdu, open the app using the "app" button next to the editor.
6. Log in (the **Log in** link in the navbar, or `/api-auth/login/`), then add data:
   - Add movies at `/api/movies/`
   - Add seats at `/api/seats/` (leave **Is booked** unchecked)
7. Load sample data (15 movies and 32 seats;   safe to run repeatedly). 'build.sh' runs it on each Render deploy:
   ```bash
   python manage.py seed_movies
   ```

## Web Pages

| URL | Description |
|---|---|
| `/` | Movie list |
| `/book/<movie_id>/` | Seat booking for a movie (login required) |
| `/bookings/history/` | The logged-in user's booking history (login required) |
| `/admin/` | Django admin |

## API Endpoints

| Endpoint | Description |
|---|---|
| `/api/movies/` | List movies, create a movie |
| `/api/movies/<id>/` | Retrieve, update, or delete a movie |
| `/api/seats/` | List seats and availability, create a seat |
| `/api/seats/<id>/` | Retrieve, update, or delete a seat |
| `/api/bookings/` | List the logged-in user's bookings, create a booking (login required) |
| `/api/bookings/<id>/` | Retrieve, update, or delete one of your bookings |

Creating a booking through the API sets the user from the logged-in account, marks the seat as booked, and returns a `400` error if the seat is already booked.

> Note: Bookings can be created, viewed, and cancelled (DELETE), but not edited. PUT and PATCH return 405.

## Running the Tests

```bash
# Unit and API integration tests (33 tests)
python manage.py test

# Behave (BDD) tests
python manage.py behave

# Coverage
pip install coverage
coverage run manage.py test
coverage report --include="bookings/*" --omit="bookings/migrations/*"
```

- **Unit tests** cover the models (string output, unique seat numbers, default values, delete rules) and the page views (login redirects, booking, history).
- **Integration tests** use DRF's `APITestCase` to check status codes and JSON for the movie, seat, and booking endpoints, including the `400` for double booking and authentication requirements.
- **BDD tests** (Behave) describe booking an available seat and being rejected when booking a taken seat.
- Test coverage: **100%** for the `bookings` app.

## Deployment (Render)

The app is deployed as a Render Web Service backed by a Render PostgreSQL database.

- **Root Directory:** `homework2/movie_theater_booking`
- **Build Command:** `./build.sh` (installs requirements, runs `collectstatic` and `migrate`, and creates the admin user)
- **Start Command:** `gunicorn movie_theater_booking.wsgi:application`
- **Environment variables:** `DATABASE_URL`, `SECRET_KEY`, `PYTHON_VERSION`, and the `DJANGO_SUPERUSER_*` variables for the admin account
- Static files are served with WhiteNoise.
- `settings.py` reads `SECRET_KEY` and the database from environment variables, and uses the `RENDER_EXTERNAL_HOSTNAME` variable to configure `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`. Locally it falls back to SQLite with `DEBUG` on.

## Logging in to the live site
Username: grader
Password: throwaway
(Browsing movies works without logging in. Booking a seat and viewing My Bookings require login.)

## Known Limitations

- **A seat's booked status is global.** `Seat.is_booked` is a single flag that is not tied to a movie or showtime, so booking a seat for one movie makes it unavailable for every movie. A more realistic design would add a Showtime model and check bookings per showtime.
- Bookings cannot currently be cancelled from the web interface (they can be deleted through the API).
- The movie and seat API endpoints have no permission checks, so anyone can create, edit, or delete movies and seats. Booking endpoints require login and only expose a user's own bookings.
- The free Render tier sleeps when idle

## AI Usage Disclosure

I used **Claude (Anthropic)** as a guide while completing this assignment. It was used for:

- **Project setup guidance:** explaining Django project and app structure, virtual environments, `.gitignore`, and git troubleshooting.
- **Models:** guidance on field types and `on_delete` behavior for `Movie`, `Seat`, and `Booking`. I wrote the models, and Claude reviewed them and supplied the final `Booking` class.
- **Serializers and viewsets:** explanations of serializers, `Meta`, viewsets, and routers. Claude provided the booking validation (`validate_seat`) and `perform_create` logic with `transaction.atomic()`.
- **Templates and views:** the Bootstrap `base.html` with navbar, the `seat_booking.html` and `booking_history.html` templates, and the `book_seat` view.
- **Settings and debugging:** help diagnosing errors 
- **Testing:** the unit tests, API integration tests, and Behave feature and step files.
- **Deployment:** guidance on Render configuration, WhiteNoise, PostgreSQL via `dj-database-url`, `build.sh`, and `requirements.txt`, based on Render's Django deployment guide.
- **UI:** the Bootswatch theme, icon, and card-grid markup for the templates.
- **Sample data:** the 'seed_movies' management command and its sample movie descriptions.
- **Bug fixes:** 'perform_destroy' to free seats on cancellation, and disabiling booking edits.
- **Review:** used Paradot to review work.

I reviewed, ran, and tested all AI-generated code and fixed errors that came up while integrating it.