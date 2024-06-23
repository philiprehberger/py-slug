# Changelog

## 0.2.1 (2026-03-31)

- Standardize README to 3-badge format with emoji Support section
- Update CI checkout action to v5 for Node.js 24 compatibility

## 0.2.0 (2026-03-28)

- Add reserved slug blocking via `reserved` parameter on `slugify()`
- Add `ReservedSlugError` exception for reserved slug matches
- Add custom transliteration map support via `transliterate` parameter on `slugify()`
- Add `slug_from_parts()` for joining multiple strings into a single slug
- Add `[tool.pytest.ini_options]` and `[tool.mypy]` to pyproject.toml
- Add .github issue templates, PR template, and dependabot config

## 0.1.4

- Add Development section to README

## 0.1.1

- Add project URLs to pyproject.toml

## 0.1.0 (2026-03-10)

- Initial release
- Unicode transliteration to ASCII
- Configurable separator and max length
- Unique slug generation with suffix
- HTML tag stripping
