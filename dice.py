import requests
import json
import time
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Constants
API_URL = "https://www.magicnewton.com/portal/api/userQuests"
BANNER_URL = "https://raw.githubusercontent.com/Aniketcrypto/aniketcrypto/refs/heads/main/magicnewton.txt"
headers_template = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd"
}

accounts = []

# Load banner
def load_banner():
    try:
        response = requests.get(BANNER_URL)
        response.raise_for_status()
        # Get the raw text content
        banner = response.text
        return banner if banner else "MagicNewton"
    except Exception as e:
        print(Fore.RED + f"Failed to load banner: {str(e)}")
        return "MagicNewton"

banner_text = load_banner()

def add_account():
    name = input(Fore.YELLOW + "Enter account name: ").strip()
    cookies = input(Fore.YELLOW + "Enter account cookies: ").strip()

    if not name or not cookies:
        print(Fore.RED + "Error: Both account name and cookies are required.")
        return

    accounts.append({"name": name, "cookies": cookies})
    print(Fore.GREEN + f"Account '{name}' added successfully.")

def run_api(account):
    payload = json.dumps({"questId": "f56c760b-2186-40cb-9cbc-3af4a3dc20e2", "metadata": {}})
    headers = headers_template.copy()
    headers["Cookie"] = account["cookies"]

    try:
        response = requests.post(API_URL, data=payload, headers=headers)
        if response.status_code == 200:
            print(Fore.GREEN + f"API call for {account['name']} succeeded.")
        else:
            print(Fore.RED + f"API call failed for {account['name']} with status {response.status_code}.")
    except Exception as e:
        print(Fore.RED + f"Failed to run API for {account['name']}: {e}")

def run_one():
    if not accounts:
        print(Fore.RED + "No accounts available. Please add an account first.")
        return

    for i, account in enumerate(accounts):
        print(Fore.CYAN + f"{i + 1}. {account['name']}")

    try:
        choice = int(input(Fore.YELLOW + "Select an account (number): ")) - 1
        if 0 <= choice < len(accounts):
            run_api(accounts[choice])
        else:
            print(Fore.RED + "Invalid choice.")
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter a number.")

def schedule_api():
    if not accounts:
        print(Fore.RED + "No accounts available. Please add an account first.")
        return

    for i, account in enumerate(accounts):
        print(Fore.CYAN + f"{i + 1}. {account['name']}")

    try:
        choice = int(input(Fore.YELLOW + "Select an account (number): ")) - 1
        if 0 <= choice < len(accounts):
            account = accounts[choice]
            print(Fore.GREEN + f"API scheduled every 24 hours for {account['name']}.")
            while True:
                run_api(account)
                time.sleep(86400)  # Schedule for the next 24 hours
        else:
            print(Fore.RED + "Invalid choice.")
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter a number.")

def main():
    print(Fore.LIGHTBLUE_EX + banner_text)  # Print the full ASCII art banner

    while True:
        print("\nMenu:")
        print(Fore.CYAN + "1. Add Account")
        print(Fore.CYAN + "2. Run One API Call")
        print(Fore.CYAN + "3. Schedule API Call (Every 24 Hours)")
        print(Fore.CYAN + "4. Exit")

        choice = input(Fore.YELLOW + "Select an option: ").strip()
        
        if choice == "1":
            add_account()
        elif choice == "2":
            run_one()
        elif choice == "3":
            schedule_api()
        elif choice == "4":
            print(Fore.LIGHTRED_EX + "Exiting... Bye!")
            break
        else:
            print(Fore.RED + "Invalid option. Please try again.")

if __name__ == "__main__":
    main()
