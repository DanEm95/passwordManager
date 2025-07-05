<h1 align="center">
	Password Manager
<p align=center>
<a href="http://makeapullrequest.com"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg"></a>
<a href="https://github.com/DanEm95"><img src="https://img.shields.io/badge/lead-DanEm95-lightblue"></a>
<a href="https://github.com/DanEm95/passwordManager/releases"><img src="https://img.shields.io/github/v/release/DanEm95/passwordManager.svg?label=version"></a>
</p>
</h1>

<h3 align="">
	Password Manager is a simple Python application that helps you securely store and manage your passwords. Or use 10 Minute Mail to keep your personal email out of potential spam.
</h3>

<h1 align="">
	Showcase
</h1>

[myPassShowcase.mp4](https://github.com/user-attachments/assets/0b750d0f-6423-4027-8956-797edcc99ab7)


## Installation with start.bat

1. Go to the [Password Manager GitHub page](https://github.com/DanEm95/passwordManager).
2. Click the green **Code** button at the top right.
3. Select **Download ZIP** to download the project.
4. Choose any folder you like and extract the ZIP file there, or create a folder called 'dev' on your C: drive (e.g. C:\dev\) and extract the ZIP file there.
5. Open the extracted Folder (passwordManager).
6. Double-click **start.bat**.

When you double-click the batch file, it will **automatically set up everything you need to run the Password Manager**, even if you have no programming experience. Here’s what will happen, step by step:

1. **Check for Python:**  
   The script first checks if Python is already installed on your computer.

2. **Install or Update Python:**  
   - If Python is **not installed**, it will automatically download and install the latest version of Python for you.
   - If Python **is already installed**, it will update Python to the newest version.

3. **Set Up a Safe Environment:**  
   The script creates a special ".venv" folder (called a “virtual environment”) inside your project. This keeps all the necessary files and settings for the Password Manager separate from the rest of your computer.

4. **Activate the Environment:**  
   It activates this environment so the next steps only affect your Password Manager and not other programs.

5. **Install and Update Required Tools:**  
   The script will download and update everything the Password Manager needs to work (like BeautifulSoup, Selenium, pyperclip, and requests). These are called “libraries” or “packages.”

6. **Start the Password Manager:**  
   Finally, the script will automatically start the Password Manager program for you.


## Manual Installation (Without start.bat)

To run the Password Manager you will need to have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

1. Clone this repository:
   ```bash
   git clone https://github.com/DanEm95/passwordManager.git
2. Create a virtual environment in the project folder:
   ```bash
	 python -m venv .venv
2. Activate the virtual environment:
   ```bash
	 .\.venv\Scripts\activate
4. Install the required packages:
   ```bash
	 pip install beautifulsoup4, selenium, pyperclip, requests

## MyPass Usage
```
1. Open the main.pyw file.
2. Fill in the fields:
 	- Website
 	- Email/Username
	- Password: Click Generate Password to generate a strong password. The generated password will automatically be copied to your clipboard.
4. Click Add to store your details in the data.json.
5. You can now paste the password directly where you need it by pressing Ctrl + V.
6. To retrieve a saved password, enter the website name and click on Search.
```

## MyMail usage
### Note: To return to MyPass, simply click on the logo
```
1. Click on the grey 'Generate a 10 MinuteMail with MyMail' button in MyPass.
2. To generate a temporary email address for 10 minutes:
	- Click "Generate email".
	- The email will be automatically filled in the Email field and copied to your clipboard.
2. Email Viewer:
	- Double-click an email in the Inbox list to view its contents.
```

## Features
 - Generate strong, random passwords.
 - Securely store and retrieve passwords.
 - Automatically copy generated passwords to clipboard for easy access.
 - Manage temporary 10 minute emails for website signups to avoid using your personal email.

## Updated v1.1.5 changes
 - Implemented Search logic
 - Update of the generate_password() function with secrets and string libraries
 - New listbox for selecting JSON data and displaying it in entries
 - Bug fixes and performance improvements: Updates to ensure smoother operation and better user experience.

## Contribute
Pull requests are welcome! If you have suggestions for improvements or new features, please open a new issue to discuss what you would like to see changed.
