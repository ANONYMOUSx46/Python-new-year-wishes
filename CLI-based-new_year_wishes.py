import os
import time
import random
from datetime import datetime
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_with_delay(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def create_firework(size=5):
    stages = [
        ['    *    ', '   ***   ', '  *****  ', ' ******* ', '*********'],
        ['    .    ', '   ...   ', '  .....  ', ' ....... ', '.........'],
        ['    o    ', '   ooo   ', '  ooooo  ', ' ooooo0o ', 'ooooo0ooo'],
        ['         ', '    +    ', '   +++   ', '  +++++  ', ' +++++++  ']
    ]
    
    for _ in range(3):  # Animation cycles
        for stage in stages:
            clear_screen()
            print("\n" * 2)
            for line in stage:
                print(f"{line:^50}")
            time.sleep(0.2)

def display_wishes(name):
    wishes = [
        f"Dear {name}, may your year sparkle with joy and laughter!",
        f"Wishing you 365 days of success and happiness, {name}!",
        f"May this year bring you amazing opportunities, {name}!",
        f"Here's to new adventures and beautiful moments, {name}!"
    ]
    
    for wish in wishes:
        clear_screen()
        print("\n" * 2)
        print("🌟" * 20)
        print_with_delay(wish)
        print("🌟" * 20)
        time.sleep(1.5)

def main():
    clear_screen()
    print("\n" * 2)
    print("=" * 50)
    print_with_delay("🎉 Welcome to New Year Celebrations! 🎉".center(50))
    print("=" * 50)
    print()
    
    name = input("Please enter your name: ")
    
    print("\nPreparing your celebration...")
    time.sleep(1)
    
    # Display fireworks animation
    create_firework()
    # Display the main celebration
    clear_screen()
    current_year = datetime.now().year
    print("\n" * 2)
    print("*" * 50)
    message = f"🎊 HAPPY NEW YEAR {current_year} 🎊".center(50)
    print_with_delay(message)
    print("*" * 50)
    
    # Display personalized wishes
    display_wishes(name)
    
    # Final message
    clear_screen()
    print("\n" * 2)
    print("✨" * 20)
    print_with_delay(f"Thank you for celebrating with me, {name}!")
    print_with_delay("May all your dreams come true!")
    print("✨" * 20)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nThanks for celebrating! Goodbye!")