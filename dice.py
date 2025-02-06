import requests
import json
import time
from colorama import Fore, Style, init
import random

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

def format_cookies(cookie_string):
    try:
        cookies = {}
        for cookie in cookie_string.split(';'):
            if '=' in cookie:
                name, value = cookie.strip().split('=', 1)
                cookies[name.strip()] = value.strip()
        return cookies
    except Exception as e:
        print(Fore.RED + f"Error formatting cookies: {e}")
        return None

def add_account():
    name = input(Fore.YELLOW + "Enter account name: ").strip()
    cookies = input(Fore.YELLOW + "Enter account cookies: ").strip()

    if not name or not cookies:
        print(Fore.RED + "Error: Both account name and cookies are required.")
        return

    formatted_cookies = format_cookies(cookies)
    if not formatted_cookies:
        print(Fore.RED + "Error: Invalid cookie format")
        return

    accounts.append({
        "name": name,
        "cookies": cookies,
        "formatted_cookies": formatted_cookies,
        "total_credits": 0
    })
    print(Fore.GREEN + f"Account '{name}' added successfully.")

def add_proxies():
    print(Fore.YELLOW + "\nEnter your proxies (one per line, format: ip:port or user:pass@ip:port)")
    print(Fore.YELLOW + "Press Enter twice when done:")
    
    while True:
        proxy = input().strip()
        if not proxy:
            break
        proxies.append(proxy)
    
    if proxies:
        print(Fore.GREEN + f"Added {len(proxies)} proxies successfully.")
    else:
        print(Fore.RED + "No proxies were added.")

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
    global use_proxy
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
                print(Fore.GREEN + f"API call for {account['name']} succeeded.")
                print(Fore.GREEN + f"Credits earned: {credits}")
                print(Fore.GREEN + f"Total credits for {account['name']}: {account['total_credits']}")
            except json.JSONDecodeError:
                print(Fore.RED + "Failed to parse response JSON")
        else:
            print(Fore.RED + f"API call failed for {account['name']} with status {response.status_code}.")
            print(Fore.RED + f"Response: {response.text[:200]}")
    except Exception as e:
        print(Fore.RED + f"Failed to run API for {account['name']}: {e}")

def run_one():
    if not accounts:
        print(Fore.RED + "No accounts available. Please add an account first.")
        return

    global use_proxy
    for i, account in enumerate(accounts):
        print(Fore.CYAN + f"{i + 1}. {account['name']} (Total Credits: {account['total_credits']})")

    try:
        choice = int(input(Fore.YELLOW + "Select an account (number): ")) - 1
        if 0 <= choice < len(accounts):
            if proxies:
                use_proxy = ask_proxy_preference()
            run_api(accounts[choice])
        else:
            print(Fore.RED + "Invalid choice.")
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter a number.")

def schedule_api():
    if not accounts:
        print(Fore.RED + "No accounts available. Please add an account first.")
        return

    global use_proxy
    for i, account in enumerate(accounts):
        print(Fore.CYAN + f"{i + 1}. {account['name']} (Total Credits: {account['total_credits']})")

    try:
        choice = int(input(Fore.YELLOW + "Select an account (number): ")) - 1
        if 0 <= choice < len(accounts):
            if proxies:
                use_proxy = ask_proxy_preference()
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
    banner_text = load_banner()
    print_yellow_banner(banner_text)

    while True:
        print("\nMenu:")
        print(Fore.CYAN + "1. Add Account")
        print(Fore.CYAN + "2. Run One API Call")
        print(Fore.CYAN + "3. Schedule API Call (Every 24 Hours)")
        print(Fore.CYAN + "4. Add Proxies")
        print(Fore.CYAN + "5. Exit")

        choice = input(Fore.YELLOW + "Select an option: ").strip()
        
        if choice == "1":
            add_account()
        elif choice == "2":
            run_one()
        elif choice == "3":
            schedule_api()
        elif choice == "4":
            add_proxies()
        elif choice == "5":
            print(Fore.LIGHTRED_EX + "Exiting... Bye!")
            break
        else:
            print(Fore.RED + "Invalid option. Please try again.")

if __name__ == "__main__":
    main()
