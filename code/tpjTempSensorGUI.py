#!/usr/bin/python3
"""
Author:         Yousif Zito
Purpose:        TPJ655 Capstone Project
App Name:       Advanced Security System
Date:           2022-08-05
"""
# import the necessary packages/libraries
import tkinter as tk
import tkinter.font as tkFont
import glob
from time import *
from os import system

# Parameters and global variables
# Declare global variables
root = None
dfont = None
frame = None
temp_c = None

# Global variable to remember if we are fullscreen or windowed
fullscreen = False

system('modprobe w1-gpio')
system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(f'{base_dir}28*')[0]
device_file = f'{device_folder}/w1_slave'


def read_temperature_raw():
    """
    This function reads the raw data from the sensor
    """
    with open(device_file,'r') as f:
        lines=f.readlines()
    return lines


def readtemp():
    """
    This function converts the raw temperature data
    into Celsius
    """
    lines=read_temperature_raw()
    while lines[0].strip()[-3:]!='YES':
        time.sleep(0.2)
        lines=read_temperature_raw()
    tout=lines[1].find('t=')
    if tout!=-1:
        tstr=lines[1].strip()[tout+2:]
        tc = round(float(tstr)/1000,2)
        unit="°C"
        return tc, unit


# Toggle fullscreen
def toggle_fullscreen(event=None):
    """
    This function toggles fullscreen for the Temperature GUI
    """
    global root
    global fullscreen
    # Toggle between fullscreen and windowed modes
    fullscreen = not fullscreen
    root.attributes('-fullscreen', fullscreen)
    resize()


def end_fullscreen(event=None):
    """
    This function reverts the screen to windowed
    """
    global root
    global fullscreen
    # Turn off fullscreen mode
    fullscreen = False
    root.attributes('-fullscreen', False)
    resize()


def resize(event=None):
    """
    This function resize GUI font based on frame height (minimum size of 12)
    """
    global dfont
    global frame
    # Use negative number for "pixels" instead of "points"
    new_size = -max(12, int((frame.winfo_height() / 10)))
    dfont.configure(size=new_size)

root=tk.Tk()
root.title('Advanced Security System - Temperature GUI')
# Create the main container
frame = tk.Frame(root)
# Lay out the main container (expand to fit window)
frame.pack(fill=tk.BOTH, expand=1)
# Variables for holding temperature and light data
temp_c = tk.DoubleVar()
# Create dynamic font for text
dfont = tkFont.Font(size=-24)

# Create widgets
label_temp = tk.Label(frame, text="Temperature", font=dfont)
label_celsius = tk.Label(frame, textvariable=temp_c, font=dfont)
#label_unitc = tk.Label(frame, text="°C", font=dfont)
button_quit = tk.Button(frame, text="Quit", font=dfont, command=root.destroy)

# Lay out widgets in a grid in the frame
label_temp.grid(row=0, column=1, padx=0, pady=0)
label_celsius.grid(row=1, column=1, padx=0, pady=0)
#label_unitc.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
button_quit.grid(row=2, column=1, padx=5, pady=5)

#device_file='/sys/bus/w1/devices/28-3cccf64902cf/w1_slave'

# Make it so that the grid cells expand out to fill window
for i in range(3):
    frame.rowconfigure(i, weight=1)
for i in range(3):
    frame.columnconfigure(i, weight=1)

# Bind F11 to toggle fullscreen and ESC to end fullscreen
root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', end_fullscreen)

# Have the resize() function be called every time the window is resized
root.bind('<Configure>', resize)


def tempGUI(top_level_window):
        global temp_c
        temp_c.set(readtemp())
        top_level_window.after(500,tempGUI,top_level_window)


root.after(500, tempGUI, root)
toggle_fullscreen()
root.mainloop()
