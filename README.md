# philiprehberger-slug

[![Tests](https://github.com/philiprehberger/py-slug/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-slug/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-slug.svg)](https://pypi.org/project/philiprehberger-slug/)
[![License](https://img.shields.io/github/license/philiprehberger/py-slug)](LICENSE)

URL slug generation with transliteration and uniqueness.

## Installation

```bash
pip install philiprehberger-slug
```

## Usage

### Basic Slugification

```python
from philiprehberger_slug import slugify

slugify("Hello World!")        # "hello-world"
slugify("Ünïcödé Têxt")       # "unicode-text"
slugify("Straße nach München") # "strasse-nach-munchen"
```

### Options

```python
slugify("Hello World", separator="_")    # "hello_world"
slugify("Hello World", max_length=8)     # "hello"
slugify("Hello World", lowercase=False)  # "Hello-World"
```

### Unique Slugs

```python
from philiprehberger_slug import unique_slugify

existing = {"hello-world", "hello-world-2"}
unique_slugify("Hello World", existing)  # "hello-world-3"
```

### Strip HTML

```python
from philiprehberger_slug import strip_html

strip_html("<p>Hello <b>World</b></p>")  # "Hello World"
```

## API

- `slugify(text, separator="-", max_length=0, lowercase=True)` — Generate a URL-safe slug
- `unique_slugify(text, existing, separator="-", max_length=0)` — Generate a unique slug with numeric suffix
- `strip_html(text)` — Remove HTML tags from text


## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## License

MIT
