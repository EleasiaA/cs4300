from fractions import Fraction
import pytest
from task4 import calculate_discount
@pytest.mark.parametrize(
    "price, discount, expected",
    [

        (100, 20, 80),                 # int, int
        (100.0, 20, 80.0),             # float, int
        (100, 12.5, 87.5),             # int, float
        (59.99, 0, 59.99),             # no discount
        (50, 100, 0),                  # full discount
        (0, 50, 0),                    # free item
        (Fraction(200), Fraction(25), Fraction(150))  # duck typing in action
    ]
)

def test_valid_inputs(price, discount, expected):
    #mixes int/float combinations, which proves the duck typing actually works
    assert calculate_discount(price, discount) == pytest.approx(expected)

@pytest.mark.parametrize(
    "price, discount",
    [("100", 10), (100, "10"), (None, 10), (100, None), (True, 10), (100, False), ([100], 10)],
)
def test_invalid_types(price, discount):
    #checks that strings, None, lists, and bool values all raise TypeError
    with pytest.raises(TypeError):
        calculate_discount(price, discount)

@pytest.mark.parametrize("price, discount", [(-1, 10), (100, -5), (100, 101)])
def test_invalid_values(price, discount):
    #checks that a negative price or an out-of-range discount raises ValueError
    with pytest.raises(ValueError):
        calculate_discount(price, discount)