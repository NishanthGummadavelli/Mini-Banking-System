

import tkinter as tk
from tkinter import messagebox, ttk
from banking import check_pin, deposit_money, withdraw_money, change_pin
from storage import load_account

root = tk.Tk()
login_frame = tk.Frame(root, bg="#F5F7FA")
dashboard_frame = tk.Frame(root)

root.title("Mini Banking System")
root.configure(bg="#F5F7FA")

root.geometry("500x650")
root.resizable(True, True)

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

pin = ""

title_label = tk.Label(login_frame, text= "Mini Banking System", font =("Segoe UI", 11))
title_label.pack(pady=20)

display = tk.Entry(login_frame,font = ("Segoe UI", 11), justify = "center",show = "*", width = 12, state = "readonly")
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

    button = tk.Button(keypad, text =text, width=8, height=2, font = ("Segoe UI", 11, "bold"), command = command)
    button.grid(row=row, column= column, padx=5, pady= 5)

login_button = tk.Button(login_frame, text= "LOGIN", font=("Segoe UI", 11, "bold"), fg="white", bg="#2E8B57", activeforeground="red",activebackground="#1E6F46", command = login)
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

dashboard_title = tk.Label(dashboard_frame, text = "Mini Banking System", font=("Segoe UI", 11))
dashboard_title.pack(pady=20)

welcome_label = tk.Label(dashboard_frame, font=("Segoe UI", 11))
welcome_label.pack(pady=5)

account_label = tk.Label(dashboard_frame, font=("Segoe UI", 11))
account_label.pack(pady=5)

balance_label = tk.Label(dashboard_frame, font=("Segoe UI", 11))
balance_label.pack(pady=10)

button_frame = tk.Frame(dashboard_frame)
button_frame.pack(pady=20)


def open_deposit_window():

    deposit_window = tk.Toplevel(root)
    deposit_window.title("Deposit Money")
    deposit_window.geometry("450x300")
    deposit_window.resizable(False, False)

    amount_label = tk.Label(deposit_window, text= "Enter Deposit Amount", font=("Segoe UI", 11))
    amount_label.pack(pady=10)

    amount_entry = tk.Entry(deposit_window, font=("Segoe UI", 11),justify="center")
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
    

deposit_button = tk.Button(button_frame, text= "Deposit", font=("Segoe UI", 11), width =20, height=2, command=open_deposit_window)
deposit_button.pack(pady=5)


def open_withdraw_window():

    withdraw_window = tk.Toplevel(root)
    withdraw_window.title("Withdraw Money")
    withdraw_window.geometry("450x300")
    withdraw_window.resizable(False, False)

    amount_label = tk.Label(withdraw_window, text = "Enter Withdrawal Amount", font=("Segoe UI", 11))
    amount_label.pack(pady=10)

    amount_entry = tk.Entry(withdraw_window, font=("Segoe UI", 11), justify = "center")
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

    withdraw_confirm_button = tk.Button(withdraw_window, text="Withdraw", width=15,height=2,command=withdraw,bg="#FF8C00")
    withdraw_confirm_button.pack(pady=15)
    
            
        

withdraw_button = tk.Button(button_frame,text="Withdraw", width=20,height=2,font=("Segoe UI",11),command=open_withdraw_window)
withdraw_button.pack(pady=5)


def open_history_window():
    history_window = tk.Toplevel(root)
    history_window.title("Transaction History")
    history_window.geometry("650x400")
    history_window.resizable(False, False)

    account = load_account()
    transactions = account["transactions"]

    tree = ttk.Treeview(history_window, columns=("datetime","transaction"),show="headings",height=12)

    tree.heading("datetime", text="Date & Time")
    tree.heading("transaction", text="Transaction")

    tree.column("datetime",width=220,anchor="center")
    tree.column("transaction",width=350,anchor="w")

    scrollbar = ttk.Scrollbar(history_window,orient="vertical",command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left",fill="both",expand="True",padx=10,pady=15)
    scrollbar.pack(side="right",fill="y")

    style = ttk.Style()

    style.configure("Treeview.Heading",font=("Segoe UI",11,"bold"))
    style.configure("Treeview",font=("Segoe UI",10),rowheight=28)

    if not transactions:
        tree.insert("",tk.END,values=("","No transactions available."))
    else:
        for entry in transactions:
            date_time,transaction = entry.split(" - ", 1)
            tree.insert("",tk.END,values=(date_time,transaction))

    close_button = tk.Button(history_window, text= "Close",width=15,command=history_window.destroy,bg="#1E90FF")
    close_button.pack(pady=10)
    


history_button = tk.Button(button_frame, text = "Transaction History", font=("Segoe UI",11),width=20,height=2,command=open_history_window)
history_button.pack(pady=5)

def open_change_pin_window():
    change_pin_window = tk.Toplevel(root)
    change_pin_window.title("Change PIN")
    change_pin_window.geometry("400x350")
    change_pin_window.resizable(False, False)

    current_pin_label = tk.Label(change_pin_window,text="Current PIN",font=("Segoe UI",12))
    current_pin_entry = tk.Entry(change_pin_window,font=("Segoe UI",12),show="*")
    current_pin_label.pack(pady=(20,5))
    current_pin_entry.pack()

    new_pin_label = tk.Label(change_pin_window,text="New PIN",font=("Segoe UI",12))
    new_pin_label.pack(pady=(15,5))
    new_pin_entry = tk.Entry(change_pin_window, show="*",font=("Segoe UI",12))
    new_pin_entry.pack()

    confirm_new_pin_label = tk.Label(change_pin_window,text="Confirm New PIN",font=("Segoe UI",12))
    confirm_new_pin_label.pack(pady=(15,5))
    confirm_new_pin_entry = tk.Entry(change_pin_window,font=("Segoe UI",12),show="*")
    confirm_new_pin_entry.pack()

    
    def change_pin_action():
        current_pin = current_pin_entry.get()
        new_pin = new_pin_entry.get()
        confirm_pin = confirm_new_pin_entry.get()

        if current_pin == "" or new_pin == "" or confirm_pin == "":
            messagebox.showerror(
                "Error",
                "Please fill all the fields."
            )
            return
        if len(current_pin) != 4 or len(confirm_pin) != 4 or len(new_pin) != 4:
            messagebox.showerror(
                "Error",
                "PIN must contain exactly 4 digits."
            )
            return
        if not current_pin.isdigit() or not new_pin.isdigit() or not confirm_pin.isdigit():
            messagebox.showerror(
                "Error",
                "PIN must contain only digits."
            )
            return
        if new_pin != confirm_pin:
            messagebox.showerror(
                "Error",
                "New PIN and Confirm PIN do not match."
            )
            return
        result = change_pin(current_pin, new_pin)

        if result == "incorrect_pin":
            messagebox.showerror("Error",
                                 "Current PIN is incorrect."
            )
        elif result == "same_pin":
            messagebox.showerror(
                "Error",
                "New PIN must be different from the Current PIN."
            )
        else:
            messagebox.showinfo(
                "Success",
                "PIN changed Successfully."
            )

            change_pin_window.destroy()

        
    change_button = tk.Button(change_pin_window,text="Change PIN",width=18,height=2,bg="green",command=change_pin_action)
    change_button.pack(pady=20)
    

        
change_pin_button = tk.Button(button_frame,text="Change PIN",width=20,height=2,font=("Segoe UI",11),command=open_change_pin_window)
change_pin_button.pack(pady=5)

def logout():
    global pin

    pin = ""

    update_display()

    dashboard_frame.pack_forget()

    login_frame.pack(fill="both",expand=True)

    messagebox.showinfo(
        "Logout",
        "You have been logged out successfully."
    )

logout_button = tk.Button(button_frame,text="Logout",width=20,height=2,font=("Segoe UI",11,"bold"),fg="white",bg="#B22222",activebackground="#8B0000",command=logout)
logout_button.pack(pady=5)

def exit_application():

    answer = messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit?"
    )

    if answer:
        root.destroy()

def customer_care():

    messagebox.showinfo(
        "Customer Care",
        "Mini Banking System\n\n"
        "Phone : + 91 8890601212\n"
        "Email : support@minibank.com\n\n"
        "Available : Monday - Friday\n"
        "9:00 AM - 6:00 PM")

def about():
    
    messagebox.showinfo(
        "About",
        "Mini Banking System\n\n"
        "Version : 1.0\n\n"
        "Developed By:\n"
        "Nishanth Gummadavelli\n\n"
        "Technologies Used:\n"
        "• Python\n"
        "• Tkinter\n"
        "• JSON\n"
        "• Git & GitHub"
    )

file_menu = tk.Menu(menu_bar, tearoff=0)

menu_bar.add_cascade(label = "File", menu=file_menu)
file_menu.add_command(label = "Exit", command=exit_application)

help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Customer Care", command=customer_care)
help_menu.add_separator()
help_menu.add_command(label="About",command=about)
    


root.mainloop()
                    
