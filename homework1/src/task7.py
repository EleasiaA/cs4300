"""Task 7: Package management - using NumPy. """
import numpy as np

def summarize(values):
	#Return mean, median, and standard deviation of a sequence of numbers
	#Raises: ValueError: if 'values' is empty

	arr = np.asarray(values, dtype=float)
	if arr.size == 0:
		raise ValueError("values must not be empty")
	return {
		"mean": float(np.mean(arr)),
		"median": float(np.median(arr)),
		"std": float(np.std(arr)),
	}

if __name__ == "__main__":
	print(summarize([1, 2, 3, 4, 5]))
