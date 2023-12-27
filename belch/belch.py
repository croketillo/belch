"""BELCH Password list generator v0.3.5

Author: Croketillo <croketillo@gmail.com>

Description: Generate a list of character strings according to a given pattern and stores it in a file.
"""
import random
import string
import time
import os
import sys
from tqdm import tqdm
from colorama import init,Style,Fore

class PasswordGenerator:
    """Generate passwods based in pattern"""
    def __init__(self, pattern):
        self.pattern = pattern

    def generate_single(self):
        result = ""
        i = 0
        while i < len(self.pattern):
            char = self.pattern[i]
            if char == "/" and i + 1 < len(self.pattern):
                i += 1
                token = self.pattern[i]
                if token == "C":
                    result += random.choice(string.ascii_uppercase)
                elif token == "c":
                    result += random.choice(string.ascii_lowercase)
                elif token == "d":
                    result += random.choice(string.digits)
                elif token == "e":
                    result += random.choice("!@#$%^&*(),.?\":{}|<>_-+/;[]")
                elif token == "?":
                    result += random.choice(string.ascii_letters + string.digits + "!@#$%^&*(),.?\":{}|<>_-+/;[]")
                else:
                    result += char + token
            else:
                result += char
            i += 1
        return result

    def generate_multiple(self, count):
        generated_passwords = set()

        with tqdm(total=count, desc="Generating passwords", unit="passwords", ascii=" ░▒█") as pbar:
            while len(generated_passwords) < count:
                generated_password = self.generate_single()
                if generated_password not in generated_passwords:
                    generated_passwords.add(generated_password)
                    pbar.update(1)

        return list(generated_passwords)

    def calculate_combinations(self):
        """Calculate the total combinations"""
        total_combinations = 1

        i = 0
        while i < len(self.pattern):
            char = self.pattern[i]
            if char == "/":
                i += 1
                control_char = self.pattern[i]
                repeat_factor = 1
                while i + 1 < len(self.pattern) and self.pattern[i + 1] == control_char:
                    repeat_factor += 1
                    i += 1
                if control_char == "C":
                    total_combinations *= len(string.digits) ** repeat_factor
                elif control_char == "c":
                    total_combinations *= len(string.ascii_lowercase) ** repeat_factor
                elif control_char == "d":
                    total_combinations *= len(string.digits) ** repeat_factor
                elif control_char in ("e", "?"):
                    total_combinations *= len("!@#$%^&*(),.?\":{}|<>_-+/;[]") ** repeat_factor
            else:
                total_combinations *= 1  # No control character, multiply by 1
            i += 1

        return total_combinations

def get_integer_input(prompt, max_value):
    """Gets an integer input from the user."""
    while True:
        value = input(prompt)
        if value:
            try:
                value=int(value) 
                if 0 < value <= max_value:
                    return value
                print(f"Please enter a number between 1 and {max_value}.")
            except ValueError:
                        print("Invalid input. Please enter a number.")
        else: 
            value=int(max_value)
            return value

def get_filename_input():
    """Gets the name of the user's file"""
    current_directory = os.getcwd()
    default_filename = "passlist.txt"
    default_path = os.path.join(current_directory, default_filename)

    user_input = input(f">>> Enter the file name (or press Enter to default): ").strip()

    if user_input:
        return os.path.join(current_directory, user_input)
    else:
        return default_path

def main():
    """Main function"""
    init(autoreset=True)
    print(Fore.LIGHTMAGENTA_EX+"""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@                     *%@@@@@@@@@@
@@@@@@@@@@@      *@@@@@@#      %@@@@@@@@
@@@@@@@@@@@      *@@@@@@@#      @@@@@@@@
@@@@@@@@@@@      *@@@@@@@#      %@@@@@@@
@@@@@@@@@@@      *@@@@@@@      #@@@@@@@@
@@@@@@@@@@@      *@%%%#*    *#@@@@@@@@@@
@@@@@@@@@@@                *#%@@@@@@@@@@
@@@@@@@@@@@      *@@@@@@%*     *@@@@@@@@
@@@@@@@@@@@      *@@@@@@@@*      @@@@@@@
@@@@@@@@@@@      *@@@@@@@@#      #@@@@@@
@@@@@@@@@@@      *@@@@@@@@       %@@@@@@
@@@@@@@@@@@      *@@@@@@%       %@@@@@@@
@@@@@@@                      *%@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@%###########################@@@@@@
@@@@@@%#                         #@@@@@@
@@@@@@@@@%%%%%%%%%%%%%%%%%%%%%%%@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@""")
    print(Fore.LIGHTBLACK_EX+"    Password List Generator   v 0.3.7")
    print(Fore.LIGHTBLACK_EX+"          [Ctrl + c] to EXIT \n")
    print(Style.BRIGHT+"TO SET PATTERN:")
    
    from rich.console import Console
    from rich.table import Table


    table = Table()
    table.add_column("Pattern command", style="cyan", justify="center")
    table.add_column("Description", style="magenta")
    table.add_row("/d", "Digit")
    table.add_row("/c", "Lowercase")
    table.add_row("/C", "Uppercase")
    table.add_row("/e", "Special characters")
    table.add_row("/?", "Random characters")
    
    console = Console()
    console.print(table)
    
    
    try:
        user_input = input(">>> Enter pattern: ")
        password_generator = PasswordGenerator(user_input)

        max_combinations = password_generator.calculate_combinations()
        print(Style.DIM+f"(The maximum number of possible combinations is: {max_combinations})")

        n_password = get_integer_input(f">>> Enter the number of passwords to generate (Enter for default: {max_combinations}): ", max_combinations)

        file_name = get_filename_input()

        start_time = time.time()
        with open(file_name, "w") as file:
            passwords = password_generator.generate_multiple(n_password)
            for generated_password in passwords:
                file.write(generated_password + "\n")
        end_time = time.time()
        original_duration = end_time - start_time

        if original_duration > 60:
            minutes, seconds = divmod(original_duration, 60)
            if minutes > 60:
                hours, minutes = divmod(minutes, 60)
                print(f"Passwords generated and stored in the file '{file_name}' in {int(hours)} hours, {int(minutes)} minutes, and {seconds:.2f} seconds.")
            else:
                print(f"Passwords generated and stored in the file '{file_name}' in {int(minutes)} minutes and {seconds:.2f} seconds.")
        else:
            print(f"Passwords generated and stored in the file '{file_name}' in {original_duration:.2f} seconds.")
    except KeyboardInterrupt:
        print(Fore.RED+"\n\n\tExit by user. Bye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
