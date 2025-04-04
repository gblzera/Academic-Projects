# Mastermind - Code Breaking Game

Mastermind is a classic code-breaking game where you must guess a secret sequence of colors within a limited number of attempts.

## How to Play

- The computer generates a secret code consisting of 4 colors.
- You have 10 attempts to guess the correct sequence.
- After each guess, you'll receive feedback:
  - The number of colors in the correct position.
  - The number of correct colors in the wrong position.
- Use logic and deduction to crack the code before you run out of attempts!

## Available Colors

The game uses the following colors:

```
R - Red
G - Green
B - Blue
Y - Yellow
O - Orange
P - Purple
```

## Running the Game

Ensure you have Python installed, then run the script using:

```sh
python mastermind.py
```

## Example Game Session

```
Welcome to Mastermind, you have 10 attempts to guess the code.
Available colors: R, G, B, Y, O, P
Guess: R G B Y
Correct positions: 2 correct positions | Incorrect positions: 1
Guess: R O B Y
Congratulations! You've guessed the code ['R', 'O', 'B', 'Y'] in 2 attempts.
```

## Features
- Random code generation
- Input validation
- Feedback after each guess
- Supports uppercase and lowercase input

## Future Improvements
- Add difficulty levels (increase or decrease code length)
- Implement a graphical interface
- Add multiplayer mode
