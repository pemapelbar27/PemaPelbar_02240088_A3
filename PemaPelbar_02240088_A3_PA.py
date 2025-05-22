import tkinter as tk
from tkinter import messagebox

# Custom Exceptions 
class InvalidInputError(Exception):
    pass

class Insufficent_balance(Exception):
    pass

# Basic Bank Account
class BankAccount:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidInputError("Amount must be more than 0")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidInputError("Amount must be more than 0")
        if amount > self.balance:
            raise Insufficent_balance("Your account has insufficient balance")
        self.balance -= amount

    def top_up_phone(self, phone, amount):
        if not phone.isdigit() or len(phone) < 8:
            raise InvalidInputError("Phone number must be valid")
        self.withdraw(amount)
        return f"Phone {phone} topped up with Nu.{amount}"

# Input (CLI)
def user_input(choice, account):
    try:
        if choice == "1":
            amount = float(input("Enter amount to deposit: "))
            account.deposit(amount)
            print(f"Nu. {amount} is credited to your account")
        elif choice == "2":
            amount = float(input("Enter amount to withdraw: "))
            account.withdraw(amount)
            print(f"Nu. {amount} is debited from your account")
        elif choice == "3":
            phone = input("Enter phone number: ")
            amount = float(input("Enter top-up amount: "))
            result = account.top_up_phone(phone, amount)
            print(f"{phone} is recharged for Nu. {amount} successfully")
        elif choice == "4":
            print(f"Avail Bal: Nu.{account.balance}")
        elif choice == "5":
            print("Thank you for banking with us!")
            return False
        else:
            print("Please choose a number from the menu.")
    except (InvalidInputError, Insufficent_balance) as e:
        print("Error:", e)
    return True

# GUI
def run_gui(account):
    def deposit():
        try:
            amount = float(entry_amount.get())
            account.deposit(amount)
            messagebox.showinfo("Success", f"Nu. {amount} is credited to your account")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def withdraw():
        try:
            amount = float(entry_amount.get())
            account.withdraw(amount)
            messagebox.showinfo("Success", f"Nu. {amount} is debited from your account")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def top_up():
        def do_top_up():
            try:
                phone = entry_phone.get()
                amount = float(entry_amount.get())
                msg = account.top_up_phone(phone, amount)
                messagebox.showinfo("Success", msg)
                # Hide phone entry after success
                label_phone.grid_remove()
                entry_phone.grid_remove()
                # Reset top-up button
                top_up_button.config(text="Top Up", command=top_up)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Show phone entry for top-up
        label_phone.grid(row=1, column=0)
        entry_phone.grid(row=1, column=1)
        # Change button text to confirm
        top_up_button.config(text="Confirm Top Up", command=do_top_up)

    def show_balance():
        messagebox.showinfo("Balance", f"Avail Bal: Nu.{account.balance}")

    # GUI window setup
    window = tk.Tk()
    window.title("Simple Bank App")

    # Amount input
    tk.Label(window, text="Amount:").grid(row=0, column=0)
    entry_amount = tk.Entry(window)
    entry_amount.grid(row=0, column=1)

    # Phone input (hidden by default)
    label_phone = tk.Label(window, text="Phone #:")
    entry_phone = tk.Entry(window)

    # Buttons
    tk.Button(window, text="Deposit", command=deposit).grid(row=2, column=0)
    tk.Button(window, text="Withdraw", command=withdraw).grid(row=2, column=1)
    top_up_button = tk.Button(window, text="Top Up", command=top_up)
    top_up_button.grid(row=3, column=0)
    tk.Button(window, text="Show Balance", command=show_balance).grid(row=3, column=1)

    window.mainloop()

# Run CLI (Optional)
def run_cli():
    account = BankAccount("User", 100)
    keep_going = True
    while keep_going:
        print("1. Deposit 2. Withdraw 3. Top-up Phone 4. Check Balance 5. Exit")
        choice = input("Pick an option: ")
        keep_going = user_input(choice, account)

# Start GUI
user_account = BankAccount("User", 100)
run_gui(user_account)