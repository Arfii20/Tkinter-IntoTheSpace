# Coursework 2 of COMP16321

"""
*** The screen resolution is 1440x900

* This is a classic asteroid game where the player needs to avoid hitting the asteroids to survive.
* The difficulty increases at certain scores.
* The speed of the asteroids will increase making the game harder and harder at each level.
"""

# game_icon.ico source: https://www.freeiconspng.com/img/17270
# spaceship_image.png source: https://www.pngkey.com/detail/u2q8a9t4r5y3a9r5_spaceship-png-file-spaceship-png/
# asteroid_1.png source: https://www.pngwing.com/en/free-png-yoygi
# asteroid_2.png source: https://pngimg.com/image/105528
# asteroid_3.png source: https://pngimg.com/image/105498
# asteroid_4.png source: https://pngimg.com/image/105494
# asteroid_5.png source: https://www.pngwing.com/en/free-png-tsprz
# background.jpg source: Photo by Aleksandar Pasaric: https://www.pexels.com/photo/dark-starry-sky-1694000/
# main.png: https://www.pngitem.com/middle/wmmbxo_asteroids-asteroid-mining-transparent-background-asteroids-png-png/

# options.png source: http://pixelartmaker.com/art/e996fd04f0c49f2
# start.png source: http://pixelartmaker.com/art/6a45404d913e6d1
# exit.png source: http://pixelartmaker.com/art/36cd392e6295705
# pause.png source: https://www.pixilart.com/draw/pause-button-2-22f5240ce52a5c4
# restart.png source: http://pixelartmaker.com/art/ad99f7494306997
# resume.png source: http://pixelartmaker.com/art/5be181b34875416
# leaderboard.png source: http://pixelartmaker.com/art/7cc98bfa5bbcc0b


from tkinter import *
from tkinter.font import Font
from PIL import Image, ImageTk
from random import randint


# from s
# from threading import Thread
# from time import sleep


# Configure main window
def configure_window():
    # global menubar
    window.title("Asteroid Game")
    window.iconbitmap("images/game_icon.ico")

    # Disabled resizing of the window
    window.resizable(False, False)

    """ Fixing geometry so that the window opens at the center """
    # Width and height of the window
    width = window_width
    height = window_height

    # Screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Change of coordinates
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2 - 20)

    # screen position
    window.geometry(f"{width}x{height}+{x}+{y}")


def normal_buttons():
    canvas_main.itemconfig(options, state="normal")
    canvas_main.itemconfig(exited, state="normal")
    canvas_main.itemconfig(leaderboards, state="normal")

def hidden_buttons():
    canvas_main.itemconfig(exited, state="hidden")
    canvas_main.itemconfig(leaderboards, state="hidden")
    canvas_main.itemconfig(options, state="hidden")

# A manubar on top of the window
def menu():
    file_menu = Menu(menubar, tearoff=False)
    menubar.add_cascade(label="File", menu=file_menu, underline=0)
    file_menu.add_command(label="Restart", command=restart_game)
    file_menu.add_command(label="Exit", command=window.destroy)

    history_menu = Menu(menubar, tearoff=False)
    menubar.add_cascade(label="Match History", menu=history_menu, underline=0)
    # history_menu.add_command(label="Match history", command=win_history)

    help_menu = Menu(menubar, tearoff=False)
    menubar.add_cascade(label="Help", menu=help_menu, underline=0)
    # history_menu.add_command(label="Help", command=help)


def main_menu(_):
    global menubar

    # Deleting the text
    canvas_main.delete(press_any_key)

    # Adding a Menu bar
    menubar = Menu(canvas_main)
    window.configure(menu=menubar)

    # Add a manu bar
    menu()

    # Add buttons to main menu of canvas
    canvas_main.itemconfig(start, state="normal")
    normal_buttons()


# Creating keybindings to move the spaceship
def move_spaceship_left(_):
    canvas_main.move(spaceship, -10, 0)


def move_spaceship_right(_):
    canvas_main.move(spaceship, 10, 0)


def move_spaceship_up(_):
    canvas_main.move(spaceship, 0, -10)


def move_spaceship_down(_):
    canvas_main.move(spaceship, 0, 10)


def pause_menu(_):
    global pause_game

    if not pause_game:
        pause_game = True

        # Adding buttons for pause menu
        canvas_main.itemconfig(resume, state="normal")
        canvas_main.itemconfig(restarted, state="normal")
        normal_buttons()
        canvas_main.itemconfig(main_image, state="normal")

    elif pause_game:
        canvas_main.itemconfig(resume, state="hidden")
        canvas_main.itemconfig(restarted, state="hidden")
        hidden_buttons()
        pause_game = False
        asteroid_falling_down()


def resume_button_click():
    global pause_game
    canvas_main.itemconfig(resume, state="hidden")
    canvas_main.itemconfig(restarted, state="hidden")
    hidden_buttons()
    pause_game = False
    asteroid_falling_down()


def options_button_click():
    pass


def leaderboard():
    pass


def add_images():
    global spaceship
    # Add spaceship to canvas
    spaceship = canvas_main.create_image(window_width / 2 - 40,
                                         window_height - window_height / 7,
                                         image=spaceship_image, anchor=NW)

    # List data structure to store asteroid images
    global asteroid_image
    asteroid_image = []

    # Resize asteroid
    for i in range(1, 6):
        asteroid_org = Image.open("images/asteroid_" + str(i) + ".png")
        asteroid_resized = asteroid_org.resize((100, 100), Image.Resampling.LANCZOS)
        asteroid_image.append(ImageTk.PhotoImage(asteroid_resized))


# Determining from where the asteroid will start falling
def asteroid_initial_position():
    global asteroid
    asteroid = []

    # Selecting initial position of the asteroid
    asteroid_select = randint(0, 4)
    asteroid_x = randint(50, window_width - 110)
    asteroid_y = 0

    # Adding the position to an empty set for threading
    asteroid.append(canvas_main.create_image(asteroid_x, asteroid_y, image=asteroid_image[asteroid_select], anchor=NW))

    # after selecting position, fall is initialised
    asteroid_falling_down()


# Function for making the asteroid fall
def asteroid_falling_down():
    global asteroid, score, after
    pos_asteroid = canvas_main.coords(asteroid[0])
    if pos_asteroid[1] != window_height and pause_game is False:
        canvas_main.coords(asteroid[0], pos_asteroid[0], pos_asteroid[1] + 10)
        after = window.after(10, asteroid_falling_down)
    elif not pause_game:
        # Increasing score
        score += 20
        score_txt = "Score: " + str(score)
        canvas_main.itemconfig(scoreText, text=score_txt)

        asteroid_initial_position()


def restart_game():
    global restart_flag, pause_game
    pause_game = False
    restart_flag = True
    canvas_main.itemconfig(resume, state="hidden")
    canvas_main.itemconfig(restarted, state="hidden")
    hidden_buttons()
    window.after_cancel(after)
    main_game()


# Creating main game function
def main_game():
    global score, scoreText, restart_flag

    canvas_main.unbind("<Return>")

    # Hides the main menu buttons
    canvas_main.itemconfig(main_image, state="hidden")
    canvas_main.itemconfig(start, state="hidden")
    hidden_buttons()

    # Deletes the scoreText when restarting
    if restart_flag:
        canvas_main.delete(scoreText)
        restart_flag = False

    # Adding all the images
    add_images()

    """ Keybindings """
    canvas_main.bind("<Left>", move_spaceship_left)
    canvas_main.bind("<Right>", move_spaceship_right)
    canvas_main.bind("<Up>", move_spaceship_up)
    canvas_main.bind("<Down>", move_spaceship_down)
    canvas_main.bind("<Escape>", pause_menu)
    canvas_main.focus_set()

    """ Making the scoring system """
    # storing and displaying the score
    score = 0
    score_text = "Score: " + str(score)

    # displaying the score on the top right
    scoreText = canvas_main.create_text(window_width - window_width / 8, window_height / 15,
                                        fill="white", font=custom_font, text=score_text)

    # Initialising the falling of asteroids
    asteroid_initial_position()


window = Tk()

"""Defining variables"""
# Width and height of the window
window_width = 1440
window_height = 900

""" custom font"""
custom_font = Font(
    family="MV Boli",
    size=35)

configure_window()

# Variables
pause_game = False
restart_flag = False

""" Creating the Canvas """
canvas_main = Canvas(window, width=window_width, height=window_height)
canvas_main.pack(fill="both", expand=True)

"""Adding Background to the pain game"""
# Open background image
background_image = ImageTk.PhotoImage(Image.open("images/background.jpg"))

# Add background to canvas
canvas_main.create_image(0, 0, image=background_image, anchor=NW)

""" Start menu """
# main menu image
main_menu_image = ImageTk.PhotoImage(Image.open("images/main.png"))
main_image = canvas_main.create_image(window_width/2, window_height/2, image=main_menu_image, anchor="center")
canvas_main.itemconfig(main_image, state="normal")

press_any_key = canvas_main.create_text(window_width / 2, window_height / 2,
                                        fill="white", font=custom_font,
                                        text="Press enter to continue")

""" Start button """
start_org = Image.open("images/start.png")
start_resized = start_org.resize((230, 90), Image.Resampling.LANCZOS)
start_image = ImageTk.PhotoImage(start_resized)
start_button = Button(window, image=start_image, bg="black", border=0, command=main_game)
start = canvas_main.create_window(window_width / 2, window_height / 2 - 165, window=start_button)
canvas_main.itemconfig(start, state="hidden")

""" options button """
options_org = Image.open("images/options.png")
options_resized = options_org.resize((280, 90), Image.Resampling.LANCZOS)
options_image = ImageTk.PhotoImage(options_resized)
options_button = Button(window, image=options_image, bg="black", border=0, command=options_button_click)
options = canvas_main.create_window(window_width / 2, window_height / 2 + 55, window=options_button)
canvas_main.itemconfig(options, state="hidden")

""" exit button """
exit_org = Image.open("images/exit.png")
exit_resized = exit_org.resize((240, 80), Image.Resampling.LANCZOS)
exit_image = ImageTk.PhotoImage(exit_resized)
exit_button = Button(window, image=exit_image, bg="black", border=0, command=window.destroy)
exited = canvas_main.create_window(window_width / 2, window_height / 2 + 165, window=exit_button)
canvas_main.itemconfig(exited, state="hidden")

""" resume button """
resume_org = Image.open("images/resume.png")
resume_resized = resume_org.resize((264, 90), Image.Resampling.LANCZOS)
resume_image = ImageTk.PhotoImage(resume_resized)
resume_button = Button(window, image=resume_image, border=0, bg="black", command=resume_button_click)
resume = canvas_main.create_window(window_width / 2, window_height / 2 - 275, window=resume_button)
canvas_main.itemconfig(resume, state="hidden")

""" restart button """
restart_org = Image.open("images/restart.png")
restart_resized = restart_org.resize((284, 100), Image.Resampling.LANCZOS)
restart_image = ImageTk.PhotoImage(restart_resized)
restart_button = Button(window, image=restart_image, border=0, bg="black", command=restart_game)
restarted = canvas_main.create_window(window_width / 2, window_height / 2 - 165, window=restart_button)
canvas_main.itemconfig(restarted, state="hidden")

""" leaderboard button """
leaderboard_org = Image.open("images/leaderboard.png")
leaderboard_resized = leaderboard_org.resize((574, 90), Image.Resampling.LANCZOS)
leaderboard_image = ImageTk.PhotoImage(leaderboard_resized)
leaderboard_button = Button(window, image=leaderboard_image, border=0, bg="black", command=leaderboard)
leaderboards = canvas_main.create_window(window_width / 2, window_height / 2 - 55, window=leaderboard_button)
canvas_main.itemconfig(leaderboards, state="hidden")

""" Spaceship """
spaceship_org = Image.open("images/spaceship_image.png")
spaceship_resized = spaceship_org.resize((100, 100), Image.Resampling.LANCZOS)
spaceship_image = ImageTk.PhotoImage(spaceship_resized)

canvas_main.bind("<Return>", main_menu)
canvas_main.focus_set()

window.mainloop()
