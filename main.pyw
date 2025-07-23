from tkinter import END, Tk, Canvas, PhotoImage, Label, Entry, Button, messagebox, Listbox, Text, filedialog
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
import keyring

# ---------------------------- GLOBAL VARIABLES ------------------------------- #
email_cache = []
session_id = None
driver = None

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

    keyring.set_password(website, email, password)

    new_data = {website: {"email": email}}
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
        messagebox.showinfo(title="Error", message="No data.json file found.")
        return

    if not data:
        messagebox.showinfo(title="Error", message="No passwords stored in the data.json file. Please add some passwords first.")
        return

    search_button.config(state='disabled')
    root = Tk()
    root.title("Select Website")

    def on_close():
        search_button.config(state='normal')
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
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
                messagebox.showinfo(title="Error", message="No data.json file found.")
                return

            if website in data:
                email = data[website]["email"]
                password = keyring.get_password(website, email)

                if password is None:
                    messagebox.showinfo(
                        title="Warning",
                        message="<No password was found in the keyring>"
                    )
                    password = ""
                else:
                    pyperclip.copy(password)

                website_entry.delete(0, "end")
                website_entry.insert(0, website)
                email_entry.delete(0, "end")
                email_entry.insert(0, email)
                password_entry.delete(0, "end")
                password_entry.insert(0, password)
                search_button.config(state='normal')
                root.destroy()                
            else:
                messagebox.showinfo(title="Error", message=f"No details for {website} found.")

    button = Button(root, text="Insert into entry and close listbox", command=insert_into_entry)
    button.pack(pady=10)

    def delete_from_listbox():
        selected_index = listbox.curselection()
        if selected_index:
            data_index = selected_index[0]
            website = listbox.get(data_index)
            try:
                data = read_json("data.json")
            except FileNotFoundError:
                messagebox.showinfo(title="Error", message="No data.json file found.")
                return

            if website in data:
                email = data[website]["email"]
                keyring.delete_password(website, email)
                del data[website]
                write_json("data.json", data)
                listbox.delete(selected_index)
                search_button.config(state='disabled')
                messagebox.showinfo(title="Success", message=f"Details for {website} deleted successfully.")
                if not listbox.get(0, END):
                    root.destroy()
            else:
                messagebox.showinfo(title="Error", message=f"No details for {website} found.")

    delete_button = Button(root, text="Delete from listbox", command=delete_from_listbox)
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
    global session_id, driver, email_cache
    try:
        if driver:
            driver.quit()
    except:
        pass
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome(options=chrome_options)

    driver.get('https://10minutemail.net/')
    temp_email_input = driver.find_element(By.CLASS_NAME, 'mailtext')

    if temp_email_input is None:
        messagebox.showinfo(title="Error", message="Failed to generate temporary email.")
        return

    temp_email = temp_email_input.get_attribute('value')
    session_id = driver.get_cookie('PHPSESSID')['value']

    my_minutemail_entry.config(state="normal")
    my_minutemail_entry.delete(0, "end")
    my_minutemail_entry.insert(0, temp_email)
    my_minutemail_entry.config(state="readonly")
    pyperclip.copy(temp_email)

    email_listbox.delete(0, "end")
    email_content.config(state='normal')
    email_content.delete("1.0", "end")
    email_content.config(state="disabled")
    email_cache = []

    extend_button.config(state="normal")
    temp_email_button.config(state="disabled")
    countdown_label.config(text="10:00")
    threading.Thread(target=fetch_emails, daemon=True).start()
    threading.Thread(target=update_timer, daemon=True).start()

def extend_email_time():
    try:
        driver.find_element(By.CSS_SELECTOR, 'a[href="more.html"]').click()
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        timer_text = soup.find('span', {'id': 'time'}).text.strip()
        countdown_label.config(text=timer_text)
    except Exception as e:
        messagebox.showinfo(title="Error", message=f"Renewal not possible: {str(e)}")

def fetch_emails():
    global email_cache
    session = requests.Session()
    session.cookies.set('PHPSESSID', session_id)

    previous_cache = []

    for i in range(60):
        try:
            response = session.get('https://10minutemail.net/mailbox.ajax.php', timeout=5)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            rows = soup.find_all('tr')

            new_cache = []
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    from_email = cols[0].text.strip()
                    subject_tag = cols[1].find('a')
                    if subject_tag:
                        subject = subject_tag.text.strip()
                        url = 'https://10minutemail.net/' + subject_tag['href']
                        new_cache.append({'from': from_email, 'subject': subject, 'url': url, 'content': None})

            if new_cache != previous_cache:
                window.after(0, lambda: email_listbox.delete(0, "end"))
                email_cache.clear()
                email_cache.extend(new_cache)
                for mail in email_cache:
                    window.after(0, lambda m=mail: email_listbox.insert("end", f"From: {m['from']} | Subject: {m['subject']}"))
                previous_cache = new_cache

        except requests.exceptions.RequestException as e:
            window.after(0, lambda: email_listbox.delete(0, "end"))
            window.after(0, lambda: email_listbox.insert("end", "Your email is loading, please wait..."))

        time.sleep(10)

def read_email(event=None):
    selection = email_listbox.curselection()
    if not selection:
        email_content.config(state="normal")
        email_content.delete("1.0", "end")
        email_content.insert("1.0", "No email selected.")
        email_content.config(state="disabled")
        return

    selected_index = selection[0]
    if selected_index >= len(email_cache):
        email_content.config(state="normal")
        email_content.delete("1.0", "end")
        email_content.insert("1.0", "Invalid email selection.")
        email_content.config(state="disabled")
        return

    email_data = email_cache[selected_index]
    if email_data.get("content") is not None:
        email_content.config(state="normal")
        email_content.delete("1.0", "end")
        email_content.insert("1.0", email_data["content"])
        email_content.config(state="disabled")
        print("Email content loaded from cache.")
        return

    email_url = email_data["url"]

    try:
        driver.get(email_url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        tab_content = soup.find('div', {'id': 'tab1'})
        mail_content = tab_content.find_all('div', {'class': 'mailinhtml'}) if tab_content else None

        if not mail_content:
            tab_content = soup.find('div', {'id': 'tab3'})
            mail_content = tab_content.find_all('p', {'class': 'mailinhtml'}) if tab_content else None
        if not mail_content:
            email_content.config(state="normal")
            email_content.delete("1.0", "end")
            email_content.insert("1.0", "No email content found.")
            email_content.config(state="disabled")
            return

        email_text = "\n\n".join(content.get_text(separator="\n", strip=True) for content in mail_content)
        email_data["content"] = email_text

        email_content.config(state="normal")
        email_content.delete("1.0", "end")
        email_content.insert("1.0", email_text)

    except Exception as e:
        email_content.config(state="normal")
        email_content.delete("1.0", "end")
        email_content.insert("1.0", f"Error retrieving email content: {e}")

    email_content.config(state="disabled")

def update_timer():
    global driver, session_id, email_cache
    timer_has_ended = False
    while True:
        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            timer_span = soup.find('span', {'id': 'time'})
            timer_text = timer_span.text.strip() if timer_span else "00:00"
            window.after(0, lambda: countdown_label.config(text=timer_text))

            if timer_text == "00:00" and not timer_has_ended:
                timer_has_ended = True
                window.after(0, lambda: extend_button.config(state="disabled"))
                window.after(0, lambda: temp_email_button.config(state="normal"))
                window.after(0, lambda: my_minutemail_entry.config(state="normal"))
                window.after(0, lambda: my_minutemail_entry.delete(0, "end"))
                window.after(0, lambda: email_listbox.delete(0, "end"))
                window.after(0, lambda: email_content.config(state="normal"))
                window.after(0, lambda: email_content.delete("1.0", "end"))
                window.after(0, lambda: email_content.config(state="disabled"))
                email_cache.clear()
                window.after(0, lambda: countdown_label.config(text="Timer ended!", anchor='w'))
                try:
                    driver.quit()
                except: pass
                driver = None
                break

            elif timer_text != "00:00":
                window.after(0, lambda: temp_email_button.config(state="disabled"))
                window.after(0, lambda: my_minutemail_entry.config(state="readonly"))
                window.after(0, lambda: extend_button.config(state="normal"))

        except Exception as e:
            continue

        time.sleep(1)

# ---------------------------- EXPORT JSON ------------------------------- #
def export_full_json():
    try:
        data = read_json("data.json")
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data.json file found.")
        return

    export_data = {}
    for website, info in data.items():
        email = info.get("email", "")
        password = keyring.get_password(website, email)
        export_data[website] = {
            "email": email,
            "password": password if password is not None else ""
        }

    json_file = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json")],
        title="Export as a JSON file"
    )
    if not json_file:
        return

    try:
        with open(json_file, "w", encoding="utf-8") as jf:
            json.dump(export_data, jf, indent=4)
        messagebox.showinfo(title="Export successfully.", message=f"The data has been saved at {json_file}.")
    except Exception as e:
        messagebox.showinfo(title="Error", message=f"Export failed: {e}")

# ---------------------------- SHOW PASSWORD GENERATOR FUNCTION ------------------------------- #
def show_password_generator():
    global logo_img
    window.minsize(width=535, height=450)

    canvas.delete(logo_img)
    logo_img = PhotoImage(file="logoMyPass.png")
    canvas.create_image(100, 100, image=logo_img)

    search_button.grid(row=1, column=2)
    generate_password_button.grid(row=3, column=2)
    add_button.grid(row=4, column=0, columnspan=3)
    export_json_button.grid(row=9, columnspan=3, pady=10)
    hide_buttons_fields_and_labels_button.grid(row=8, columnspan=3)
    extend_button.grid_forget()
    website_entry.grid(row=1, column=1)
    email_entry.grid(row=2, column=1)
    my_minutemail_entry.grid_forget()
    password_entry.grid(row=3, column=1)
    website_label.grid(row=1, column=0, sticky='w')
    email_label.config(text="Email/Username:", anchor='w')
    email_label.grid(row=2, column=0, sticky='w')
    password_label.grid(row=3, column=0, sticky='w')
    toggle_button.grid(row=3, column=3, padx=(5, 0))
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
    export_json_button.grid_forget()
    hide_buttons_fields_and_labels_button.grid_forget()
    website_entry.grid_forget()
    email_entry.grid_forget()
    my_minutemail_entry.grid(row=1, column=1)
    password_entry.grid_forget()
    website_label.grid_forget()
    email_label.config(text="10 minute email:")
    email_label.grid(row=1, column=0)
    password_label.grid_forget()
    toggle_button.grid_forget()
    extend_button.grid(row=2, column=1, pady=5, sticky='nsew')
    timer_label.grid(row=3, column=0, sticky='w')
    countdown_label.grid(row=3, column=1)
    list_box_Label.grid(row=4, column=1)
    temp_email_button.grid(row=1, column=2, padx=5)
    email_listbox.grid(row=5, column=0, columnspan=3, sticky='nsew')
    email_content.grid(row=6, column=0, columnspan=3, sticky='nsew')

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
window.minsize(width=535, height=450)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logoMyPass.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)
canvas.bind("<Button-1>", lambda event: show_password_generator())

website_label = Label(text="Website:", anchor='w')
website_label.grid(row=1, column=0, sticky='w')

email_label = Label(text="Email/Username:", anchor='w')
email_label.grid(row=2, column=0, sticky='w')

password_label = Label(text="Password:", anchor='w')
password_label.grid(row=3, column=0, sticky='w')

timer_label = Label(text="Email timer:", anchor='w')
countdown_label = Label(text="00:00")

list_box_Label = Label(text="Inbox")

website_entry = Entry(width=36)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=36)
email_entry.grid(row=2, column=1)
email_entry.insert(0, "yourEmail@googlemail.com")

my_minutemail_entry = Entry(width=36, justify='center')

password_entry = Entry(width=36, show="*")
password_entry.grid(row=3, column=1)
def toggle_password():
    if password_entry.cget('show') == "":
        password_entry.config(show="*")
        toggle_button.config(text="🙈")
    else:
        password_entry.config(show="")
        toggle_button.config(text="🙉")

toggle_button = Button(window, text="🙈", command=toggle_password, width=2)
toggle_button.grid(row=3, column=3, padx=(5, 0))


search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(row=1, column=2)

generate_password_button = Button(text="Generate password", width=14, command=generate_password)
generate_password_button.grid(row=3, column=2)

add_button = Button(text="Add", width=60, command=save_password)
add_button.grid(row=4, column=0, columnspan=3)

export_json_button = Button(text="Export as a JSON file", width=20, command=export_full_json)
export_json_button.grid(row=9, columnspan=3, pady=10)

temp_email_button = Button(text="Generate email", width=14, command=create_temp_email)

hide_buttons_fields_and_labels_button = Button(text="Generate a 10 minute email with MyMail", width=60, bg="#cdcccd",
                                               command=show_ten_minute_mail)                                               
hide_buttons_fields_and_labels_button.grid(row=8, columnspan=3)

extend_button = Button(text="I need 10 more minutes", width=17, state="disabled", command=extend_email_time)

email_listbox = Listbox(window, height=6, width=67, borderwidth=0, highlightthickness=4, highlightcolor="#f0f0f0", highlightbackground="#f0f0f0")
email_listbox.bind("<Double-Button-1>", read_email)

email_content = Text(window, height=6, width=50, wrap="word", borderwidth=0, highlightthickness=4, highlightcolor="#f0f0f0", highlightbackground="#f0f0f0")
email_content.config(state='disabled')

window.mainloop()
