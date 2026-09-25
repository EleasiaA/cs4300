import pytest
import task6 

def test_default_file_word_count():
    assert task6.count_words() == 104

@pytest.mark.parametrize(
    "content, expected",
    [
        ("", 0),    #empty file has no words
        ("hello", 1),
        ("hello world", 2),         #confirm .split() handles whitespace correctly
        (" spaced out words ", 3),
        ("line one\nline two\n", 4),
        ("tabs\tand\nnewlines", 3),
    ],
)

def test_count_words_various_content(tmp_path, content, expected):
    f = tmp_path / "sample.txt" #tests a new temp directory that is cleaned afterward
    f.write_text(content, encoding="utf-8")
    assert task6.count_words(f) == expected

def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        task6.count_words(tmp_path / "nope.txt")