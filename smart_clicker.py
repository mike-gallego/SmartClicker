'''
    - Monitor Mouse; Output mouse location (x, y)
    - GUI must output mouse location and not make it editable
    - To the user, encourage them to place cursor in middle of specified area
    - Pressing a button (f11) on your keyboard, will set the specified location
    - Randomize the area to click so that the clicks are spread out from the set location
    - Click speed interval to be randomized
    - Future update: record clicks
'''

from tkinter import *
import threading
import numpy as np
import random
from pynput.mouse import Controller
from pynput import keyboard
import pyautogui as ms

# Initialize the window
window = Tk()
window.title("Smart Clicker Version 0.1.0")
window.geometry('800x400')

# Controller object to get mouse position
mouse = Controller()

# Labels for mouse information
string_variable_x = StringVar()
string_variable_y = StringVar()
mouse_variable_x = StringVar()
mouse_variable_y = StringVar()
label_set_location = StringVar()
string_set_location = StringVar()
directions = StringVar()

# Placeholder spread of cursor values
targeted_mouse_area = None

# Mouse position will be set from the user when the user presses f11
mouse_position_x = 0
mouse_position_y = 0

# Placing the labels to specified location for GUI
directions_label = Label(window, textvariable=directions).place(x=400, y=15, anchor="center")
label_placeholder = Label(window, text="").grid(row=0, column=0)

label_x = Label(window, textvariable=string_variable_x).grid(row=1, column=0)
mouse_x = Label(window, textvariable=mouse_variable_x).grid(row=1, column=1)

label_y = Label(window, textvariable=string_variable_y).grid(row=2, column=0)
mouse_y = Label(window, textvariable=mouse_variable_y).grid(row=2, column=1)

display_location = Label(window, textvariable=label_set_location).grid(row=3, column=0)
set_location = Label(window, textvariable=string_set_location).grid(row=3, column=1)

string_variable_x.set('Mouse X: ')
string_variable_y.set('Mouse Y: ')
label_set_location.set('Set (f11): ')

directions.set('Press f11 to set location, press f12 to start clicker')


# This function returns the mouse coordinates of user's cursor during runtime
def set_mouse_label():
    position = mouse.position
    mouse_variable_x.set(position[0])
    mouse_variable_y.set(position[1])
    window.after(1, set_mouse_label)


def set_mouse_area(position):
    # The spread of the clicks around the original position; might be CHANGEABLE by the user in the future
    # MUST BE ODD, since we need the middle location to be the original set position
    area_width = 21
    area_height = 21

    # Placeholder for a shape of our height and width
    mouse_area = np.ndarray(shape=(area_height, area_width), dtype=tuple)

    # Needed to add values to the right locations around it by subtracting the difference from the middle value
    middle_y = int(np.median(range(area_height)))
    middle_x = int(np.median(range(area_width)))

    # Add the mouse position in the center of the array
    mouse_area[middle_y, middle_x] = position

    # From the middle cursor position, the for loop adds in the values around it
    for val_y in range(area_height):
        for val_x in range(area_width):
            difference_x = middle_x - val_x
            difference_y = middle_y - val_y
            mouse_area[val_y, val_x] = (position[0] - difference_x, position[1] - difference_y)

    # Will show a multi dimensional array of the spread of cursor values
    print(mouse_area)

    global targeted_mouse_area
    targeted_mouse_area = mouse_area


def background():
    def on_press(key):
        if key == keyboard.Key.f11:

            # Passing the position of user's cursor to the function set_mouse_area
            print('Mouse position set at: {}'.format(mouse.position))
            position = mouse.position
            string_set_location.set('x = ' + str(position[0]) + ',' + ' y = ' + str(position[1]))
            set_mouse_area(position)

        if key == keyboard.Key.f12:

                # Clicks for 10 seconds at 10 randomly differently locations in the targeted area
                for x in range(10):
                    coordinates = targeted_mouse_area[random.randint(0, 20), random.randint(0, 20)]
                    ms.click(coordinates[0], coordinates[1], clicks=1, interval=random.uniform(0.0, 1.0), button='left')
                    print('clicked at {}'.format(coordinates))

    # Listens for keyboard inputs [Do not touch]
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


# This thread will run the listener in the background for optimal performance
background = threading.Thread(name='background', target=background)
background.start()

# Not resizable
window.resizable(False, False)

# Will update every time the cursor is moved
set_mouse_label()

window.mainloop()
