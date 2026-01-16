import pytest
from app.text_utils import normalize_whitespace, is_valid_slug


def test_normalize_whitespace_collapses_and_trims():
    assert normalize_whitespace("  hello   world \n") == "hello world"


def test_normalize_whitespace_none_raises():
    with pytest.raises(ValueError, match="text cannot be None"):
        normalize_whitespace(None)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "value,expected",
    [
        ("hello", True),
        ("hello-world", True),
        ("hello-world-2", True),
        ("Hello", False),
        ("hello_world", False),
        ("-hello", False),
        ("hello-", False),
        ("", False),
        (None, False),
    ],
)
def test_is_valid_slug(value, expected):
    assert is_valid_slug(value) is expected
