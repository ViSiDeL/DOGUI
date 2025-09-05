# import tkinter as tk


# root = tk.TK()

# root.title("")


# Button = you click it, then it does something

from tkinter import *

def click():
    print("Hello!")

window = Tk()
button = Button(window, text='Click me!!!')
button.config(command= click)  #performs call back of function 
button.config(font=("Ink Free", 50, 'bold'))
button.config(bg='#f20a0a')
button.config(fg='#fcfcfc')
button.config(activebackground= '#2600ff')
button.config(activeforeground= '#fcfcfc')
button.pack()
window.mainloop()








