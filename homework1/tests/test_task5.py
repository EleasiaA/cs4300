import task5

def test_book_list_has_titles_and_authors():
    #checks the list isn't empty and every entry has titles and authors
    assert len(task5.FAVORITE_BOOKS) >= 3
    for title, author in task5.FAVORITE_BOOKS:
        assert title and author

def test_first_three_books():
    #confirms slicing returns exactly 3 items
    result = task5.first_three_books()
    assert len(result) == 3
    assert result == task5.FAVORITE_BOOKS[:3]

def test_first_three_books_short_list():
    #if the list has fewer than three books
    #Passing a custom 1-book list checks that slicing doesn't error
    assert task5.first_three_books([("A", "X")]) == [("A", "X")]

def test_student_lookup():
    assert task5.get_student_id("Alice") == 1001

def test_student_missing_returns_none():
    assert task5.get_student_id("Nobody") is None

def test_student_ids_are_unique():
    #removes any possible duplicates
    ids = list(task5.STUDENTS.values())
    assert len(ids) == len(set(ids))

def test_main_output(capsys):
    task5.main()
    out = capsys.readouterr().out
    assert "The Hobbit by J.R.R. Tolkien" in out
    assert "Alice" in out