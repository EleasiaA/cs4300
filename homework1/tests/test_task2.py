import pytest
import task2 

"""Runs the same test function once per tuple in the list, so there are 
four separate test results from one function. """
@pytest.mark.parametrize(
    "func, expected_type",
    [
        (task2.task2_integer, int),
        (task2.task2_float, float),
        (task2.task2_string, str),
        (task2.task2_boolean, bool),
    ],
)

def test_data_types(func, expected_type):
    assert type(func()) is expected_type

def test_main_output(capsys):
    task2.main()
    out = capsys.readouterr().out
    for name in ("int", "float", "str", "bool"):
        assert name in out