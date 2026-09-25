"""Task 2: Variables and data types."""
#return different data types

def task2_integer():
    return 14
        
def task2_float():
    return 2.56

def task2_string():
    return "Task2"

def task2_boolean():
    return True

def main():
    """Print each value and its type"""
    for value in (task2_integer(), task2_float(), task2_string(), task2_boolean()):
        print(f"{value!r} is of type {type(value).__name__}")

if __name__=="__main__":
    main()