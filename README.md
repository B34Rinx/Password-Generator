# Password Generator (Python)

Cryptographically strong password generator using Python's `secrets`. Interactive CLI; nothing is stored.

## Features
- Cryptographically secure randomness (`secrets`) - not `random`
- Guarantees at least one character from each selected set
- No whitespace in specials; configurable allowed symbols
- Interactive CLI (no data stored)

## Requirements
- Python 3.10+ (recommended)

## Quick start
```bash
python password_generator.py
```

## Security notes
- Uses Python's `secrets` (crypto-strong)
- Ensures at least one character from each selected set
- No whitespace in specials; edit the allowed set if a site restricts symbols
- Prefer length >= 16; rotate if exposed

## Development
Create a virtual environment and run the script:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

python password_generator.py
```

## License
MIT — see `LICENSE`.
