
import tkinter as tk

root = tk.Tk()

root.title("Mini Banking System")

root.geometry("500x650")
root.resizable(False, False)

pin = ""

title_label = tk.Label(root, text= "Mini Banking System", font =("Arial", 20, "bold"))
title_label.pack(pady=20)

display = tk.Entry(root,font = ("Arial", 18), justify = "center",show = "*", width = 12, state = "readonly")
display.pack(pady=10)

def update_display():
    display.config(state="normal")
    display.delete(0, tk.END)
    display.insert(0, pin)
    display.config(state ="readonly")

def add_digit(digit):
    global pin

    if len(pin) < 4:
        pin += str(digit)
        update_display()

def clear_pin():
    global pin
    pin = ""
    update_display()

def backspace():
    global pin
    pin = pin[:-1]
    update_display()

keypad = tk.Frame(root)
keypad.pack(pady=20)

buttons = [
    ("1", 0, 0),
    ("2", 0, 1),
    ("3", 0, 2),
    ("4", 1, 0),
    ("5", 1, 1),
    ("6", 1, 2),
    ("7", 2, 0),
    ("8", 2, 1),
    ("9", 2, 2),
    ("CLR", 3, 0),
    ("0", 3, 1),
    ("⌫", 3, 2)
]

for text, row, column in buttons:

    if text == "CLR":
        command = clear_pin
    elif text == "⌫":
        command = backspace
    else:
        command = lambda value =text: add_digit(value)

    button = tk.Button(keypad, text =text, width=8, height=2, font = ("Arial", 12), command = command)
    button.grid(row=row, column= column, padx=5, pady= 5)

login_button = tk.Button(root, text= "LOGIN", font=("Arial", 14, "bold"), fg="white", bg="#2E8B57", activeforeground="red",activebackground="#1E6F46")
login_button.pack(pady=20)

root.mainloop()
                    
