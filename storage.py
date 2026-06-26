#account.json is a mini database
#storage.py file's job is to read data and save data

import json

FILE_NAME = "account.json"

def load_account():
    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return json.load(file)

def save_account(data):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        return json.dump(data, file, indent=4,ensure_ascii=False)
    
