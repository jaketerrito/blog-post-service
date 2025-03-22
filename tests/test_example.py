import pytest


def add(a, b):
    return a + b


def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_true():
    """A trivial test that will always pass"""
    assert True


@pytest.mark.parametrize(
    "input_a, input_b, expected",
    [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
        (10, 20, 30),
    ],
)
def test_add_parametrized(input_a, input_b, expected):
    """Demonstrate pytest's parametrization feature"""
    result = add(input_a, input_b)
    assert result == expected
