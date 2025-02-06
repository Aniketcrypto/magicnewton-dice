import requests
import json
import time
from colorama import Fore, Style, init
import random
import os

# Initialize colorama
init(autoreset=True)

# Constants
API_URL = "https://www.magicnewton.com/portal/api/userQuests"
BANNER_URL = "https://raw.githubusercontent.com/Aniketcrypto/aniketcrypto/refs/heads/main/magicnewton.txt"
ACCOUNTS_FILE = "accounts.json"
PROXIES_FILE = "proxies.json"

headers_template = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd"
}

accounts = []
proxies = []
use_proxy = False

def load_banner():
    try:
        response = requests.get(BANNER_URL)
        response.raise_for_status()
        return response.text if response.text else "MagicNewton"
    except Exception as e:
        print(Fore.RED + f"Failed to load banner: {str(e)}")
        return "MagicNewton"

def print_yellow_banner(banner_text):
    print(Fore.YELLOW + banner_text)

def save_accounts():
    try:
        with open(ACCOUNTS_FILE, 'w') as f:
            json.dump(accounts, f, indent=4)
        print(Fore.GREEN + "Accounts saved successfully.")
    except Exception as e:
        print(Fore.RED + f"Error saving accounts: {e}")

def load_accounts():
    global accounts
    try:
        if os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, 'r') as f:
                accounts = json.load(f)
            print(Fore.GREEN + f"Loaded {len(accounts)} accounts.")
    except Exception as e:
        print(Fore.RED + f"Error loading accounts: {e}")
        accounts = []

def save_proxies():
    try:
        with open(PROXIES_FILE, 'w') as f:
            json.dump(proxies, f, indent=4)
        print(Fore.GREEN + "Proxies saved successfully.")
    except Exception as e:
        print(Fore.RED + f"Error saving proxies: {e}")

def load_proxies():
    global proxies
    try:
        if os.path.exists(PROXIES_FILE):
            with open(PROXIES_FILE, 'r') as f:
                proxies = json.load(f)
            print(Fore.GREEN + f"Loaded {len(proxies)} proxies.")
    except Exception as e:
        print(Fore.RED + f"Error loading proxies: {e}")
        proxies = []

def get_random_proxy():
    if not proxies:
        return None
    return {"http": f"http://{random.choice(proxies)}", "https": f"http://{random.choice(proxies)}"}

def ask_proxy_preference():
    while True:
        choice = input(Fore.YELLOW + "Do you want to use proxy for this operation? (y/n): ").strip().lower()
        if choice in ['y', 'n']:
            return choice == 'y'
        print(Fore.RED + "Invalid choice. Please enter 'y' or 'n'.")

def run_api(account):
    payload = json.dumps({"questId": "f56c760b-2186-40cb-9cbc-3af4a3dc20e2", "metadata": {}})
    headers = headers_template.copy()
    current_proxy = get_random_proxy() if use_proxy and proxies else None
    
    try:
        response = requests.post(
            API_URL, 
            data=payload, 
            headers=headers,
            cookies=account["formatted_cookies"],
            proxies=current_proxy,
            timeout=30
        )
        
        if response.status_code == 200:
            try:
                resp_data = response.json()
                credits = resp_data.get('data', {}).get('credits', 0)
                account['total_credits'] += credits
                save_accounts()
                print(Fore.GREEN + f"API call for {account['name']} succeeded.")
                print(Fore.GREEN + f"Credits earned: {credits}")
                print(Fore.GREEN + f"Total credits for {account['name']}: {account['total_credits']}")
            except json.JSONDecodeError:
                print(Fore.RED + "Failed to parse response JSON. Response:")
                print(Fore.RED + response.text)
        else:
            print(Fore.RED + f"API call failed for {account['name']} with status {response.status_code}.")
            print(Fore.RED + f"Response: {response.text[:200]}")
    except Exception as e:
        print(Fore.RED + f"Failed to run API for {account['name']}: {e}")

def run_all():
    global use_proxy
    if proxies:
        use_proxy = ask_proxy_preference()
    for account in accounts:
        run_api(account)

def schedule_all():
    global use_proxy
    if proxies:
        use_proxy = ask_proxy_preference()
    print(Fore.GREEN + "API scheduled every 24 hours for all accounts.")
    while True:
        for account in accounts:
            run_api(account)
        time.sleep(86400)

def add_account():
    name = input(Fore.YELLOW + "Enter account name: ").strip()
    cookies = input(Fore.YELLOW + "Enter account cookies: ").strip()
    if not name or not cookies:
        print(Fore.RED + "Error: Both account name and cookies are required.")
        return
    accounts.append({"name": name, "cookies": cookies, "formatted_cookies": {}, "total_credits": 0})
    save_accounts()
    print(Fore.GREEN + f"Account '{name}' added successfully.")

def main():
    load_accounts()
    load_proxies()
    banner_text = load_banner()
    print_yellow_banner(banner_text)
    
    while True:
        print("\nMenu:")
        print(Fore.CYAN + "1. Add Account")
        print(Fore.CYAN + "2. Run API for All Accounts")
        print(Fore.CYAN + "3. Schedule API for All Accounts (Every 24 Hours)")
        print(Fore.CYAN + "4. Add Proxies")
        print(Fore.CYAN + "5. Exit")

        choice = input(Fore.YELLOW + "Select an option: ").strip()
        
        if choice == "1":
            add_account()
        elif choice == "2":
            run_all()
        elif choice == "3":
            schedule_all()
        elif choice == "4":
            add_proxies()
        elif choice == "5":
            print(Fore.LIGHTRED_EX + "Exiting... Bye!")
            break
        else:
            print(Fore.RED + "Invalid option. Please try again.")

if __name__ == "__main__":
    main()
