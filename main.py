import turtle
from turtle import Screen, Turtle

import pandas as pd

# CONSTANTS
FONT = ("arial", 7, "normal")
END_FONT = ("arial", 15, "normal")
IMG_PATH = "./image/blank_states_img.gif"

# Screen setup
screen = Screen()
screen.title("US State Guess Game")
screen.addshape(IMG_PATH)
turtle.shape(IMG_PATH)

# Read Data from CSV file
df = pd.read_csv("./dataset/50_states.csv")
columns = list(df.columns)

# getting states list from DataFrame
states = df.state.to_list()


def locate_state(state):
    # creating pointer to locate state
    name = Turtle()
    name.color("Black")
    name.penup()
    name.hideturtle()

    if state in states:
        # getting coordinates from DataFrame
        state_location = df[df[columns[0]] == state]
        # coordinates = (int(state_location['x']), int(state_location['y']))
        coordinates = tuple(map(int, (state_location.x, state_location.y)))  # I wanted to use map function

        # locating guessed state
        name.goto(coordinates)
        name.write(f"{state_location.state.item()}", True, "center", FONT)

        # re-guessing closes the game
        states.remove(state)
        return True
    else:
        # Game End Text.
        name.write(f"Wrong Guess, Game End!!!", True, "center", END_FONT)
        return False


# missed states stored in csv
def missed_states(guess_list):
    missing_states = {
        "states": [],
    }
    for each_guess in guess_list:
        if each_guess in states:
            states.remove(each_guess)
    else:
        missing_states["states"].extend(states)

    learn_states_df = pd.DataFrame(missing_states)
    learn_states_df.to_csv("states_to_learn.csv")


is_guess_correct = True
guesses = []

while len(guesses) < 50:
    guess = screen.textinput(f"{len(guesses)}/50 Guess The State", "Enter the name of the state: ").title()
    is_guess_correct = locate_state(guess)
    if guess == "Exit":
        break
    if is_guess_correct:
        guesses.append(guess)

missed_states(guesses)
