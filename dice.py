import tkinter as tk
from tkinter import messagebox
import requests
import json
from threading import Timer

# Constants
API_URL = "https://www.magicnewton.com/portal/api/userQuests"
BANNER_URL = "https://raw.githubusercontent.com/Aniketcrypto/aniketcrypto/refs/heads/main/magicnewton.json"
headers_template = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd"
}

accounts = []

# Functions
def load_banner():
    try:
        response = requests.get(BANNER_URL)
        response.raise_for_status()
        data = response.json()
        return data.get("banner", "MagicNewton")
    except Exception as e:
        print("Failed to load banner:", e)
        return "MagicNewton"

banner_text = load_banner()

# Add Account
def add_account():
    def save_account():
        name = name_entry.get().strip()
        cookies = cookie_entry.get().strip()

        if not name or not cookies:
            messagebox.showerror("Error", "Please provide both account name and cookies.")
            return

        accounts.append({"name": name, "cookies": cookies})
        account_listbox.insert(tk.END, name)
        add_window.destroy()
        messagebox.showinfo("Success", f"Account '{name}' added successfully.")

    add_window = tk.Toplevel(root)
    add_window.title("Add Account")

    tk.Label(add_window, text="Account Name:").pack(pady=5)
    name_entry = tk.Entry(add_window)
    name_entry.pack(pady=5)

    tk.Label(add_window, text="Cookies:").pack(pady=5)
    cookie_entry = tk.Entry(add_window)
    cookie_entry.pack(pady=5)

    tk.Button(add_window, text="Save", command=save_account).pack(pady=10)

# API Request
def run_api(account):
    payload = json.dumps({"questId": "f56c760b-2186-40cb-9cbc-3af4a3dc20e2", "metadata": {}})
    headers = headers_template.copy()
    headers["Cookie"] = account["cookies"]

    try:
        response = requests.post(API_URL, data=payload, headers=headers)
        if response.status_code == 200:
            messagebox.showinfo("Success", f"API call for {account['name']} succeeded.")
        else:
            messagebox.showerror("Error", f"API call failed for {account['name']} with status {response.status_code}.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run API for {account['name']}: {e}")

# Run Once
def run_one():
    selected = account_listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "Please select an account.")
        return

    account = accounts[selected[0]]
    run_api(account)

# Run Every 24 Hours
def schedule_api():
    selected = account_listbox.curselection()
    if not selected:
        messagebox.showerror("Error", "Please select an account.")
        return

    account = accounts[selected[0]]

    def task():
        run_api(account)
        Timer(86400, task).start()  # Schedule for the next 24 hours

    messagebox.showinfo("Scheduled", f"API scheduled every 24 hours for {account['name']}.")
    task()

# Exit Application
def exit_app():
    root.destroy()

# UI Setup
root = tk.Tk()
root.title("MagicNewton Bot")

# Header
tk.Label(root, text=banner_text, font=("Helvetica", 16), fg="blue").pack(pady=10)

# Account Listbox
account_listbox = tk.Listbox(root, height=6)
account_listbox.pack(pady=10)

# Buttons
tk.Button(root, text="Add Account", bg="green", fg="white", command=add_account).pack(pady=5)
tk.Button(root, text="Run One", bg="blue", fg="white", command=run_one).pack(pady=5)
tk.Button(root, text="Run Every 24 Hours", bg="orange", fg="white", command=schedule_api).pack(pady=5)
tk.Button(root, text="Exit", bg="red", fg="white", command=exit_app).pack(pady=5)

root.mainloop()
