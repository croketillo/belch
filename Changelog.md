# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2026-03-14

### Changed
- Unified pattern parsing into a single `_parse_pattern()` function. Previously,
  `generate_single()` and `calculate_combinations()` each parsed the pattern
  independently, duplicating logic and risking inconsistencies.
- Merged the two internal token dictionaries (`_translate_token` and
  `_token_combinations`) into a single module-level constant `TOKEN_MAP`.
  Combination counts are now derived directly from `len(set(pool))`, eliminating
  the redundant mapping.
- Fixed a bug in `calculate_combinations()` where consecutive repeated tokens
  (e.g. `/d/d/d`) could cause the loop index to desynchronize, producing
  incorrect combination counts.
- Replaced per-line file writes with a single buffered `write()` call, improving
  performance significantly for large password lists.
- Extracted time formatting logic into a dedicated `format_duration()` helper,
  removing the verbose `if/elif/else` block from `main()`.
- Migrated packaging from `setup.py` to `pyproject.toml`.
- Updated supported Python versions to 3.10, 3.11 and 3.12.

### Added
- Docstrings on `PasswordGenerator` and its public methods.
- Type annotations throughout the codebase.

