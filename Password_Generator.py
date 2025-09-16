#!/usr/bin/env python3
# SPDX-License-Identifier: MIT

import string
import secrets

# Defaults
DEFAULT_LENGTH = 16
DEFAULT_NUM = 1
# Curated symbols (no whitespace, no quotes/backticks which some sites reject)
DEFAULT_SPECIALS = "!@#$%^&*()-_=+[]{};:,.?/"
AMBIGUOUS = set("Il1O0o")  # characters many people find confusing


def secure_shuffle(items: list) -> None:
    """Fisher–Yates shuffle using secrets (no PRNG from random)."""
    for i in range(len(items) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        items[i], items[j] = items[j], items[i]


def build_pools(use_digits: bool, use_letters: bool, use_special: bool,
                specials: str, exclude_ambiguous: bool) -> tuple[list[str], str]:
    """Return (pools_list, combined_pool_str) after filters."""
    pools = []
    combined = ""

    if use_digits:
        digits = string.digits
        if exclude_ambiguous:
            digits = "".join(ch for ch in digits if ch not in AMBIGUOUS)
        pools.append(digits)
        combined += digits

    if use_letters:
        letters = string.ascii_letters
        if exclude_ambiguous:
            letters = "".join(ch for ch in letters if ch not in AMBIGUOUS)
        pools.append(letters)
        combined += letters

    if use_special:
        # ensure no whitespace even if user typed some
        specials = "".join(ch for ch in specials if not ch.isspace())
        if not specials:
            raise ValueError("Specials set is empty after removing whitespace.")
        pools.append(specials)
        combined += specials

    if not combined:
        raise ValueError("Select at least one character set.")

    return pools, combined


def generate_password(length: int,
                      use_digits: bool = True,
                      use_letters: bool = True,
                      use_special: bool = True,
                      specials: str = DEFAULT_SPECIALS,
                      exclude_ambiguous: bool = True) -> str:
    """Generate one password; guarantees ≥1 char from each selected set."""
    if length <= 0:
        raise ValueError("Length must be positive.")

    pools, combined = build_pools(use_digits, use_letters, use_special, specials, exclude_ambiguous)

    if length < len(pools):
        raise ValueError(f"Length must be at least {len(pools)} to include one of each selected set.")

    # Ensure at least one from each selected pool
    pwd_chars = [secrets.choice(pool) for pool in pools]
    # Fill the rest from the combined pool
    pwd_chars += [secrets.choice(combined) for _ in range(length - len(pwd_chars))]

    # Crypto-safe shuffle so required chars aren't in predictable positions
    secure_shuffle(pwd_chars)
    return "".join(pwd_chars)


# ---- Minimal, friendly interactive CLI ----

def prompt_int(label: str, default: int, min_value: int = 1) -> int:
    while True:
        raw = input(f"{label} [{default}]: ").strip()
        if not raw:
            return default
        try:
            val = int(raw)
            if val < min_value:
                print(f"Please enter a number ≥ {min_value}.")
                continue
            return val
        except ValueError:
            print("Please enter a whole number.")


def prompt_bool(label: str, default: bool = True) -> bool:
    suffix = "Y/n" if default else "y/N"
    while True:
        raw = input(f"{label} ({suffix}): ").strip().lower()
        if raw == "":
            return default
        if raw in {"y", "yes"}:
            return True
        if raw in {"n", "no"}:
            return False
        print("Please answer y or n.")


if __name__ == "__main__":
    try:
        print("=== Password Generator (secrets) ===")
        length = prompt_int("Password length", DEFAULT_LENGTH, min_value=4)
        num = prompt_int("How many passwords", DEFAULT_NUM, min_value=1)

        use_digits = prompt_bool("Include digits?", True)
        use_letters = prompt_bool("Include letters (a-z, A-Z)?", True)
        use_special = prompt_bool("Include symbols?", True)

        specials = DEFAULT_SPECIALS
        if use_special and prompt_bool(f"Use custom symbols? (default: {DEFAULT_SPECIALS})", False):
            custom = input("Enter symbols (no spaces): ").strip()
            specials = "".join(ch for ch in custom if not ch.isspace())
            if not specials:
                raise SystemExit("Error: specials cannot be empty when symbols are enabled.")

        exclude_ambiguous = prompt_bool("Exclude ambiguous characters (I, l, 1, O, 0, o)?", True)

        for _ in range(num):
            print(generate_password(
                length=length,
                use_digits=use_digits,
                use_letters=use_letters,
                use_special=use_special,
                specials=specials,
                exclude_ambiguous=exclude_ambiguous,
            ))

        print("\nDone. (Nothing was stored.)")

    except KeyboardInterrupt:
        print("\nAborted.")
    except ValueError as e: 
        print(f"Error: {e}")
