import pytest
import task7

def test_summarize_basic():
	#checks if mean and median are both 3 and std
	result = task7.summarize([1, 2, 3, 4, 5])
	assert result["mean"] == pytest.approx(3.0)
	assert result["median"] == pytest.approx(3.0)
	assert result["std"] == pytest.approx(2 ** 0.5)

@pytest.mark.parametrize(
	"values, mean, median",
    [([10], 10, 10), ([1, 1, 1, 1], 1, 1), ([1, 2, 3, 100], 26.5, 2.5), ((2.5, 3.5), 3.0, 3.0)],
)

def test_summarize_parametrized(values, mean, median):
	#covers a single value, all-identical values, and a list where mean and median diverge a lot
	result = task7.summarize(values)
	assert result["mean"] == pytest.approx(mean)
	assert result["median"] == pytest.approx(median)

def test_summarize_empty_raises():
	#checks the ValueError guards against an empty list
	with pytest.raises(ValueError):
		task7.summarize([])
