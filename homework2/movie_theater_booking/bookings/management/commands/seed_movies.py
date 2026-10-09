from datetime import date

from django.core.management.base import BaseCommand

from bookings.models import Movie, Seat

MOVIES = [
    ("The Shawshank Redemption", date(1994, 9, 23), 142,
     "A banker wrongly convicted of murder forms an unlikely friendship in prison while quietly planning his escape."),
    ("The Godfather", date(1972, 3, 24), 175,
     "The aging head of a crime family hands control to his reluctant youngest son, who is pulled into the family business."),
    ("The Dark Knight", date(2008, 7, 18), 152,
     "Batman faces the Joker, a chaotic criminal who pushes Gotham City and its defenders to their limits."),
    ("Pulp Fiction", date(1994, 10, 14), 154,
     "Interwoven stories of hitmen, a boxer, and a gangster's wife unfold across Los Angeles in this darkly funny crime tale."),
    ("Forrest Gump", date(1994, 7, 6), 142,
     "A kind-hearted man with a low IQ unknowingly takes part in several defining moments of American history."),
    ("Inception", date(2010, 7, 16), 148,
     "A thief who steals secrets from people's dreams is offered a chance to plant an idea instead."),
    ("The Matrix", date(1999, 3, 31), 136,
     "A hacker discovers his reality is a simulation and joins a rebellion against the machines that control it."),
    ("Interstellar", date(2014, 11, 7), 169,
     "With Earth dying, a former pilot leads a team through a wormhole in search of a new home for humanity."),
    ("Spirited Away", date(2001, 7, 20), 125,
     "A young girl wanders into a world of spirits and must work in a bathhouse to free her parents."),
    ("Parasite", date(2019, 5, 30), 132,
     "A struggling family schemes its way into the home of a wealthy household, with unexpected consequences."),
    ("Jurassic Park", date(1993, 6, 11), 127,
     "A theme park of cloned dinosaurs descends into chaos when its security systems fail."),
    ("Toy Story", date(1995, 11, 22), 81,
     "A cowboy doll's world is upended when a flashy new space ranger toy arrives in his owner's bedroom."),
    ("The Lion King", date(1994, 6, 24), 88,
     "A young lion prince flees his kingdom after his father's death, then returns to reclaim his place."),
    ("Back to the Future", date(1985, 7, 3), 116,
     "A teenager is accidentally sent to 1955 and must make sure his parents fall in love so he can exist."),
    ("Gladiator", date(2000, 5, 5), 155,
     "A betrayed Roman general is sold into slavery and fights his way through the arena to seek revenge."),
]


class Command(BaseCommand):
    help = "Add sample movies and seats if they don't already exist."

    def handle(self, *args, **options):
        for title, release, minutes, description in MOVIES:
            _, created = Movie.objects.get_or_create(
                title=title,
                defaults={"release_date": release, "duration": minutes,
                          "description": description},
            )
            if created:
                self.stdout.write(f"Added movie: {title}")

        for row in "ABCD":
            for number in range(1, 9):
                Seat.objects.get_or_create(seat_number=f"{row}{number}")

        self.stdout.write(self.style.SUCCESS("Seed data loaded."))