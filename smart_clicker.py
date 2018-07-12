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
from tkinter import messagebox
import threading
import numpy as np
import random
from pynput.mouse import Controller
from pynput import keyboard
import pyautogui as ms

# Initialize the window
window = Tk()
window.title("Smart Clicker Version 0.3.0")
window.geometry('800x300')

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
number_of_clicks = StringVar()
interval_range = StringVar()
input_clicks = StringVar()
area_text_width = StringVar()
area_text_height = StringVar()

# Placeholder spread of cursor values
targeted_mouse_area = None

# For click thread
clicks_running = False

# Mouse position will be set from the user when the user presses f11
mouse_position_x = 0
mouse_position_y = 0

# Placing the labels to specified location for GUI
directions_label = Label(window, textvariable=directions).place(x=400, y=15, anchor="center")
label_placeholder = Label(window, text="").grid(row=0, column=0)

# label_x = Label(window, textvariable=string_variable_x).grid(row=1, column=0)
# mouse_x = Label(window, textvariable=mouse_variable_x).grid(row=1, column=1)
#
# label_y = Label(window, textvariable=string_variable_y).grid(row=2, column=0)
# mouse_y = Label(window, textvariable=mouse_variable_y).grid(row=2, column=1)
#
# display_location = Label(window, textvariable=label_set_location).grid(row=3, column=0)
# set_location = Label(window, textvariable=string_set_location).grid(row=3, column=1)

label_x = Label(window, textvariable=string_variable_x).place(x=350, y=45, anchor="center")
mouse_x = Label(window, textvariable=mouse_variable_x).place(x=450, y=45, anchor="center")

label_y = Label(window, textvariable=string_variable_y).place(x=350, y=75, anchor="center")
mouse_y = Label(window, textvariable=mouse_variable_y).place(x=450, y=75, anchor="center")

display_clicks = Label(window, textvariable=number_of_clicks).place(x=350, y=105, anchor="center")
input_clicks = Entry(window, width=5)
input_clicks.insert(END, '1')
input_clicks.place(x=450, y=105, anchor="center")

display_interval = Label(window, textvariable=interval_range).place(x=350, y=135, anchor="center")
input_interval_x = Entry(window, width=3)
input_interval_x.insert(END, '.3')
input_interval_x.place(x=435, y=135, anchor="center")
dash_interval = Label(window, text="-").place(x=460, y=135, anchor="center")
input_interval_y = Entry(window, width=3)
input_interval_y.insert(END, '.7')
input_interval_y.place(x=485, y=135, anchor="center")

label_area_text_width = Label(window, textvariable=area_text_width).place(x=350, y=165, anchor="center")
label_area_width = Entry(window, width=3)
label_area_width.insert(END, '1')
label_area_width.place(x=450, y=165, anchor="center")

label_area_text_height = Label(window, textvariable=area_text_height).place(x=350, y=195, anchor="center")
label_area_height = Entry(window, width=3)
label_area_height.insert(END, '1')
label_area_height.place(x=450, y=195, anchor="center")

display_location = Label(window, textvariable=label_set_location).place(x=350, y=225, anchor="center")
set_location = Label(window, textvariable=string_set_location).place(x=450, y=225, anchor="center")

string_variable_x.set('Mouse X: ')
string_variable_y.set('Mouse Y: ')
label_set_location.set('Click location (f11): ')
number_of_clicks.set('Number of clicks: ')
interval_range.set('Interval Range: ')
area_text_width.set('Spread of clicks width: ')
area_text_height.set('Spread of clicks height: ')

directions.set('press f11 to start clicker at cursor and f12 to stop clicker')


# This function returns the mouse coordinates of user's cursor during runtime
def set_mouse_label():
    position = mouse.position
    mouse_variable_x.set(position[0])
    mouse_variable_y.set(position[1])
    window.after(1, set_mouse_label)


def set_mouse_area(position):
    # The spread of the clicks around the original position

    if int(label_area_width.get()) > 0:
        if int(label_area_width.get()) % 2 == 0:
            area_width = int(label_area_width.get()) + 1
        else:
            area_width = int(label_area_width.get())
    else:
        area_width = 1
        print('it is 0 or a negative number, putting 1 instead')

    if int(label_area_height.get()) > 0:
        if int(label_area_height.get()) % 2 == 0:
            area_height = int(label_area_height.get()) + 1
        else:
            area_height = int(label_area_height.get())
    else:
        area_height = 1

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
        global clicks_running

        if key == keyboard.Key.f11 and not clicks_running:
            # Passing the position of user's cursor to the function set_mouse_area
            print('Mouse position set at: {}'.format(mouse.position))
            position = mouse.position
            string_set_location.set('x = ' + str(position[0]) + ',' + ' y = ' + str(position[1]))
            set_mouse_area(position)

            t = threading.Thread(target=start_clicks)
            t.start()
            # catching value exceptions when the user puts in wrong values in the GUI

        if key == keyboard.Key.f12:
            clicks_running = False

    # Listens for keyboard inputs [Do not touch]
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


def start_clicks():
    global clicks_running
    clicks_running = True

    try:
        if float(input_interval_x.get()) < 0:
            interval_x = 0.0
        else:
            interval_x = float(input_interval_x.get())
    except ValueError:
        interval_x = 0

    try:
        if float(input_interval_y.get()) < 0:
            interval_y = 0.0
        else:
            interval_y = float(input_interval_y.get())
    except ValueError:
        interval_y = 0

    try:
        if int(input_clicks.get()) > 0:
            clicks = int(input_clicks.get())
        else:
            clicks = 1
    except ValueError:
        clicks = 1

    if interval_x > interval_y:
        interval_x, interval_y = interval_y, interval_x

    # Clicks for 10 seconds at 10 randomly differently locations in the targeted area
    for x in range(clicks):

        if not clicks_running:
            break

        try:
            coordinates = targeted_mouse_area[random.randint(0, int(label_area_height.get()) - 1), random.randint(0, int(label_area_width.get()) - 1)]
        except ValueError:
            coordinates = targeted_mouse_area[0, 0]
        ms.click(coordinates[0], coordinates[1], clicks=1, interval=random.uniform(interval_x, interval_y),
                 button='left', pause=0.1)
        print('clicked at {}'.format(coordinates))

    clicks_running = False


# This thread will run the listener in the background for optimal performance
background = threading.Thread(name='background', target=background)
background.start()

# Not resizable
window.resizable(False, False)

# Will update every time the cursor is moved
set_mouse_label()

Button(window, text="QUIT", command=window.destroy)
window.mainloop()
