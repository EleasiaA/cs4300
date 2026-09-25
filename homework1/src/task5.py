""" Task 5: Lists and Dictionaries """

FAVORITE_BOOKS = [

    ("The Hobbit", "J.R.R. Tolkien"),
    ("Dune", "Frank Herbert"),
    ("1984", "George Orwell"),
    ("Neuromancer", "William Gibson"),
    ("Project Hail Mary", "Andy Weir")
]

STUDENTS = {
    "Alice": 1001,
    "Bob": 1002,
    "Carmen": 1003,
}

def first_three_books(books=FAVORITE_BOOKS):
    #Return the first three books using list slicing
    return books[:3]

def get_student_id(name, db=STUDENTS):
    #Return the student ID for 'name', or None if not found.
    return db.get(name)

def main():
    for title, author in first_three_books():
        print(f"{title} by {author}")
    print(STUDENTS)

if __name__ == "__main__":
    main()
