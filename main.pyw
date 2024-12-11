import json
import random
import string
import pyperclip
from tkinter import Tk, Canvas, PhotoImage, Label, Entry, Button, messagebox

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = string.ascii_letters
    numbers = string.digits

    password_length = 24

    nr_letters = random.randint(8, 10)
    nr_numbers = random.randint(2, 4)

    while nr_letters + nr_numbers < password_length:
        if nr_letters < 10:
            nr_letters += 1
        else:
            nr_numbers += 1

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_numbers
    random.shuffle(password_list)

    # Insert a dash after every 4 characters
    password = ''.join(password_list)
    formatted_password = '-'.join(password[i:i+4] for i in range(0, len(password), 4))

    password_entry.delete(0, "end")
    password_entry.insert(0, formatted_password)

    # After Adding the password you can just paste it with ctrl + v
    pyperclip.copy(formatted_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()
    
    if not website or not email or not password:
        messagebox.showinfo(title="Oops", message="Please fill in all fields.")
        return

    new_data = {website: {"email": email, "password": password}}
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        data = {}

    data.update(new_data)

    with open("data.json", "w") as data_file:
        json.dump(data, data_file, indent=4)

    website_entry.delete(0, "end")
    password_entry.delete(0, "end")

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get().strip()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found.")
        return

    if website in data:
        email = data[website]["email"]
        password = data[website]["password"]
        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
    else:
        messagebox.showinfo(title="Error", message=f"No details for {website} found.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
Label(text="Website:").grid(row=1, column=0)
Label(text="Email/Username:").grid(row=2, column=0)
Label(text="Password:").grid(row=3, column=0)

# Entries/Fields
website_entry = Entry(width=36)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=36)
email_entry.grid(row=2, column=1)

# Change your Email here if you want
email_entry.insert(0, "yourEmail@googlemail.com")

password_entry = Entry(width=36)
password_entry.grid(row=3, column=1)

# Buttons
Button(text="Search", width=14, command=find_password).grid(row=1, column=2)
Button(text="Generate Password", width=14, command=generate_password).grid(row=3, column=2)
Button(text="Add", width=60, command=save_password).grid(row=4, column=0, columnspan=3)

window.mainloop()
