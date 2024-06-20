import random
import string
import time
import os
import sys
from tqdm import tqdm
from colorama import init, Style, Fore

class PasswordGenerator:
    """Generate passwords based on a pattern."""
    
    def __init__(self, pattern):
        self.pattern = pattern.strip()

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
                elif token == "@":
                    result += random.choice(string.ascii_uppercase + string.ascii_lowercase)
                elif token == "&":
                    result += random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
                else:
                    result += "/" + token  # Handle unknown token by treating as literal
            else:
                result += char
            i += 1
        return result
    
    def count_char(self,string):
        return len(string)

    def generate_multiple(self, count):
        generated_passwords = set()

        with tqdm(total=count, desc="Generating passwords", unit="passwords", ascii=" ░▒█") as pbar:
            try:
                while len(generated_passwords) < count:
                    generated_password = self.generate_single()
                    if generated_password not in generated_passwords:
                        generated_passwords.add(generated_password)
                        pbar.update(1)
            except KeyboardInterrupt:
                pbar.close()
                print(Fore.LIGHTRED_EX + "\n\n[!] "+Fore.RESET+"Generation interrupted by user. Saving generated passwords so far...")

        return list(generated_passwords)

    def calculate_combinations(self):
        """Calculate the total combinations based on the pattern."""
        total_combinations = 1

        i = 0
        while i < len(self.pattern):
            char = self.pattern[i]
            if char == "/":
                if i + 1 >= len(self.pattern):
                    total_combinations *= 1  # Interprets '/' at the end as a literal character
                    break
                i += 1
                control_char = self.pattern[i]
                repeat_factor = 1
                while i + 1 < len(self.pattern) and self.pattern[i + 1] == control_char:
                    repeat_factor += 1
                    i += 1
                if control_char == "C":
                    total_combinations *= len(string.ascii_uppercase) ** repeat_factor
                elif control_char == "c":
                    total_combinations *= len(string.ascii_lowercase) ** repeat_factor
                elif control_char == "d":
                    total_combinations *= len(string.digits) ** repeat_factor
                elif control_char == "e":
                    total_combinations *= len("!@#$%^&*(),.?\":{}|<>_-+/;[]") ** repeat_factor
                elif control_char == "?":
                    total_combinations *= len(string.ascii_letters + string.digits + "!@#$%^&*(),.?\":{}|<>_-+/;[]") ** repeat_factor
                elif control_char == "@":
                    total_combinations *= len(string.ascii_uppercase + string.ascii_lowercase) ** repeat_factor
                elif control_char == "&":
                    total_combinations *= len(string.ascii_uppercase + string.ascii_lowercase + string.digits) ** repeat_factor
            else:
                total_combinations *= 1  # No control character, multiply by 1
            i += 1

        return total_combinations

def get_integer_input(prompt, max_value):
    """Gets an integer input from the user."""
    while True:
        try:
            value = input(prompt)
            if value:
                try:
                    value = int(value)
                    if 0 < value <= max_value:
                        return value
                    print(Fore.LIGHTRED_EX + "[!] "+Fore.RESET+f"Please enter a number between 1 and {max_value}.")
                except ValueError:
                    print(Fore.LIGHTRED_EX + "[!] "+Fore.RESET+"Invalid input. Please enter a number." + Fore.RESET)
            else:
                return max_value
        except KeyboardInterrupt:
            print(Fore.LIGHTRED_EX + "\n\n[!] "+Fore.RESET+"Exit by user. Bye!")
            sys.exit(0)

def get_filename_input():
    """Gets the name of the user's file."""
    current_directory = os.getcwd()
    default_filename = "passlist.txt"
    default_path = os.path.join(current_directory, default_filename)

    try:
        user_input = input("["+Fore.LIGHTGREEN_EX+">"+Fore.RESET+"]  Enter the file name (or press Enter to use passlist.txt): ").strip()
    except KeyboardInterrupt:
        print(Fore.LIGHTRED_EX + "\n\n[!] "+Fore.RESET+"Exit by user. Bye!")
        sys.exit(0)

    if user_input:
        return os.path.join(current_directory, user_input)
    else:
        return default_path
    
def show_logo():
    print(Style.BRIGHT+"\n\t\t   BELCH Password List Generator   v 0.4.0 \t")
    print(Style.DIM+"\t\t\t\tBy Croketillo")
    print("\t\t\t      [Ctrl + C] to EXIT \n")

def print_columns(options, num_columns=2):
    max_width = max(len(opt[0]) + len(opt[1]) + 3 for opt in options) + 2  # Calculate max width with some padding
    wrapped_text = []
    
    for i in range(0, len(options), num_columns):
        line = ""
        for j in range(num_columns):
            if i + j < len(options):
                opt, desc = options[i + j]
                text = f"{opt} - {desc}"
                line += text.ljust(max_width)
        wrapped_text.append(line)
    
    for line in wrapped_text:
        print(line)

def calculate_weight_from_length(n_lines: int, length: int) -> str:
    """
    Calculates the weight of a string based on its length in characters and the number of lines, in bytes, megabytes, or gigabytes.

    :param n_lines: The number of lines.
    :param length: The length of the string in characters per line.
    :return: The weight of the string in bytes, megabytes, or gigabytes.
    """
    # Calculate total weight in bytes, assuming each line ends with a newline character
    weight_in_bytes = (length + 1) * n_lines  # +1 for newline character
    weight_in_megabytes = weight_in_bytes / (1024 * 1024)
    weight_in_gigabytes = weight_in_megabytes / 1024

    if weight_in_gigabytes >= 1:
        return f"{weight_in_gigabytes:.2f} GB"
    elif weight_in_megabytes >= 0.01:
        return f"{weight_in_megabytes:.2f} MB"
    return f"{weight_in_bytes} bytes"

def main():
    """Main function."""
    init(autoreset=True)
    show_logo()

    options = [
    ("/d", "Digit"),
    ("/c", "Lowercase"),
    ("/C", "Uppercase"),
    ("/e", "Special characters"),
    ("/?", "Random characters"),
    ("/@", "Mixed uppercase and lowercase"),
    ("/&", "Mixed uppercase, lowercase and digits")
    ]
    
    print(Style.BRIGHT + "Available Patterns:")
    print_columns(options)
    print("_"*80)
    
    while True:
        try:
            user_input = input("\n["+Fore.LIGHTGREEN_EX+">"+Fore.RESET+"] Enter pattern: ").strip()
            if not user_input or any(char.isspace() for char in user_input):
                print(Fore.LIGHTRED_EX + "[!] "+Fore.RESET+"Invalid pattern. Pattern cannot be empty or contain spaces.")
                continue

            password_generator = PasswordGenerator(user_input)
            break
        except KeyboardInterrupt:
            print(Fore.LIGHTRED_EX + "\n\n[!] "+Fore.RESET+"Exit by user. Bye!")
            sys.exit(0)

    try:
        max_combinations = password_generator.calculate_combinations()
        look_n_char=password_generator.generate_single()
        nchar=password_generator.count_char(look_n_char)

        file_weight=calculate_weight_from_length(max_combinations,nchar)

        print(Style.DIM + f"["+Fore.YELLOW+"i"+Fore.RESET+"] The maximum number of possible combinations is: {max_combinations}. ({file_weight})")

        n_password = get_integer_input(f"["+Fore.LIGHTGREEN_EX+">"+Fore.RESET+f"] Enter the number of passwords to generate (Enter for default: {max_combinations}): ", max_combinations)

        file_name = get_filename_input()

        start_time = time.time()
        print("_"*80)
        generated_passwords = password_generator.generate_multiple(n_password)

        with open(file_name, "w") as file:
            for generated_password in generated_passwords:
                file.write(generated_password + "\n")
        end_time = time.time()
        original_duration = end_time - start_time

        if original_duration > 60:
            minutes, seconds = divmod(original_duration, 60)
            if minutes > 60:
                hours, minutes = divmod(minutes, 60)
                print("_"*80)
                print(Fore.GREEN+f"\n\n[+] "+Fore.RESET+f"Passwords generated and stored in the file '{file_name}' in {int(hours)} hours, {int(minutes)} minutes, and {seconds:.2f} seconds.")
            else:
                print("_"*80)
                print(Fore.GREEN+f"\n\n[+] "+Fore.RESET+f"Passwords generated and stored in the file '{file_name}' in {int(minutes)} minutes and {seconds:.2f} seconds.")
        else:
            print("_"*80)
            print(Fore.GREEN+"\n\n[+] "+Fore.RESET+f"Passwords generated and stored in the file '{file_name}' in {original_duration:.2f} seconds.")
    except KeyboardInterrupt:
        print(Fore.LIGHTRED_EX + "\n\n[!] "+Fore.RESET+"Exit by user. Bye!")
        sys.exit(0)

if __name__ == "__main__":
    main()