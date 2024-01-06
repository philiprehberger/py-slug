"""URL slug generation with transliteration and uniqueness."""

from __future__ import annotations

import re
import unicodedata


__all__ = [
    "ReservedSlugError",
    "slugify",
    "slug_from_parts",
    "unique_slugify",
    "strip_html",
]


class ReservedSlugError(ValueError):
    """Raised when a generated slug matches a reserved word."""

    def __init__(self, slug: str, reserved: list[str]) -> None:
        self.slug = slug
        self.reserved = reserved
        super().__init__(
            f"Slug {slug!r} is reserved. Reserved slugs: {reserved}"
        )


TRANSLITERATION_MAP: dict[str, str] = {
    "\u00df": "ss",
    "\u00e6": "ae",
    "\u00c6": "AE",
    "\u0153": "oe",
    "\u0152": "OE",
    "\u00f8": "o",
    "\u00d8": "O",
    "\u00f0": "d",
    "\u00d0": "D",
    "\u00fe": "th",
    "\u00de": "TH",
    "\u0111": "d",
    "\u0110": "D",
    "\u0142": "l",
    "\u0141": "L",
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
    reserved: list[str] | None = None,
    transliterate: dict[str, str] | None = None,
) -> str:
    """Generate a URL-safe slug from the given text.

    Args:
        text: Input text to slugify.
        separator: Character used between words. Defaults to ``"-"``.
        max_length: Maximum slug length. 0 means no limit.
            Truncation respects word boundaries.
        lowercase: Whether to lowercase the result.
        reserved: List of reserved slugs. Raises ``ReservedSlugError`` if the
            generated slug matches any reserved word.
        transliterate: Custom transliteration map merged with built-in defaults.
            User-provided mappings take precedence over built-in ones.

    Returns:
        A URL-safe slug string.

    Raises:
        ReservedSlugError: If the generated slug matches a reserved word.
    """
    merged_map = {**TRANSLITERATION_MAP, **(transliterate or {})}

    for char, replacement in merged_map.items():
        text = text.replace(char, replacement)

    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    if lowercase:
        text = text.lower()

    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", separator, text).strip(separator)

    if max_length > 0 and len(text) > max_length:
        text = _truncate_at_word(text, max_length, separator)

    if reserved is not None:
        reserved_lower = [r.lower() for r in reserved]
        if text.lower() in reserved_lower:
            raise ReservedSlugError(text, reserved)

    return text


def slug_from_parts(*parts: str, separator: str = "-") -> str:
    """Join multiple strings into a single slug with deduplication of separators.

    Each part is individually slugified and then joined with the separator.
    Empty parts are skipped. Consecutive separators are collapsed.

    Args:
        *parts: Strings to join into a slug.
        separator: Character used between parts. Defaults to ``"-"``.

    Returns:
        A URL-safe slug built from all parts.
    """
    slugified_parts = [slugify(part, separator=separator) for part in parts]
    filtered = [p for p in slugified_parts if p]
    joined = separator.join(filtered)
    sep_escaped = re.escape(separator)
    joined = re.sub(f"{sep_escaped}{{2,}}", separator, joined)
    return joined.strip(separator)


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
