import pytest

from philiprehberger_slug import (
    ReservedSlugError,
    slugify,
    slug_from_parts,
    unique_slugify,
    strip_html,
)


def test_basic_slugify():
    assert slugify("Hello World!") == "hello-world"


def test_unicode_transliteration():
    assert slugify("Straße") == "strasse"


def test_custom_separator():
    assert slugify("Hello World", separator="_") == "hello_world"


def test_max_length():
    result = slugify("Hello beautiful world", max_length=8)
    assert len(result) <= 8


def test_no_lowercase():
    assert slugify("Hello World", lowercase=False) == "Hello-World"


def test_special_chars():
    assert slugify("foo & bar @ baz") == "foo-and-bar-at-baz"


def test_accented_chars():
    result = slugify("café résumé")
    assert "cafe" in result
    assert "resume" in result


def test_unique_slugify_no_conflict():
    result = unique_slugify("Hello World", set())
    assert result == "hello-world"


def test_unique_slugify_with_conflict():
    existing = {"hello-world"}
    result = unique_slugify("Hello World", existing)
    assert result == "hello-world-2"


def test_unique_slugify_multiple_conflicts():
    existing = {"hello-world", "hello-world-2", "hello-world-3"}
    result = unique_slugify("Hello World", existing)
    assert result == "hello-world-4"


def test_strip_html():
    assert strip_html("<p>Hello <b>World</b></p>") == "Hello World"


def test_strip_html_no_tags():
    assert strip_html("plain text") == "plain text"


def test_empty_string():
    assert slugify("") == ""


def test_only_special_chars():
    assert slugify("!!!") == ""


# --- Reserved slug tests ---


def test_reserved_slug_raises_error():
    with pytest.raises(ReservedSlugError) as exc_info:
        slugify("Admin", reserved=["admin", "api", "about"])
    assert exc_info.value.slug == "admin"
    assert exc_info.value.reserved == ["admin", "api", "about"]


def test_reserved_slug_case_insensitive():
    with pytest.raises(ReservedSlugError):
        slugify("API", reserved=["admin", "api"])


def test_reserved_slug_no_match_passes():
    result = slugify("hello-world", reserved=["admin", "api"])
    assert result == "hello-world"


def test_reserved_slug_empty_list():
    result = slugify("admin", reserved=[])
    assert result == "admin"


def test_reserved_slug_none_default():
    result = slugify("admin")
    assert result == "admin"


# --- Custom transliteration tests ---


def test_custom_transliteration():
    result = slugify("Ölkörper", transliterate={"ö": "oe", "Ö": "Oe"})
    assert result == "oelkoerper"


def test_custom_transliteration_overrides_builtin():
    # Built-in maps ß -> ss; custom overrides to sz
    result = slugify("Straße", transliterate={"ß": "sz"})
    assert result == "strasze"


def test_custom_transliteration_with_new_chars():
    result = slugify("price is 5€", transliterate={"€": "euro"})
    assert result == "price-is-5euro"


def test_custom_transliteration_merges_with_builtin():
    # ü is not in the built-in map but ß is
    result = slugify("Straße über", transliterate={"ü": "ue"})
    assert result == "strasse-ueber"


def test_custom_transliteration_empty_map():
    result = slugify("Straße", transliterate={})
    assert result == "strasse"


# --- slug_from_parts tests ---


def test_slug_from_parts_basic():
    result = slug_from_parts("Hello", "World")
    assert result == "hello-world"


def test_slug_from_parts_multiple():
    result = slug_from_parts("2026", "03", "my post title")
    assert result == "2026-03-my-post-title"


def test_slug_from_parts_custom_separator():
    result = slug_from_parts("Hello", "World", separator="_")
    assert result == "hello_world"


def test_slug_from_parts_deduplicates_separators():
    result = slug_from_parts("hello-", "-world")
    assert result == "hello-world"


def test_slug_from_parts_skips_empty():
    result = slug_from_parts("hello", "", "world")
    assert result == "hello-world"


def test_slug_from_parts_single():
    result = slug_from_parts("Hello World!")
    assert result == "hello-world"


def test_slug_from_parts_all_empty():
    result = slug_from_parts("", "", "")
    assert result == ""


def test_slug_from_parts_with_special_chars():
    result = slug_from_parts("Blog", "Straße & Weg")
    assert result == "blog-strasse-and-weg"
