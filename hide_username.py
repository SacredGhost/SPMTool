import tkinter as tk
from tkinter import simpledialog

def get_username():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    username = simpledialog.askstring("Username", "Please enter your username:")

    # If the user clicks "Cancel" or closes the window without entering a username, the result will be None
    if username is not None:
        return username.strip()  # Strip any leading or trailing spaces from the input
    else:
        return None

# Example usage:
if __name__ == "__main__":
    username = get_username()
    if username:
        print(f"Hello, {username}!")
    else:
        print("No username entered.")
