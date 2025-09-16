# Password Generator (Python)

Cryptographically strong password generator using Python's `secrets`. Interactive CLI; nothing is stored.

## Features
- Cryptographically secure randomness (`secrets`) — not `random`
- Guarantees at least one character from each selected set
- No whitespace in specials; configurable allowed symbols
- Interactive CLI (no data stored)

## Requirements
- Python 3.10+ (recommended)
- No external packages needed

## Quick start
```bash
python3 Password_Generator.py
```
## Example (interactive)

> Demo only — the password below is a placeholder. Always generate your own.

```text
$ python3 Password_Generator.py
Enter password length: 16
Include which sets? (y/n)
Digits? [y/n]: y
Letters? [y/n]: y
Specials? [y/n]: y
Your password: <generated password appears here>
```

## Setup & Run (simple steps)

### Windows (PowerShell)
1. Create a virtual environment:
   ```powershell
   py -3 -m venv .venv
   ```
2. Activate it:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   > If activation is blocked, run in **Command Prompt** instead:
   > ```cmd
   > .\.venv\Scripts\activate.bat
   > ```
3. Run the generator:
   ```powershell
   python Password_Generator.py
   ```
4. When you're done:
   ```powershell
   deactivate
   ```

### macOS / Linux
1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```
2. Activate it:
   ```bash
   source .venv/bin/activate
   ```
3. Run the generator:
   ```bash
   python3 Password_Generator.py
   ```
4. When you're done:
   ```bash
   deactivate
   ```

> Tip: You can also run without a venv if you prefer:
> ```bash
> python3 Password_Generator.py
> ```

## Security notes
- Uses Python's `secrets` (crypto-strong)
- Ensures at least one character from each selected set
- No whitespace in specials; edit the allowed set if a site restricts symbols
- Prefer length ≥ 16; rotate if exposed

## License
MIT © 2025 Nalain R — see [LICENSE](LICENSE).
