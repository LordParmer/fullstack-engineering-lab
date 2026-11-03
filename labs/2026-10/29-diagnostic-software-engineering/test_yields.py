import pytest
from yields import average_yield


def test_ignores_missing_runs():
    assert average_yield({"run1": 42.0, "run2": None, "run3": 37.5}) == 39.75


def test_keeps_zero_values():
    assert average_yield({"a": 0.0, "b": 10.0, "c": None}) == 5.0


def test_no_measured_runs_raises():
    with pytest.raises(ValueError):
        average_yield({"run1": None, "run2": None})
