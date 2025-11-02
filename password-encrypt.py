from cryptography.fernet import Fernet
import json

# Generate a key once and save it securely
def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    
        
def load_key():
    try:
        return open("key.key", "rb").read()
    except FileNotFoundError:
        write_key()
        load_key()
        return 


# write_key() # To generate Master key before storing

"""
    Start creating password storage
"""

key = load_key()
fer = Fernet(key)

def add_pasword():
    account = input("Account Name: ")
    password = input("Passowrd: ")
    encrypted_pass = fer.encrypt(password.encode()).decode() # encrypting inputed password using the master generated password
    
    data = load_data()
    data[account] = encrypted_pass
    save_data(data)
    print("✅Password saved\n")

def view_passwords():
    data = load_data()
    for account, enc_pass in data.items():
        decrypted = fer.decrypt(enc_pass.encode()).decode()
        print(f"{account}: {decrypted}")
    print("\n")
    
def search_password():
    search_input = input("Enter Account Name: ")
    data = load_data()
    searched = ""
    for account, enc_pass in data.items():
        if account.lower() == search_input.lower():
            decrypted = fer.decrypt(enc_pass.encode()).decode()
            searched = f"{account}: {decrypted}\n"
    
    print("=== Result ===")
    if searched:
        print(searched)
    else:
        print("❌Account not found!\n")
        
def load_data():
    try:
        with open("vault.json", "r") as vault:
            return json.load(vault)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open("vault.json", "w") as vault:
        json.dump(data, vault, indent=4)


while True:
    print("Welcome to the Safe Vault\n---\n1. Add Password\n2. View Password\n3. Search by account\nEnter key to Exit")
    choice = input("Enter option: ")
    
    if choice == "1":
        add_pasword()
    elif choice == "2":
        view_passwords()
    elif choice == "3":
        search_password()
    else:
        break