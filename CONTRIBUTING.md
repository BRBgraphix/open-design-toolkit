# Contributing

Thank you for considering a contribution!

## Before you start

1. Search existing Issues to avoid duplicate reports.
2. For a significant feature, open an Issue first to discuss the proposal.
3. Keep changes focused and explain why they are useful to designers.

## Development setup

```bash
python -m venv .venv
# Activate the environment, then:
python -m pip install -r requirements.txt
```

## Checks

Run the test suite before submitting:

```bash
python -m unittest discover -s tests -v
```

## Pull requests

- Describe the problem and the solution.
- Include steps to reproduce a bug or test a feature.
- Update the README when user-facing behavior changes.
- Add or update tests where practical.
- Do not include private files, client artwork, credentials, or copyrighted assets you do not have permission to share.

## Code style

Prefer clear names, small functions, and helpful comments. Avoid adding dependencies unless they are needed.
