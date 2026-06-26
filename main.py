

import tkinter as tk
from tkinter import messagebox
from banking import check_pin, deposit_money, withdraw_money
from storage import load_account

root = tk.Tk()
login_frame = tk.Frame(root)
dashboard_frame = tk.Frame(root)

root.title("Mini Banking System")

root.geometry("500x650")
root.resizable(True, True)

pin = ""

title_label = tk.Label(login_frame, text= "Mini Banking System", font =("Arial", 20, "bold"))
title_label.pack(pady=20)

display = tk.Entry(login_frame,font = ("Arial", 18), justify = "center",show = "*", width = 12, state = "readonly")
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

def login():
    global pin

    result = check_pin(pin)

    if result == "success":
        messagebox.showinfo("Login Successful",
                            "Welcome to Mini Banking System"
        )

        show_dashboard()
        
        pin = ""
        update_display()
        
    elif result == "Invalid_pin":
        messagebox.showerror("Login Failed",
                             "Incorrect PIN"
        )
        
        pin = ""
        update_display()
        
    elif result == "locked":
        messagebox.showerror(
            "Account Locked",
            "Account locked due to three invalid PIN attempts."
        )
        
        pin = ""
        update_display()

keypad = tk.Frame(login_frame)
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

login_button = tk.Button(login_frame, text= "LOGIN", font=("Arial", 14, "bold"), fg="white", bg="#2E8B57", activeforeground="red",activebackground="#1E6F46", command = login)
login_button.pack(pady=20)

login_frame.pack(fill = "both", expand=True)

def show_dashboard():

    account = load_account()

    welcome_label.config(
        text = f"Welcome, {account['account_holder']}"
    )

    account_label.config(
        text = f"Account Number : {account['account_number']}"
    )

    balance_label.config(
        text = f"Current Balance : {account['balance']}"
    )

    
    login_frame.pack_forget() #Hides the login frame
    dashboard_frame.pack(fill="both",expand =True)

dashboard_title = tk.Label(dashboard_frame, text = "Mini Banking System", font=("Arial", 20,"bold"))
dashboard_title.pack(pady=20)

welcome_label = tk.Label(dashboard_frame, font=("Arial", 16))
welcome_label.pack(pady=5)

account_label = tk.Label(dashboard_frame, font=("Arial", 14))
account_label.pack(pady=5)

balance_label = tk.Label(dashboard_frame, font=("Arial", 14, "bold"))
balance_label.pack(pady=10)

button_frame = tk.Frame(dashboard_frame)
button_frame.pack(pady=20)


def open_deposit_window():

    deposit_window = tk.Toplevel(root)
    deposit_window.title("Deposit Money")
    deposit_window.geometry("450x300")
    deposit_window.resizable(False, False)

    amount_label = tk.Label(deposit_window, text= "Enter Deposit Amount", font=("Arial", 12))
    amount_label.pack(pady=10)

    amount_entry = tk.Entry(deposit_window, font=("Arial", 14),justify="center")
    amount_entry.pack(pady=10)

    def deposit():
        amount = amount_entry.get()

        if amount == "":
            messagebox.showerror(
                "Error",
                "Please enter an amount."
            )
            return
        try:
            amount = int(amount)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter a valid number."
            )
            return
        result = deposit_money(amount)

        if result == "Invalid_amount":
            messagebox.showerror(
                "Invalid amount",
                "Amount must be greater than zero."
            )
        else:
            messagebox.showinfo(
                "Deposit Successful",
                f"₹{amount} deposited successfully."
            )
            show_dashboard()
            deposit_window.destroy()
            

    deposit_confirm_button = tk.Button(deposit_window, text="Deposit", width=15,fg="white", bg="#2E8B57", activeforeground="red",activebackground="#1E6F46",command =deposit)
    deposit_confirm_button.pack(pady=15)

deposit_button = tk.Button(button_frame, text= "Deposit", font=("Arial", 12, "bold"), width =20, height=2, command=open_deposit_window)
deposit_button.pack(pady=5)


def open_withdraw_window():

    withdraw_window = tk.Toplevel(root)
    withdraw_window.title("Withdraw Money")
    withdraw_window.geometry("450x300")
    withdraw_window.resizable(False, False)

    amount_label = tk.Label(withdraw_window, text = "Enter Withdrawal Amount", font=("Arial", 12))
    amount_label.pack(pady=10)

    amount_entry = tk.Entry(withdraw_window, font=("Arial", 14), justify = "center")
    amount_entry.pack(pady=10)


    def withdraw():

        amount = amount_entry.get()

        if amount == "":
            messagebox.showerror(
                "Error",
                "Please enter an amount."
            )
            return
        try:
            amount = int(amount)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter a valid number."
            )
            return
        result = withdraw_money(amount)

        if result == "invalid_amount":
             messagebox.showerror(
                "Invalid amount",
                "Amount must be greater than zero."
            )
             
        elif result == "insufficient_balance":
            messagebox.showerror(
                "Error",
                "Insufficeint Funds."
            )
        else:
            messagebox.showinfo(
                "Withdrawal Successful",
                f"₹{amount} withdrawn successfullly.")
            show_dashboard()
            withdraw_window.destroy()

    withdraw_confirm_button = tk.Button(withdraw_window, text="Withdraw", width=15,height=2,command=withdraw)
    withdraw_confirm_button.pack(pady=15)
            
        

withdraw_button = tk.Button(button_frame,text="Withdraw", width=20,height=2,font=("Arial",12,"bold"),command=open_withdraw_window)
withdraw_button.pack(pady=5)
    


root.mainloop()
                    
