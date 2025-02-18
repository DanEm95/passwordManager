from tkinter import END, Tk, Canvas, PhotoImage, Label, Entry, Button, messagebox, Listbox, Text
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import string
import pyperclip
import requests
import time
import threading
import secrets
import string

# ---------------------------- GLOBAL VARIABLES ------------------------------- #
email_cache = []
session_id = None

# ---------------------------- STARTING SELENIUM ------------------------------- #
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')  # Run in headless mode
driver = webdriver.Chrome(options=chrome_options)

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_length = 20
    pool = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(pool) for _ in range(password_length))
    formatted_password = '-'.join(password[i:i+6] for i in range(0, len(password), 7))

    password_entry.delete(0, END)
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
        data = read_json("data.json")
    except FileNotFoundError:
        data = {}

    data.update(new_data)
    write_json("data.json", data)

    website_entry.delete(0, "end")
    password_entry.delete(0, "end")

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    try:
        data = read_json("data.json")
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found.")
        return

    if not data:
        messagebox.showinfo(title="Error", message="No passwords stored in JSON file. Please save some passwords first.")
        return

    def select_data():
        selected_index = listbox.curselection()
        if selected_index:
            data_index = selected_index[0]
            website = listbox.get(data_index)
            try:
                data = read_json("data.json")
            except FileNotFoundError:
                messagebox.showinfo(title="Error", message="No data file found.")
                return

            if website in data:
                email = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
            else:
                messagebox.showinfo(title="Error", message=f"No details for {website} found.")
    search_button.config(state='disabled')
    root = Tk()
    root.title("Select Website")
    listbox = Listbox(root, width=50, height=20)
    listbox.pack(pady=10)

    for website in data:
        listbox.insert(END, website)

    def insert_into_entry():
        selected_index = listbox.curselection()
        if selected_index:
            data_index = selected_index[0]
            website = listbox.get(data_index)
            try:
                data = read_json("data.json")
            except FileNotFoundError:
                messagebox.showinfo(title="Error", message="No data file found.")
                return

            if website in data:
                email = data[website]["email"]
                password = data[website]["password"]
                website_entry.delete(0, "end")
                website_entry.insert(0, website)
                email_entry.delete(0, "end")
                email_entry.insert(0, email)
                password_entry.delete(0, "end")
                password_entry.insert(0, password)
                pyperclip.copy(password)
                search_button.config(state='normal')
                root.destroy()
            else:
                messagebox.showinfo(title="Error", message=f"No details for {website} found.")
    button = Button(root, text="Insert into Entry and Close Listbox", command=insert_into_entry)
    button.pack(pady=10)

    def delete_and_close():
        selected_index = listbox.curselection()
        if selected_index:
            data_index = selected_index[0]
            website = listbox.get(data_index)
            try:
                data = read_json("data.json")
            except FileNotFoundError:
                messagebox.showinfo(title="Error", message="No data file found.")
                return

            if website in data:
                del data[website]
                write_json("data.json", data)
                listbox.delete(selected_index)
                search_button.config(state='normal')

                # Check if the list is empty after deletion
                if not listbox.get(0, END):
                    root.destroy()
            else:
                messagebox.showinfo(title="Error", message=f"No details for {website} found.")

    delete_button = Button(root, text="Delete From Listbox", command=delete_and_close)
    delete_button.pack(pady=10)
    root.mainloop()

# ---------------------------- FILE HANDLING UTILS ------------------------------- #
def read_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def write_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# ---------------------------- TEMPORARY EMAIL FUNCTIONS ------------------------------- #
def create_temp_email():
    global session_id
    driver.get('https://10minutemail.net/')

    temp_email_input = driver.find_element(By.CLASS_NAME, 'mailtext')

    if temp_email_input is None:
        messagebox.showinfo(title="Error", message="Failed to generate temporary email.")
        return
    
    temp_email = temp_email_input.get_attribute('value')
    session_id = driver.get_cookie('PHPSESSID')['value']
    
    my_minutemail_entry.delete(0, "end")
    my_minutemail_entry.insert(0, temp_email)
    pyperclip.copy(temp_email)

    email_listbox.delete(0, "end")

    email_content.config(state='normal')
    email_content.delete("1.0", "end")
    email_cache.clear()

    
    fetch_emails()
    threading.Thread(target=update_timer, daemon=True).start()
    
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
        driver.get(email_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
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

        email_content.config(state='normal')
        email_content.delete("1.0", "end")
        email_content.insert("1.0", email_text)

    except Exception as e:
        email_content.delete("1.0", "end")
        email_content.insert("1.0", f"Error retrieving email content: {e}")
    
    email_content.config(state='disabled')

def update_timer():
    global session_id
    while True:
        try:
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

hide_buttons_fields_and_labels_button = Button(text="Generate a 10 Minute Mail with MyMail", width=60, bg="#cdcccd",
                                               command=show_ten_minute_mail)                                               
hide_buttons_fields_and_labels_button.grid(row=8, columnspan=3)

email_listbox = Listbox(window, height=6, width=67)
email_listbox.bind("<Double-Button-1>", read_email)

email_content = Text(window, height=6, width=50, wrap="word")
email_content.config(state='disabled')

window.mainloop()
