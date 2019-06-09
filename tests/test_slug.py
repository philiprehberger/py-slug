from philiprehberger_slug import slugify, unique_slugify, strip_html


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
