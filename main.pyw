import json
import random
import string
import pyperclip
import requests
import time
import threading
from tkinter import Tk, Canvas, PhotoImage, Label, Entry, Button, messagebox, Listbox, Scrollbar, Text
from bs4 import BeautifulSoup

# ---------------------------- GLOBAL VARIABLES ------------------------------- #
email_cache = []  # To store fetched emails
session_id = None  # Session ID for temp email inbox

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

# ---------------------------- TEMPORARY EMAIL FUNCTIONS ------------------------------- #
def create_temp_email():
    global session_id
    response = requests.get('https://10minutemail.net/')
    soup = BeautifulSoup(response.text, 'html.parser')
    temp_email = soup.find('input', {'class': 'mailtext'})['value']
    session_id = response.cookies.get('PHPSESSID')

    email_entry.delete(0, "end")
    email_entry.insert(0, temp_email)
    email_listbox.delete(0, "end")
    fetch_emails()
    
    threading.Thread(target=update_timer, daemon=True).start()

def update_timer():
    for remaining in range(600, -1, -1):
        mins, secs = divmod(remaining, 60)
        countdown_label.config(text=f"{mins:02d}:{secs:02d}")
        time.sleep(1)
        if remaining == 0:
            countdown_label.config(text="Timer ended!")

def fetch_emails():
    def check_inbox(session_id):
        for _ in range(60):
            try:
                response = requests.get('https://10minutemail.net/mailbox.ajax.php', cookies={'PHPSESSID': session_id})
                soup = BeautifulSoup(response.text, 'html.parser')
                rows = soup.find_all('tr')
                
                email_listbox.delete(0, "end")  # Clear listbox before updating
                
                if rows:
                    for row in rows:
                        cols = row.find_all('td')
                        if len(cols) >= 3:
                            sender = cols[0].text.strip()  # "From"
                            subject_link = cols[1].find('a')  # "Subject"
                            subject = subject_link.text.strip() if subject_link else "No subject"
                            
                            # Build the string for the inbox
                            email_entry = f"From: {sender} | Subject: {subject}"
                            email_listbox.insert("end", email_entry)
                else:
                    email_listbox.insert("end", "No new emails.")
                
                time.sleep(10)  # Update every 10 seconds
                
            except Exception as e:
                email_listbox.delete(0, "end")
                email_listbox.insert("end", f"Error fetching emails: {e}")
                break  # Stop further attempts if an error occurs
    
    threading.Thread(target=check_inbox, args=(session_id,), daemon=True).start()

# ---------------------------- READ EMAIL ------------------------------- #
def read_email(event):
    # Get the selected index from the email listbox
    selection = email_listbox.curselection()
    
    if not selection:
        email_content.delete("1.0", "end")
        email_content.insert("1.0", "No email selected.")
        return

    # Extract selected email details
    selected_index = selection[0]
    selected_email = email_listbox.get(selected_index)

    # Simulate fetching detailed content (if applicable)
    try:
        response = requests.get(f"https://10minutemail.net/mailbox.ajax.php", cookies={'PHPSESSID': session_id})
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr')
        
        if selected_index < len(rows):
            email_details = rows[selected_index]
            email_body = email_details.text.strip()
        else:
            email_body = "No content available for this email."

        # Display the email content
        email_content.delete("1.0", "end")
        email_content.insert("1.0", email_body)
    except Exception as e:
        email_content.delete("1.0", "end")
        email_content.insert("1.0", f"Error retrieving email content: {e}")

# ---------------------------- SHOW BUTTONS, FIELDS, AND LABELS FUNCTION ------------------------------- #
def show_password_generator():
    # Show buttons
    search_button.grid(row=1, column=2)
    generate_password_button.grid(row=3, column=2)
    add_button.grid(row=4, column=0, columnspan=3)
    hide_buttons_fields_and_labels_button.grid(row=8, columnspan=3)

    # Show entry fields
    website_entry.grid(row=1, column=1)
    email_entry.grid(row=2, column=1)
    password_entry.grid(row=3, column=1)

    # Show labels
    website_label.grid(row=1, column=0)
    email_label.grid(row=2, column=0)
    password_label.grid(row=3, column=0)
    
    # Hide labels
    timer_label.grid_forget()
    countdown_label.grid_forget()
    list_box_Label.grid_forget()
    
    # Hide temp_email_button 
    temp_email_button.grid_forget()

    # Hide ListBox
    email_listbox.grid_forget()

    # Hide Email Content Viewer
    email_content.grid_forget()

# ---------------------------- HIDE BUTTONS, FIELDS, AND LABELS FUNCTION ------------------------------- #
def show_ten_minute_mail():
    global temp_email_button
    # Hide buttons
    search_button.grid_forget()
    generate_password_button.grid_forget()
    add_button.grid_forget()
    hide_buttons_fields_and_labels_button.grid_forget()
    
    # Hide entry fields
    website_entry.grid_forget()
    password_entry.grid_forget()

    # Hide labels
    website_label.grid_forget()
    password_label.grid_forget()
    timer_label.grid(row=3, column=0)
    countdown_label.grid(row=3, column=1)
    list_box_Label.grid(row=4, column=1)
    
    # Move temp_email_button next to email_entry
    temp_email_button.grid(row=2, column=2)

    # ListBox
    email_listbox.grid(row=5, column=0, columnspan=3)
    
    # Email Content Viewer
    email_content.grid(row=6, column=0, columnspan=3)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Logo
canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Bind click event to logo image to show all components again
canvas.bind("<Button-1>", lambda event: show_password_generator())

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

timer_label = Label(text="Email Timer:")
countdown_label = Label(text="10:00")

list_box_Label = Label(text="Inbox")

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
search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2)

generate_password_button = Button(text="Generate Password", width=14, command=generate_password)
generate_password_button.grid(row=3, column=2)

add_button = Button(text="Add", width=60, command=save_password)
add_button.grid(row=4, column=0, columnspan=3)

temp_email_button = Button(text="Generate Email", width=14, command=create_temp_email)

# Button to hide other buttons, fields and labels
hide_buttons_fields_and_labels_button = Button(text="Generate a 10 MinuteMail with MyMinuteMail", width=60, bg="#cdcccd",
                                               command=show_ten_minute_mail)                                               
hide_buttons_fields_and_labels_button.grid(row=8, columnspan=3)

# Email Listbox and Scrollbar
email_listbox = Listbox(window, height=6, width=67)
email_listbox.bind("<Double-Button-1>", read_email)

# Email Content Viewer
email_content = Text(window, height=6, width=50, wrap="word")

window.mainloop()
