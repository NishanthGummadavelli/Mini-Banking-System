from storage import load_account, save_account

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

    account["transactions"].append(f"Deposited ₹{amount}")

    save_account(account)

    return "Success"
def withdraw_money(amount):
    account = load_account()

    if amount <= 0:
        return "invalid_amount"
    if amount > account['balance']:
        return "insufficient_balance"
    account["balance"] -= amount
    account["transactions"].append(f"Withdrew ₹{amount}")

    save_account(account)

    return "success"
    
