"""Test Task 1 """
import task1

def test_hello_world(capsys):
    task1.main()
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!\n"