"""Task 6: File Handling - count words in task6_read_me.txt"""

from pathlib import Path 

#makes sure code can be ran relative to the scripts own location
DEFAULT_FILE = Path(__file__).resolve().parent.parent / "task6_read_me.txt"

def count_words(path=DEFAULT_FILE):
    #Return number of whitespace-separated words in a text fule
    #Raises: FileNotFoundError: if the file does not exist

    with open(path, "r", encoding="utf-8") as f:
        return len(f.read().split())

if __name__ == "__main__":
    print(f"Word count: {count_words()}")

