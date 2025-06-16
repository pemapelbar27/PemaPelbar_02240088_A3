import tkinter as tk
from tkinter import messagebox
import random
import os


class InvalidInputError(Exception):
    """Raised when the input is invalid."""
    pass

class InsufficientBalanceError(Exception):
    """Raised when there is not enough balance."""
    pass

class BankAccount:
    def __init__(self, account_id, passcode, balance=0):
        self.account_id = account_id
        self.passcode = passcode
        self.balance = float(balance)

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidInputError("Deposit amount must be greater than 0")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidInputError("Withdrawal amount must be greater than 0")
        if amount > self.balance:
            raise InsufficientBalanceError("Insufficient balance")
        self.balance -= amount

    def top_up_phone(self, phone_number, amount):
        if not phone_number.isdigit() or len(phone_number) < 8:
            raise InvalidInputError("Invalid phone number")
        if amount <= 0:
            raise InvalidInputError("Top-up amount must be greater than 0")
        if amount > self.balance:
            raise InsufficientBalanceError("Insufficient balance")
        self.balance -= amount
        return f"Phone {phone_number} topped up with Nu.{amount}"

class BankingSystem:
    def __init__(self, filename="accounts.txt"):
        self.filename = filename
        self.accounts = self.load_accounts()

    def load_accounts(self):
        accounts = {}
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) == 3:
                        acc_id, passcode, balance = parts
                        accounts[acc_id] = BankAccount(acc_id, passcode, float(balance))
        return accounts

    def save_accounts(self):
        with open(self.filename, "w") as file:
            for acc in self.accounts.values():
                file.write(f"{acc.account_id},{acc.passcode},{acc.balance}\n")

    def create_account(self):
        account_id = str(random.randint(10000, 99999))
        passcode = str(random.randint(1000, 9999))
        while account_id in self.accounts:
            account_id = str(random.randint(10000, 99999))
        new_account = BankAccount(account_id, passcode)
        self.accounts[account_id] = new_account
        self.save_accounts()
        return new_account

    def login(self, account_id, passcode):
        acc = self.accounts.get(account_id)
        if acc and acc.passcode == passcode:
            return acc
        else:
            raise ValueError("Account number or password is invalid")

    def delete_account(self, account_id):
        if account_id in self.accounts:
            del self.accounts[account_id]
            self.save_accounts()
        else:
            raise ValueError("Account does not exist")

class BankAppGUI:
    def __init__(self, banking_system, account):
        self.system = banking_system
        self.account = account

        self.window = tk.Tk()
        self.window.title(f"Bank - {account.account_id}")
        self.window.geometry("350x400")

        # Amount Entry
        tk.Label(self.window, text="Amount (Nu):").pack()
        self.amount_entry = tk.Entry(self.window)
        self.amount_entry.pack()

        # Deposit & Withdraw
        tk.Button(self.window, text="Deposit", command=self.deposit).pack(pady=3)
        tk.Button(self.window, text="Withdraw", command=self.withdraw).pack(pady=3)

        # Phone Top-Up
        tk.Label(self.window, text="Phone Number:").pack()
        self.phone_entry = tk.Entry(self.window)
        self.phone_entry.pack()
        tk.Button(self.window, text="Top-Up Phone", command=self.top_up).pack(pady=3)

        # Transfer
        tk.Label(self.window, text="Recipient Account ID:").pack()
        self.recipient_entry = tk.Entry(self.window)
        self.recipient_entry.pack()
        tk.Button(self.window, text="Transfer", command=self.transfer).pack(pady=3)

        # Show & Delete
        tk.Button(self.window, text="Show Balance", command=self.show_balance).pack(pady=3)
        tk.Button(self.window, text="Delete Account", command=self.delete_account).pack(pady=3)

        self.window.mainloop()

    def deposit(self):
        try:
            amount = float(self.amount_entry.get())
            self.account.deposit(amount)
            self.system.save_accounts()
            messagebox.showinfo("Success", f"Nu.{amount} is deposited with Avail Bal: Nu.{self.account.balance}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def withdraw(self):
        try:
            amount = float(self.amount_entry.get())
            self.account.withdraw(amount)
            self.system.save_accounts()
            messagebox.showinfo("Success", f"Nu.{amount} is debited with Avail Bal Nu.{self.account.balance}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def top_up(self):
        try:
            phone = self.phone_entry.get()
            amount = float(self.amount_entry.get())
            msg = self.account.top_up_phone(phone, amount)
            self.system.save_accounts()
            messagebox.showinfo("Success", f"{msg}. Avail Bal Nu.{self.account.balance}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def transfer(self):
        try:
            recipient_id = self.recipient_entry.get()
            amount = float(self.amount_entry.get())
            if recipient_id not in self.system.accounts:
                raise ValueError("Recipient does not exist")
            self.account.withdraw(amount)
            recipient = self.system.accounts[recipient_id]
            recipient.deposit(amount)
            self.system.save_accounts()
            messagebox.showinfo("Success", f"Transferred Nu.{amount} to {recipient_id}. New Balance: Nu.{self.account.balance}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_balance(self):
        messagebox.showinfo("Balance", f"Your Available Balance is Nu.{self.account.balance}")

    def delete_account(self):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete your account?")
        if confirm:
            self.system.delete_account(self.account.account_id)
            messagebox.showinfo("Deleted", "Account deleted successfully.")
            self.window.destroy()

def login_screen(system):
    win = tk.Tk()
    win.title("Login or Create Account")
    win.geometry("300x200")

    tk.Label(win, text="Account ID:").pack()
    id_entry = tk.Entry(win)
    id_entry.pack()

    tk.Label(win, text="Passcode:").pack()
    pass_entry = tk.Entry(win, show="*")
    pass_entry.pack()

    def try_login():
        acc_id = id_entry.get()
        passcode = pass_entry.get()
        try:
            acc = system.login(acc_id, passcode)
            win.destroy()
            BankAppGUI(system, acc)
        except Exception as e:
            messagebox.showerror("Login Failed", str(e))

    def create_new():
        acc = system.create_account()
        messagebox.showinfo("Account Created", f"Account ID: {acc.account_id}\nPasscode: {acc.passcode}")

    tk.Button(win, text="Login", command=try_login).pack(pady=5)
    tk.Button(win, text="Create Account", command=create_new).pack()

    win.mainloop()

if __name__ == "__main__":
    system = BankingSystem()
    login_screen(system)
