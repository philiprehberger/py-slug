# philiprehberger-slug

[![Tests](https://github.com/philiprehberger/py-slug/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-slug/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-slug.svg)](https://pypi.org/project/philiprehberger-slug/)
[![Last updated](https://img.shields.io/github/last-commit/philiprehberger/py-slug)](https://github.com/philiprehberger/py-slug/commits/main)

URL slug generation with transliteration and uniqueness.

## Installation

```bash
pip install philiprehberger-slug
```

## Usage

```python
from philiprehberger_slug import slugify

slugify("Hello World!")        # "hello-world"
slugify("Ünïcödé Têxt")       # "unicode-text"
slugify("Straße nach München") # "strasse-nach-munchen"
```

### Options

```python
from philiprehberger_slug import slugify

slugify("Hello World", separator="_")    # "hello_world"
slugify("Hello World", max_length=8)     # "hello"
slugify("Hello World", lowercase=False)  # "Hello-World"
```

### Reserved Slug Blocking

```python
from philiprehberger_slug import slugify, ReservedSlugError

try:
    slugify("Admin", reserved=["admin", "api", "about"])
except ReservedSlugError as e:
    print(e)  # "Slug 'admin' is reserved. Reserved slugs: ['admin', 'api', 'about']"
```

### Custom Transliteration

```python
from philiprehberger_slug import slugify

slugify("Ölkörper", transliterate={"ö": "oe", "ü": "ue"})  # "oelkoerper"
```

### Slug from Parts

```python
from philiprehberger_slug import slug_from_parts

slug_from_parts("2026", "03", "my post title")  # "2026-03-my-post-title"
slug_from_parts("Blog", "Straße & Weg")         # "blog-strasse-and-weg"
```

### Unique Slugs

```python
from philiprehberger_slug import unique_slugify

existing = {"hello-world", "hello-world-2"}
unique_slugify("Hello World", existing)  # "hello-world-3"
```

### Validate a slug

```python
from philiprehberger_slug import is_valid_slug

is_valid_slug("hello-world")    # True
is_valid_slug("Hello World")    # False
is_valid_slug("--bad--")        # False
is_valid_slug("hello_world", separator="_")  # True
```

### Strip HTML

```python
from philiprehberger_slug import strip_html

strip_html("<p>Hello <b>World</b></p>")  # "Hello World"
```

## API

| Function / Class | Description |
|------------------|-------------|
| `slugify(text, separator, max_length, lowercase, reserved, transliterate)` | Generate a URL-safe slug from text |
| `slug_from_parts(*parts, separator)` | Join multiple strings into a single slug |
| `unique_slugify(text, existing, separator, max_length)` | Generate a unique slug with numeric suffix |
| `is_valid_slug(text, separator)` | Return `True` if `text` is already in canonical slug form |
| `strip_html(text)` | Remove HTML tags from text |
| `ReservedSlugError` | Raised when a slug matches a reserved word |

## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## Support

If you find this project useful:

⭐ [Star the repo](https://github.com/philiprehberger/py-slug)

🐛 [Report issues](https://github.com/philiprehberger/py-slug/issues?q=is%3Aissue+is%3Aopen+label%3Abug)

💡 [Suggest features](https://github.com/philiprehberger/py-slug/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)

❤️ [Sponsor development](https://github.com/sponsors/philiprehberger)

🌐 [All Open Source Projects](https://philiprehberger.com/open-source-packages)

💻 [GitHub Profile](https://github.com/philiprehberger)

🔗 [LinkedIn Profile](https://www.linkedin.com/in/philiprehberger)

## License

[MIT](LICENSE)
