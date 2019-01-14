"""URL slug generation with transliteration and uniqueness."""

from __future__ import annotations

import re
import unicodedata


__all__ = [
    "slugify",
    "unique_slugify",
    "strip_html",
]

TRANSLITERATION_MAP: dict[str, str] = {
    "ß": "ss",
    "æ": "ae",
    "Æ": "AE",
    "œ": "oe",
    "Œ": "OE",
    "ø": "o",
    "Ø": "O",
    "ð": "d",
    "Ð": "D",
    "þ": "th",
    "Þ": "TH",
    "đ": "d",
    "Đ": "D",
    "ł": "l",
    "Ł": "L",
    "&": "and",
    "@": "at",
    "+": "plus",
    "%": "percent",
}

_HTML_TAG_RE = re.compile(r"<[^>]+>")


def slugify(
    text: str,
    separator: str = "-",
    max_length: int = 0,
    lowercase: bool = True,
) -> str:
    """Generate a URL-safe slug from the given text.

    Args:
        text: Input text to slugify.
        separator: Character used between words. Defaults to ``"-"``.
        max_length: Maximum slug length. 0 means no limit.
            Truncation respects word boundaries.
        lowercase: Whether to lowercase the result.

    Returns:
        A URL-safe slug string.
    """
    for char, replacement in TRANSLITERATION_MAP.items():
        text = text.replace(char, replacement)

    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    if lowercase:
        text = text.lower()

    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", separator, text).strip(separator)

    if max_length > 0 and len(text) > max_length:
        text = _truncate_at_word(text, max_length, separator)

    return text


def _truncate_at_word(text: str, max_length: int, separator: str) -> str:
    truncated = text[:max_length]
    last_sep = truncated.rfind(separator)
    if last_sep > 0:
        truncated = truncated[:last_sep]
    return truncated.rstrip(separator)


def unique_slugify(
    text: str,
    existing: set[str] | list[str],
    separator: str = "-",
    max_length: int = 0,
) -> str:
    """Generate a unique slug by appending a numeric suffix if needed.

    Args:
        text: Input text to slugify.
        existing: Collection of slugs that already exist.
        separator: Character used between words.
        max_length: Maximum slug length. 0 means no limit.

    Returns:
        A unique slug not present in ``existing``.
    """
    existing_set = set(existing)
    base = slugify(text, separator=separator, max_length=max_length)

    if base not in existing_set:
        return base

    counter = 2
    while True:
        suffix = f"{separator}{counter}"
        if max_length > 0:
            candidate = slugify(text, separator=separator, max_length=max_length - len(suffix))
            candidate = f"{candidate}{suffix}"
        else:
            candidate = f"{base}{suffix}"

        if candidate not in existing_set:
            return candidate
        counter += 1


def strip_html(text: str) -> str:
    """Remove HTML tags from text.

    Args:
        text: HTML string to strip.

    Returns:
        Text with all HTML tags removed.
    """
    return _HTML_TAG_RE.sub("", text)
