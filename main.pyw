import json
import random
import string
import tkinter as tk
from tkinter import messagebox
import pyperclip
import requests
import time
import threading
import threading
import time
from tkinter import Tk, Canvas, PhotoImage, Label, Entry, Button, messagebox, Listbox, Text
from bs4 import BeautifulSoup
from selenium import webdriver

class PasswordManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        self.minsize(535, 450)
        self.config(padx=50, pady=50)

        # UI setup
        self.canvas = tk.Canvas(height=200, width=200)


# ---------------------------- GLOBAL VARIABLES ------------------------------- #
email_cache = []
session_id = None

# ---------------------------- STARTING SELENIUM ------------------------------- #
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')  # Run in headless mode
driver = webdriver.Chrome(options=chrome_options)

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

    password_list = [random.choice(letters) for _ in range(nr_letters)] + \
                    [random.choice(numbers) for _ in range(nr_numbers)]
    random.shuffle(password_list)

    formatted_password = '-'.join(''.join(password_list[i:i+4]) for i in range(0, len(password_list), 4))

    password_entry.delete(0, "end")
    password_entry.insert(0, formatted_password)
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
    temp_email_input = soup.find('input', {'class': 'mailtext'})
    
    if temp_email_input is None:
        messagebox.showinfo(title="Error", message="Failed to generate temporary email.")
        return
    
    temp_email = temp_email_input['value']
    session_id = response.cookies.get('PHPSESSID')
    
    my_minutemail_entry.delete(0, "end")
    my_minutemail_entry.insert(0, temp_email)
    pyperclip.copy(temp_email)

    email_listbox.delete(0, "end")

    email_content.config(state='normal')
    email_content.delete("1.0", "end")
    email_cache.clear()

    
    fetch_emails()
    threading.Thread(target=update_timer, daemon=True).start()
    
def update_timer():
    global session_id
    while True:
        try:
            driver.get('https://10minutemail.net/')
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            countdown_label.config(text=soup.find('span', {'id': 'time'}).text.strip())
            
            if not countdown_label["text"].strip() == "00:00":
                temp_email_button.config(state="disabled")
                my_minutemail_entry.config(state="readonly")

            # Check if the timer has ended
            if countdown_label["text"].strip() == "00:00":
                driver.quit()
                my_minutemail_entry.config(state="normal")
                timer_label.config(text="Timer ended!")
                break
        
        except Exception as e:
            messagebox.showinfo(title="Error", message=f"Failed to update timer: {e}")
          
    driver.quit()  # Close the browser instance

def fetch_emails():
    def check_inbox(session_id):
        global email_cache
        for _ in range(60):
            try:
                response = requests.get('https://10minutemail.net/mailbox.ajax.php', cookies={'PHPSESSID': session_id})
                soup = BeautifulSoup(response.text, 'html.parser')
                rows = soup.find_all('tr')
                
                email_listbox.delete(0, "end")
                email_cache.clear()
                
                if rows:
                    for row in rows:
                        cols = row.find_all('td')
                        if len(cols) >= 3:
                            from_email = cols[0].text.strip()
                            subject = cols[1].find('a').text.strip()
                            url = 'https://10minutemail.net/' + cols[1].find('a')['href']
                            email_cache.append({'from': from_email, 'subject': subject, 'url': url})
                            email_listbox.insert("end", f"From: {from_email} | Subject: {subject}")
            except Exception as e:
                email_listbox.delete(0, "end")
                email_listbox.insert("end", f"Error fetching emails: {e}")
            time.sleep(10)  # Update every 10 seconds

    threading.Thread(target=check_inbox, args=(session_id,), daemon=True).start()

# ---------------------------- READ EMAIL ------------------------------- #
def read_email(event=None):
    selection = email_listbox.curselection()
    
    if not selection:
        email_content.delete("1.0", "end")
        email_content.insert("1.0", "No email selected.")
        return
    
    selected_index = selection[0]

    if selected_index >= len(email_cache):
        email_content.delete("1.0", "end")
        email_content.insert("1.0", "Invalid email selection.")
        return

    email_data = email_cache[selected_index]
    email_url = email_data['url']

    try:
        response = requests.get(email_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        tab_content = soup.find('div', {'id': 'tab1'})
        mail_content = tab_content.find_all('div', {'class': 'mailinhtml'}) if tab_content else None

        if not mail_content:
            tab_content = soup.find('div', {'id': 'tab3'})
            mail_content = tab_content.find_all('p', {'class': 'mailinhtml'}) if tab_content else None

        if not mail_content:
            email_content.delete("1.0", "end")
            email_content.insert("1.0", "No email content found.")
            return

        email_text = "\n\n".join(content.get_text(separator="\n", strip=True) for content in mail_content)

        email_content.delete("1.0", "end")
        email_content.insert("1.0", email_text)

    except Exception as e:
        email_content.delete("1.0", "end")
        email_content.insert("1.0", f"Error retrieving email content: {e}")
    
    email_content.config(state='disabled')

# ---------------------------- SHOW PASSWORD GENERATOR FUNCTION ------------------------------- #
def show_password_generator():
    global logo_img

    window.minsize(width=535, height=450)

    canvas.delete(logo_img)
    logo_img = PhotoImage(file="logo.png")
    canvas.create_image(100, 100, image=logo_img)

    search_button.grid(row=1, column=2)
    generate_password_button.grid(row=3, column=2)
    add_button.grid(row=4, column=0, columnspan=3)
    hide_buttons_fields_and_labels_button.grid(row=8, columnspan=3)

    website_entry.grid(row=1, column=1)
    email_entry.grid(row=2, column=1)
    my_minutemail_entry.grid_forget()
    password_entry.grid(row=3, column=1)

    website_label.grid(row=1, column=0)
    email_label.config(text="Email/Username:")
    email_label.grid(row=2, column=0)
    password_label.grid(row=3, column=0)
    
    timer_label.grid_forget()
    countdown_label.grid_forget()
    list_box_Label.grid_forget()
    temp_email_button.grid_forget()
    email_listbox.grid_forget()
    email_content.grid_forget()

# ---------------------------- SHOW TEN MINUTE MAIL FUNCTION ------------------------------- #
def show_ten_minute_mail():
    global logo_img

    window.minsize(width=535, height=575)
    
    canvas.delete(logo_img)
    logo_img = PhotoImage(file="logoMyMail.png")
    canvas.create_image(100, 100, image=logo_img)
    
    search_button.grid_forget()
    generate_password_button.grid_forget()
    add_button.grid_forget()
    hide_buttons_fields_and_labels_button.grid_forget()
    
    website_entry.grid_forget()
    email_entry.grid_forget()
    my_minutemail_entry.grid(row=1, column=1)
    password_entry.grid_forget()

    website_label.grid_forget()
    email_label.config(text=" 10 Minute/Email:")
    email_label.grid(row=1, column=0)
    password_label.grid_forget()
    
    timer_label.grid(row=3, column=0)
    countdown_label.grid(row=3, column=1)
    list_box_Label.grid(row=4, column=1)

    temp_email_button.grid(row=1, column=2)
    email_listbox.grid(row=5, column=0, columnspan=3)
    email_content.grid(row=6, column=0, columnspan=3)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
window.minsize(width=535, height=450)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)
canvas.bind("<Button-1>", lambda event: show_password_generator())

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

timer_label = Label(text="Email Timer:")
countdown_label = Label(text="00:00")

list_box_Label = Label(text="Inbox")

website_entry = Entry(width=36)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=36)
email_entry.grid(row=2, column=1)
email_entry.insert(0, "yourEmail@googlemail.com")

my_minutemail_entry = Entry(width=36)

password_entry = Entry(width=36)
password_entry.grid(row=3, column=1)

search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2)

generate_password_button = Button(text="Generate Password", width=14, command=generate_password)
generate_password_button.grid(row=3, column=2)

add_button = Button(text="Add", width=60, command=save_password)
add_button.grid(row=4, column=0, columnspan=3)

temp_email_button = Button(text="Generate Email", width=14, command=create_temp_email)

hide_buttons_fields_and_labels_button = Button(text="Generate a 10 MinuteMail with MyMinuteMail", width=60, bg="#cdcccd",
                                               command=show_ten_minute_mail)                                               
hide_buttons_fields_and_labels_button.grid(row=8, columnspan=3)

email_listbox = Listbox(window, height=6, width=67)
email_listbox.bind("<Double-Button-1>", read_email)

email_content = Text(window, height=6, width=50, wrap="word")
email_content.config(state='disabled')

window.mainloop()
