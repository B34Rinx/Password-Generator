import string
import secrets


def secure_shuffle(items: list) -> None:
    """Fisher–Yates shuffle using secrets (no PRNG from random module)."""
    for i in range(len(items) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        items[i], items[j] = items[j], items[i]


def generate_password(
    length: int,
    use_digits: bool = True,
    use_letters: bool = True,
    use_special: bool = True,
    # all common login-allowed specials; no spaces
    specials: str = string.punctuation,
) -> str:
    if length <= 0:
        raise ValueError("length must be positive")

    # Build pools
    pools = []
    pool = ""

    if use_digits:
        pools.append(string.digits)
        pool += string.digits

    if use_letters:
        pools.append(string.ascii_letters)
        pool += string.ascii_letters

    if use_special:
        # ensure no whitespace even if specials is overridden
        specials = "".join(ch for ch in specials if not ch.isspace())
        if not specials:
            raise ValueError("specials set is empty after removing whitespace")
        pools.append(specials)
        pool += specials

    if not pool:
        raise ValueError("Select at least one character set")

    if length < len(pools):
        raise ValueError(
            f"length must be at least {len(pools)} to include one of each selected set")

    # Ensure at least one from each selected pool
    pwd_chars = [secrets.choice(s) for s in pools]
    # Fill the rest from the combined pool
    pwd_chars += [secrets.choice(pool) for _ in range(length - len(pwd_chars))]

    # Crypto-safe shuffle
    secure_shuffle(pwd_chars)
    return "".join(pwd_chars)


if __name__ == "__main__":
    # Simple interactive CLI
    try:
        length = int(input("Enter password length: "))
    except ValueError:
        raise SystemExit("Length must be an integer.")

    print("Include which sets? (y/n)")
    use_digits = input("Digits? [y/n]: ").strip().lower().startswith("y")
    use_letters = input("Letters? [y/n]: ").strip().lower().startswith("y")
    use_special = input("Specials? [y/n]: ").strip().lower().startswith("y")

    try:
        password = generate_password(
            length, use_digits, use_letters, use_special)
    except ValueError as e:
        raise SystemExit(f"Error: {e}")

    print("Your password:", password)
