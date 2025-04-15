

import pyautocad

def draw_circle(radius):
    with pyautocad.activate():
        pyautocad.command("_.Circle", [0, 0], radius)


# This function takes in the radius of the circle as an argument and uses the pyautocad library to create a new circle at coordinates (0, 0) with the specified radius. The `with` statement ensures that the autocad application is properly closed after the command has been executed.