#!/usr/bin/env python3
"""
Password Generator (Python)

- Cryptographically strong randomness via `secrets`
- Guarantees at least one character from each selected set
- No whitespace in specials; configurable allowed symbols
- Interactive CLI by default; also supports non-interactive flags
- No data is stored anywhere

Quick start:
    python password_generator.py

Examples (non-interactive):
    python password_generator.py -l 20 --num 3 --exclude-ambiguous
    python password_generator.py --no-symbols --length 24
"""

from __future__ import annotations

import argparse
import sys
import textwrap
from dataclasses import dataclass
from typing import Dict, List
import secrets
import string
import random  # Using SystemRandom for secure shuffling only


DEFAULT_LENGTH = 16
DEFAULT_NUM = 1
DEFAULT_SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?/"  # no whitespace
AMBIGUOUS = set("Il1O0o")  # common ambiguous characters


@dataclass(frozen=True)
class CharSets:
    lowercase: str
    uppercase: str
    digits: str
    symbols: str

    def selected_sets(self, use_lower: bool, use_upper: bool, use_digits: bool, use_symbols: bool) -> Dict[str, str]:
        selected = {}
        if use_lower and self.lowercase:
            selected["lowercase"] = self.lowercase
        if use_upper and self.uppercase:
            selected["uppercase"] = self.uppercase
        if use_digits and self.digits:
            selected["digits"] = self.digits
        if use_symbols and self.symbols:
            selected["symbols"] = self.symbols
        return selected


def build_charsets(allowed_symbols: str, exclude_ambiguous: bool) -> CharSets:
    def filt(s: str) -> str:
        # remove whitespace and optionally ambiguous characters
        s = "".join(ch for ch in s if not ch.isspace())
        if exclude_ambiguous:
            s = "".join(ch for ch in s if ch not in AMBIGUOUS)
        return s

    lowercase = filt(string.ascii_lowercase)
    uppercase = filt(string.ascii_uppercase)
    digits = filt(string.digits)
    symbols = filt(allowed_symbols)
    return CharSets(lowercase, uppercase, digits, symbols)


def generate_password(
    length: int,
    use_lower: bool = True,
    use_upper: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
    allowed_symbols: str = DEFAULT_SYMBOLS,
    exclude_ambiguous: bool = True,
    ensure_each_selected: bool = True,
) -> str:
    """
    Generate a single password.

    Ensures at least one character from each selected set when ensure_each_selected is True.
    """
    if length <= 0:
        raise ValueError("Length must be positive.")

    charsets = build_charsets(allowed_symbols, exclude_ambiguous)
    selected = charsets.selected_sets(use_lower, use_upper, use_digits, use_symbols)

    if not selected:
        raise ValueError("No character sets selected. Enable at least one of: lower/upper/digits/symbols.")

    if ensure_each_selected and length < len(selected):
        raise ValueError(
            f"Length {length} is too short for {len(selected)} selected sets. "
            f"Use length ≥ {len(selected)}."
        )

    # Build initial pool and ensure at least one from each selected set
    pool = "".join(selected.values())
    if not pool:
        raise ValueError("Empty pool after applying filters; adjust your options/symbols.")

    password_chars: List[str] = []
    if ensure_each_selected:
        for charset in selected.values():
            password_chars.append(secrets.choice(charset))

    remaining = length - len(password_chars)
    for _ in range(remaining):
        password_chars.append(secrets.choice(pool))

    # Secure shuffle so the guaranteed chars aren't predictable in position
    rng = random.SystemRandom()
    rng.shuffle(password_chars)

    return "".join(password_chars)


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cryptographically strong password generator using Python's secrets.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("-l", "--length", type=int, default=DEFAULT_LENGTH, help=f"Password length (default: {DEFAULT_LENGTH})")
    parser.add_argument("--num", type=int, default=DEFAULT_NUM, help=f"How many passwords to generate (default: {DEFAULT_NUM})")

    group = parser.add_argument_group("character sets")
    group.add_argument("--no-lowercase", action="store_true", help="Exclude lowercase letters")
    group.add_argument("--no-uppercase", action="store_true", help="Exclude uppercase letters")
    group.add_argument("--no-digits", action="store_true", help="Exclude digits")
    group.add_argument("--no-symbols", action="store_true", help="Exclude symbols")
    group.add_argument("--symbols", type=str, default=DEFAULT_SYMBOLS,
                       help=f"Allowed symbols (no whitespace). Default: {DEFAULT_SYMBOLS}")

    parser.add_argument("--include-ambiguous", action="store_true",
                        help=f"Include ambiguous characters like: {''.join(sorted(AMBIGUOUS))}")
    parser.add_argument("--no-ensure-each", action="store_true",
                        help="Do NOT guarantee at least one character from each selected set")

    parser.add_argument("-y", "--yes", action="store_true",
                        help="Non-interactive: accept all defaults implied by flags (skip prompts).")

    return parser.parse_args(argv)


def prompt_bool(prompt: str, default: bool = True) -> bool:
    suffix = "[Y/n]" if default else "[y/N]"
    while True:
        resp = input(f"{prompt} {suffix} ").strip().lower()
        if not resp:
            return default
        if resp in {"y", "yes"}:
            return True
        if resp in {"n", "no"}:
            return False
        print("Please enter 'y' or 'n'.")


def prompt_int(prompt: str, default: int, min_value: int = 1) -> int:
    while True:
        raw = input(f"{prompt} [{default}] ").strip()
        if not raw:
            return default
        try:
            val = int(raw)
            if val < min_value:
                print(f"Please enter an integer ≥ {min_value}.")
                continue
            return val
        except ValueError:
            print("Please enter a valid integer.")


def interactive_wizard() -> argparse.Namespace:
    print(textwrap.dedent(f"""
    === Password Generator ===
    - Crypto-strong randomness via secrets
    - Guarantees at least one character from each selected set
    - No whitespace in symbols
    """).strip())

    length = prompt_int("Password length", DEFAULT_LENGTH, min_value=4)
    num = prompt_int("How many passwords?", DEFAULT_NUM, min_value=1)

    use_lower = prompt_bool("Include lowercase?", True)
    use_upper = prompt_bool("Include uppercase?", True)
    use_digits = prompt_bool("Include digits?", True)
    use_symbols = prompt_bool("Include symbols?", True)

    symbols = DEFAULT_SYMBOLS
    if use_symbols:
        custom = input(f"Allowed symbols (Enter for default: {DEFAULT_SYMBOLS}): ").strip()
        if custom:
            symbols = "".join(ch for ch in custom if not ch.isspace())

    exclude_ambiguous = prompt_bool("Exclude ambiguous characters (l, I, 1, O, 0, o)?", True)
    ensure_each = prompt_bool("Guarantee at least one from each selected set?", True)

    ns = argparse.Namespace(
        length=length,
        num=num,
        no_lowercase=not use_lower,
        no_uppercase=not use_upper,
        no_digits=not use_digits,
        no_symbols=not use_symbols,
        symbols=symbols,
        include_ambiguous=not exclude_ambiguous,
        no_ensure_each=not ensure_each,
        yes=True,  # already answered prompts
    )
    return ns


def main(argv: List[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    args = parse_args(argv)

    # If no -y/--yes and the user supplied no flags beyond defaults, run interactive wizard
    ran_interactive = False
    if not args.yes and argv == []:
        args = interactive_wizard()
        ran_interactive = True

    use_lower = not args.no_lowercase
    use_upper = not args.no_uppercase
    use_digits = not args.no_digits
    use_symbols = not args.no_symbols
    exclude_ambiguous = not args.include_ambiguous
    ensure_each = not args.no_ensure_each

    try:
        # Validate before generation
        tmp_charsets = build_charsets(args.symbols, exclude_ambiguous)
        selected = tmp_charsets.selected_sets(use_lower, use_upper, use_digits, use_symbols)
        if not selected:
            raise ValueError("No character sets selected. Enable at least one of: lower/upper/digits/symbols.")
        if ensure_each and args.length < len(selected):
            raise ValueError(
                f"Length {args.length} is too short for {len(selected)} selected sets. "
                f"Use length ≥ {len(selected)}."
            )
        if not tmp_charsets.symbols and use_symbols:
            raise ValueError("Your allowed symbols filtered to empty. Provide at least one non-whitespace symbol.")

        for i in range(args.num):
            pwd = generate_password(
                length=args.length,
                use_lower=use_lower,
                use_upper=use_upper,
                use_digits=use_digits,
                use_symbols=use_symbols,
                allowed_symbols=args.symbols,
                exclude_ambiguous=exclude_ambiguous,
                ensure_each_selected=ensure_each,
            )
            print(pwd)

        if ran_interactive:
            print("\nDone. (Nothing was stored.)")

        return 0

    except KeyboardInterrupt:
        print("\nAborted by user.", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
