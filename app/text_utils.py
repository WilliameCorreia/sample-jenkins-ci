from __future__ import annotations
import re


def normalize_whitespace(text: str) -> str:
    if text is None:
        raise ValueError("text cannot be None")
    return re.sub(r"\s+", " ", text).strip()


def is_valid_slug(value: str) -> bool:
    if value is None:
        return False
    return re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value) is not None
