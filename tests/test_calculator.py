import pytest
from app.calculator import add, divide


def test_add():
    assert add(2, 3) == 5


def test_divide_ok():
    assert divide(10, 2) == 5


def test_divide_by_zero_raises():
    with pytest.raises(ValueError, match="division by zero"):
        divide(1, 0)
