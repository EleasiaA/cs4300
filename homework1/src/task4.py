"""Task 4: Functions and duck typing """
from numbers import Real

def calculate_discount(price, discount):
    """Return the price after applying a percentage discount
    
    Any real numeric type works, because behavior is checked, rather than a specific type
    like 'int' or 'float'

    Original price, must be >=0
    Discount percentage, must be between 0 and 100

    Raises:
        TypeError: if either argument is not a real number
        ValueError: if price is negative or discount is outside 0 -100.

     """

    for name, value in (("price", price), ("discount", discount)):
        if isinstance(value, bool) or not isinstance(value, Real):
            raise TypeError(f"{name} must be a real number, got {type(value).__name__}")

    if price < 0:
        raise ValueError("price must be non-negative")
    if not 0 <= discount <= 100:
        raise ValueError("discount must be between 0 and 100")
    return price - price * discount / 100

if __name__ == "__main__":
    print(calculate_discount(100, 20))      #80.0
    print(calculate_discount(59.99, 12.5))  #52.49125
