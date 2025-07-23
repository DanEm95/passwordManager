def save_password():
    website = website_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    if not website or not email or not password:
        messagebox.showinfo(title="Oops", message="Please fill in all fields.")
        return

    # Passwort immer (neu) speichern – überschreibt ggf. vorhandenes
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
