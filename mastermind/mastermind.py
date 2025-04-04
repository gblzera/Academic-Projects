import random

COLORS = ['R', 'G', 'B', 'Y', 'O', 'P']  # Red, Green, Blue, Yellow, Orange, Purple
TRIES = 10
CODE_LENGTH = 4

def generate_code():
    code = []

    for _ in range(CODE_LENGTH):
        color = random.choice(COLORS)
        code.append(color)
    
    return code

def guess_code():
    while True:
        guess = input("Guess: ").upper().split(" ")
        
        if len(guess) != CODE_LENGTH:
            print(f"You must guess exactly {CODE_LENGTH} colors.")
            continue

        for color in guess:
            if color not in COLORS:
                print(f"Invalid color: {color}. Choose from {', '.join(COLORS)}.")
                break
        else:
            break

    return guess

def check_code(guess, real_code):
    color_counts = {}
    correct_pos = 0
    incorrect_pos = 0

    for color in real_code:
        if color not in color_counts:
            color_counts[color] = 0
        color_counts[color] += 1

    for guess_color, real_color in zip(guess, real_code):
        if guess_color == real_color:
            correct_pos += 1
            color_counts[guess_color] -= 1
    
    for guess_color, real_color in zip(guess, real_code):
        if guess_color in color_counts and color_counts[guess_color] > 0:
            incorrect_pos += 1
            color_counts[guess_color] -= 1
    
    return correct_pos, incorrect_pos

def game():
    print(f"Welcome to Mastermind, you have {TRIES} attempts to guess the code.")
    print(f"Available colors: {', '.join(COLORS)}")

    code = generate_code()
    for attempt in range(1, TRIES + 1):
        guess = guess_code()
        correct_pos, incorrect_pos = check_code(guess, code)

        if correct_pos == CODE_LENGTH:
            print(f"Congratulations! You've guessed the code {code} in {attempt} attempts.")
            break

        print(f"Correct positions: {correct_pos} correct positions | Incorrect positions: {incorrect_pos}")
    
    else:
        print(f"Sorry, you've used all your attempts. The correct code was:", *code)

if __name__ == "__main__":
    game()