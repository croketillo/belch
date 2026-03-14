from pathlib import Path
import random
import string
import sys
import time
from typing import List, Set, Tuple
from colorama import init, Style, Fore
from tinyprogress import progress


SPECIAL_CHARACTERS = "!@#$%^&*(),.?\":{}|<>_-+/;[]"

# Unified token map: token -> character pool
# Both generation and combination count derive from this single source of truth.
TOKEN_MAP: dict[str, str] = {
    "C": string.ascii_uppercase,
    "c": string.ascii_lowercase,
    "d": string.digits,
    "e": SPECIAL_CHARACTERS,
    "?": string.ascii_letters + string.digits + SPECIAL_CHARACTERS,
    "@": string.ascii_letters,
    "&": string.ascii_letters + string.digits,
}


def _parse_pattern(pattern: str) -> List[str | None]:
    """Parse a pattern string into a list of character pools or None for literals.

    Each element is either:
      - A string (the pool of characters to pick from for that position), or
      - A single literal character (returned as a one-char string pool with
        exactly that character, i.e. pool of size 1).
    """
    tokens: List[str] = []
    i = 0
    while i < len(pattern):
        char = pattern[i]
        if char == "/" and i + 1 < len(pattern):
            i += 1
            token = pattern[i]
            if token in TOKEN_MAP:
                tokens.append(TOKEN_MAP[token])
            else:
                # Unknown escape: treat as literal "/" + token
                tokens.append("/" + token)
        else:
            tokens.append(char)  # literal character (pool of exactly 1)
        i += 1
    return tokens


class PasswordGenerator:
    """Generates passwords according to a pattern string.

    Pattern tokens:
        /d  Digit
        /c  Lowercase letter
        /C  Uppercase letter
        /e  Special character
        /?  Any printable character (letters + digits + special)
        /@  Any letter (upper or lower)
        /&  Any letter or digit
    Any other character in the pattern is used as a literal.
    """

    def __init__(self, pattern: str):
        self.pattern = pattern.strip()
        # Parse once; reuse for both generation and combination count.
        self._pools: List[str] = _parse_pattern(self.pattern)

    def generate_single(self) -> str:
        """Generate a single password from the pattern."""
        return "".join(random.choice(pool) for pool in self._pools)

    def generate_multiple(self, count: int) -> List[str]:
        """Generate `count` unique passwords.

        Uses a set for O(1) duplicate detection. For counts near the theoretical
        maximum, the caller should be aware that generation may slow down.
        """
        max_possible = self.calculate_combinations()
        if count > max_possible:
            raise ValueError(
                f"Cannot generate {count} unique passwords. "
                f"Max possible is {max_possible}."
            )

        generated_passwords: Set[str] = set()
        try:
            for _ in progress(range(count), task_name="Generating passwords"):
                password = self.generate_single()
                while password in generated_passwords:
                    password = self.generate_single()
                generated_passwords.add(password)
        except KeyboardInterrupt:
            print(Fore.LIGHTRED_EX + "\n\n[!] " + Fore.RESET + "Interrupted. Saving progress...")
        return list(generated_passwords)

    def calculate_combinations(self) -> int:
        """Return the number of unique passwords the pattern can produce."""
        total = 1
        for pool in self._pools:
            total *= len(set(pool))  # use set() to deduplicate pool chars
        return total


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def format_duration(seconds: float) -> str:
    """Return a human-readable duration string."""
    if seconds > 3600:
        h, rem = divmod(seconds, 3600)
        m, s = divmod(rem, 60)
        return f"{int(h)}h {int(m)}m {s:.2f}s"
    if seconds > 60:
        m, s = divmod(seconds, 60)
        return f"{int(m)}m {s:.2f}s"
    return f"{seconds:.2f}s"


def calculate_weight(n_lines: int, line_length: int) -> str:
    """Return a human-readable file size estimate."""
    total_bytes = (line_length + 1) * n_lines  # +1 for newline
    mb = total_bytes / (1024 * 1024)
    gb = mb / 1024
    if gb >= 1:
        return f"{gb:.2f} GB"
    if mb >= 0.01:
        return f"{mb:.2f} MB"
    return f"{total_bytes} bytes"


def get_integer_input(prompt: str, max_value: int) -> int:
    """Prompt the user for an integer in [1, max_value]. Enter returns max_value."""
    while True:
        try:
            value = input(prompt)
            if value:
                value = int(value)
                if 0 < value <= max_value:
                    return value
                print(Fore.LIGHTRED_EX + "[!] " + Fore.RESET + f"Enter a number between 1 and {max_value}.")
            else:
                return max_value
        except ValueError:
            print(Fore.LIGHTRED_EX + "[!] " + Fore.RESET + "Invalid input. Enter a valid number.")
        except KeyboardInterrupt:
            print(Fore.LIGHTRED_EX + "\n\n[!] " + Fore.RESET + "Exiting. Bye!")
            sys.exit(0)


def get_filename_input(default_name: str = "passlist.txt") -> str:
    """Prompt the user for an output filename."""
    try:
        user_input = input(
            f"[{Fore.LIGHTGREEN_EX}>{Fore.RESET}] Enter filename (Enter = {default_name}): "
        ).strip()
        return str(Path(user_input).resolve()) if user_input else str(Path.cwd() / default_name)
    except KeyboardInterrupt:
        print(Fore.LIGHTRED_EX + "\n\n[!] " + Fore.RESET + "Exiting. Bye!")
        sys.exit(0)


def show_logo():
    print(Style.BRIGHT + "\n\t\t   BELCH Password List Generator   v 1.1.2")
    print(Style.DIM + "\t\t\t\tBy Croketillo")
    print("\t\t\t      [Ctrl + C] to EXIT \n")


def print_columns(options: List[Tuple[str, str]], num_columns: int = 2):
    max_width = max(len(k) + len(v) + 3 for k, v in options) + 2
    for i in range(0, len(options), num_columns):
        line = ""
        for j in range(num_columns):
            if i + j < len(options):
                k, v = options[i + j]
                line += f"{k} - {v}".ljust(max_width)
        print(line)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    init(autoreset=True)
    show_logo()

    options = [
        ("/d", "Digit"),
        ("/c", "Lowercase"),
        ("/C", "Uppercase"),
        ("/e", "Special characters"),
        ("/?", "Random characters"),
        ("/@", "Mixed upper/lower"),
        ("/&", "Mixed upper/lower/digits"),
    ]

    print(Style.BRIGHT + "Available Patterns:")
    print_columns(options)
    print("_" * 80)

    while True:
        try:
            pattern = input(f"[{Fore.LIGHTGREEN_EX}>{Fore.RESET}] Enter pattern: ").strip()
            if not pattern or any(c.isspace() for c in pattern):
                print(Fore.LIGHTRED_EX + "[!] " + Fore.RESET + "Invalid pattern. No spaces allowed.")
                continue
            generator = PasswordGenerator(pattern)
            break
        except KeyboardInterrupt:
            print(Fore.LIGHTRED_EX + "\n\n[!] " + Fore.RESET + "Exiting. Bye!")
            sys.exit(0)

    try:
        combinations = generator.calculate_combinations()
        example = generator.generate_single()
        weight = calculate_weight(combinations, len(example))

        print(Style.DIM + f"[{Fore.YELLOW}i{Fore.RESET}] Maximum combinations: {combinations} ({weight})")

        count = get_integer_input(
            f"[{Fore.LIGHTGREEN_EX}>{Fore.RESET}] Number of passwords to generate (default: {combinations}): ",
            combinations,
        )
        filename = get_filename_input()

        print("_" * 80)
        start = time.time()
        passwords = generator.generate_multiple(count)

        # Single buffered write — much faster than one write per password.
        with open(filename, "w") as f:
            f.write("\n".join(passwords) + "\n")

        duration = time.time() - start
        print("_" * 80)
        print(Fore.GREEN + "\n\n[+] " + Fore.RESET + f"Saved to '{filename}' in {format_duration(duration)}.")

    except KeyboardInterrupt:
        print(Fore.LIGHTRED_EX + "\n\n[!] " + Fore.RESET + "Exiting. Bye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
