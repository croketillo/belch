from pathlib import Path
import random
import string
import sys
import time
from typing import List, Set, Tuple
from colorama import init, Style, Fore
from tinyprogress import progress


SPECIAL_CHARACTERS = "!@#$%^&*(),.?\":{}|<>_-+/;[]"


class PasswordGenerator:
    def __init__(self, pattern: str):
        self.pattern = pattern.strip()

    def generate_single(self) -> str:
        result = []
        i = 0
        while i < len(self.pattern):
            char = self.pattern[i]
            if char == "/" and i + 1 < len(self.pattern):
                i += 1
                token = self.pattern[i]
                result.append(self._translate_token(token))
            else:
                result.append(char)
            i += 1
        return "".join(result)

    def _translate_token(self, token: str) -> str:
        token_map = {
            "C": string.ascii_uppercase,
            "c": string.ascii_lowercase,
            "d": string.digits,
            "e": SPECIAL_CHARACTERS,
            "?": string.ascii_letters + string.digits + SPECIAL_CHARACTERS,
            "@": string.ascii_letters,
            "&": string.ascii_letters + string.digits
        }
        return random.choice(token_map[token]) if token in token_map else "/" + token

    def generate_multiple(self, count: int) -> List[str]:
        max_possible = self.calculate_combinations()
        if count > max_possible:
            raise ValueError(f"Cannot generate {count} unique passwords. Max possible is {max_possible}.")

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
        total = 1
        i = 0
        while i < len(self.pattern):
            char = self.pattern[i]
            if char == "/" and i + 1 < len(self.pattern):
                i += 1
                control = self.pattern[i]
                repeat = 1
                while i + 1 < len(self.pattern) and self.pattern[i + 1] == control:
                    repeat += 1
                    i += 1
                total *= self._token_combinations(control) ** repeat
            else:
                total *= 1
            i += 1
        return total

    def _token_combinations(self, token: str) -> int:
        token_map = {
            "C": len(string.ascii_uppercase),
            "c": len(string.ascii_lowercase),
            "d": len(string.digits),
            "e": len(SPECIAL_CHARACTERS),
            "?": len(string.ascii_letters + string.digits + SPECIAL_CHARACTERS),
            "@": len(string.ascii_letters),
            "&": len(string.ascii_letters + string.digits)
        }
        return token_map.get(token, 1)


def get_integer_input(prompt: str, max_value: int) -> int:
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
    try:
        user_input = input(f"[{Fore.LIGHTGREEN_EX}>{Fore.RESET}] Enter filename (Enter = {default_name}): ").strip()
        return str(Path(user_input).resolve()) if user_input else str(Path.cwd() / default_name)
    except KeyboardInterrupt:
        print(Fore.LIGHTRED_EX + "\n\n[!] " + Fore.RESET + "Exiting. Bye!")
        sys.exit(0)


def show_logo():
    print(Style.BRIGHT + "\n\t\t   BELCH Password List Generator   v 0.5.0")
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


def calculate_weight(n_lines: int, line_length: int) -> str:
    total_bytes = (line_length + 1) * n_lines
    mb = total_bytes / (1024 * 1024)
    gb = mb / 1024
    if gb >= 1:
        return f"{gb:.2f} GB"
    elif mb >= 0.01:
        return f"{mb:.2f} MB"
    return f"{total_bytes} bytes"


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
        ("/&", "Mixed upper/lower/digits")
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
            combinations
        )
        filename = get_filename_input()

        print("_" * 80)
        start = time.time()
        passwords = generator.generate_multiple(count)

        with open(filename, "w") as f:
            for pwd in passwords:
                f.write(pwd + "\n")
        duration = time.time() - start

        print("_" * 80)
        if duration > 3600:
            h, rem = divmod(duration, 3600)
            m, s = divmod(rem, 60)
            print(Fore.GREEN + f"\n\n[+] " + Fore.RESET + f"Saved to '{filename}' in {int(h)}h {int(m)}m {s:.2f}s.")
        elif duration > 60:
            m, s = divmod(duration, 60)
            print(Fore.GREEN + f"\n\n[+] " + Fore.RESET + f"Saved to '{filename}' in {int(m)}m {s:.2f}s.")
        else:
            print(Fore.GREEN + f"\n\n[+] " + Fore.RESET + f"Saved to '{filename}' in {duration:.2f}s.")

    except KeyboardInterrupt:
        print(Fore.LIGHTRED_EX + "\n\n[!] " + Fore.RESET + "Exiting. Bye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
