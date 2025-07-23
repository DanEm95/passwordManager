<h1 align="center">
	Password Manager
<p align=center>
<a href="http://makeapullrequest.com"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg"></a>
<a href="https://github.com/DanEm95"><img src="https://img.shields.io/badge/lead-DanEm95-lightblue"></a>
<a href="https://github.com/DanEm95/passwordManager/releases"><img src="https://img.shields.io/github/v/release/DanEm95/passwordManager.svg?label=version"></a>
</p>
</h1>

<h3 align="">
	Password Manager is a simple Python application that helps you store and manage your passwords. Alternatively, use the included 10 minute email feature to prevent potential spam from reaching your own email addresses.
</h3>

<h1 align="">
	Showcase
</h1>

[myPassShowcase.mp4](https://github.com/user-attachments/assets/0b750d0f-6423-4027-8956-797edcc99ab7)


## Installation with installationStart.bat

**Note: This setup is configured for Windows only. For other operating systems, please inform yourself accordingly.**

1. To download the ZIP folder, either click [here](https://github.com/DanEm95/passwordManager/archive/refs/heads/main.zip), or click the green **Code** button at the top right.
2. If you clicked the green Code button, select **Local** at the top of the dropdown.
3. Select **Download ZIP** to download the project.
4. Extract the ZIP file and create a folder called "dev" on your C: drive (e.g. "C:\dev\") and extract the ZIP file there. Alternatively, you have the option to save it in any desired folder.
5. Open the extracted Folder (passwordManager).
6. Double-click **installationStart.bat**.
7. Once everything has been installed, you can start the Password Manager by clicking **startPasswordManager.vbs**.


When you double-click the **installationStart.bat** file, it will **automatically set up everything you need to run the Password Manager**, even if you have no programming experience. Here’s what will happen, step by step:

1. **Python**  
   The script first checks if Python is already installed on your computer.
  
   - If Python is **not installed**, it will automatically download and install the latest version of Python for you.
   - If Python **is already installed**, it will update Python to the newest version.

2. **Virtual environment**  
   The script creates a ".venv" folder (also called a “virtual environment”) inside your project. This keeps all the necessary files and settings for the Password Manager separate from the rest of your venv enviroments. Then, the virtual environment will be activated and all the libraries and packages required by the Password Manager, such as BeautifulSoup, Selenium, Pyperclip, Requests, and Keyring, will be downloaded and updated.

3. **Password Manager**  
   Finally, the script will automatically start the Password Manager program for you.


## Manual installation without installationStart.bat

**Note: This setup is configured for Windows only. For other operating systems, please inform yourself accordingly.**

To run the Password Manager you will need to have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

1. Clone this repository
   ```bash
   git clone https://github.com/DanEm95/passwordManager.git
2. Create a virtual environment in the project folder
   ```bash
	 python -m venv .venv
3. Activate the virtual environment
   ```bash
	 .\.venv\Scripts\activate
4. Install the required packages
   ```bash
	 pip install beautifulsoup4, selenium, pyperclip, requests, keyring

## How do I use MyPass?
```
1. Fill in the fields:
 	- Website
 	- Email/Username
	- Password: Click the "Generate password" button to generate a strong password. The generated password will automatically be copied to your clipboard.

2. Click "Add" to store your details in the "data.json". (The password will be stored in the Windows Credential Manager. It will not be stored in the "data.json" file).

3. You can now paste the password directly wherever you need it by pressing Ctrl+V. Alternatively, press Win+V to open/activate the clipboard.

4. To retrieve a saved password, click on "Search", select a website from the list and click on "Insert into entry and close listbox".

5. To delete a saved password, click on "Search", select a website from the list and click on "Delete from listbox".

6. To export all credentials, including passwords, to a JSON file, click "Export as a JSON file" (For example, you can then save the exported JSON file to a USB stick).
```
### Note: Be very careful with the exported JSON file because it stores all your passwords in plain text that is neither encrypted nor hashed. For example, you might save the JSON file to a USB drive so that you can quickly access and copy your passwords. However, anyone who gains access to the USB drive or the file can easily read your passwords. Make sure to keep the file in a safe place and never share it with others.

## How do I use MyMail?
```
1. In MyPass, click the gray "Generate a 10 minute email with MyMail" button.

2. To generate a temporary email address for 10 minutes, click "Generate email". The email address will automatically be filled into the "Email" field and copied to your clipboard.

3. Double-click an email in the Inbox list to view its contents.

4. To keep the same email for another 10 minutes, click the "I need 10 more minutes" button.
```
### Note: To return to MyPass, simply click on the logo

## Features
 - Generate strong, random passwords.
 - Store, retrieve and delete passwords.
 - Automatically copies the generated password and email to the clipboard for quick access.
 - Manage temporary 10 minute emails for website signups to avoid using your personal emails.

## Updated v1.1.7 changes
### Mymail
- Added show/hide password button (🙈/🙉).
- Added extend email time for 10 minutes button.
- Improved chromedriver management for temporary email.
- Email messages are now cached for quicker access.
- Entry/Inbox/Listbox cleanup when email timer goes to 00:00.
### MyPass
- Passwords are now stored in the Credential Manager (keyring) rather than in "data.json". 
- The "data.json" file is now only used to store website and email information.
- Added an export feature that saves your full login details, including passwords, as a JSON file.

## Contribute
Pull requests are welcome! If you have suggestions for improvements or new features, please open a new issue to discuss what you would like to see changed.
