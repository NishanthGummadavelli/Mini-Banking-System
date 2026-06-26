from storage import load_account, save_account
from datetime import datetime

def check_pin(entered_pin):
    account = load_account()

    if account["locked"]:
        return  "locked"
    
    if entered_pin == account["pin"]:
        account["failed_attempts"] = 0
        save_account(account)
        return "success"
    
    account["failed_attempts"] += 1
    
    if account["failed_attempts"] >= 3:
        account["locked"] = True

    save_account(account)

    if account["locked"]:
        return "locked"
    return "Invalid_pin"

def deposit_money(amount):
    account = load_account()
    if amount <= 0:
        return "Invalid_amount"
    account["balance"] += amount

    current_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    account["transactions"].append(f"{current_time} - Deposited ₹{amount}")

    save_account(account)

    return "Success"
def withdraw_money(amount):
    account = load_account()

    if amount <= 0:
        return "invalid_amount"
    if amount > account['balance']:
        return "insufficient_balance"
    account["balance"] -= amount

    current_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    
    account["transactions"].append(f"{current_time} - Withdrew ₹{amount}")

    save_account(account)

    return "success"

def change_pin(current_pin,new_pin):
    account = load_account()

    if current_pin != account["pin"]:
        return "incorrect_pin"
    if new_pin == account["pin"]:
        return "same_pin"
    
    account["pin"] = new_pin
    current_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")
    account["transactions"].append(f"{current_time} - PIN Changed")
    save_account(account)
    
    return "success"
    
