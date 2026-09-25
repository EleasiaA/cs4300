import pytest
import task3 

@pytest.mark.parametrize(
   
    "n, expected",
    [(5, "positive"),(0.1, "positive"), (-3, "negative"), (-0.5, "negative"), (0, "zero"), (0.0, "zero")],

)

def test_classify_number(n, expected):
    #parameterized over positive, negative and zero, including a float and an int for each
    assert task3.classify_number(n) == expected

def test_first_ten_primes():
    assert task3.first_primes(10) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

@pytest.mark.parametrize("count, expected", [(0,[]),(1, [2]), (2, [2, 3])])

def test_first_primes_edge_cases (count, expected):
    #checks boundaries (count=0 should return an empty list)
    assert task3.first_primes(count) == expected

def test_sum_1_to_100():
    #has one obvious answer, so there is just one direct assertion
    assert task3.sum_1_to_100() == 5050

def test_main_output(capsys):
    #checks the full printed transcript line by line so it's not thrown off by exact spacing
    task3.main()
    lines = capsys.readouterr().out.splitlines()
    assert lines[0] == "positive negative zero"
    assert lines[1:11] == [str(p) for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)]
    assert lines[-1] == "5050"

