<h1 align="center">
	Password Manager
<p align=center>
<a href="http://makeapullrequest.com"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg"></a>
<a href="https://github.com/DanEm95"><img src="https://img.shields.io/badge/lead-DanEm95-lightblue"></a>
<a href="https://github.com/DanEm95/passwordManager/releases"><img src="https://img.shields.io/github/v/release/DanEm95/passwordManager.svg?label= version"></a>
</p>
</h1>

<h3 align="">
	Password Manager is a simple Python application that helps you securely store and manage your passwords. Or use 10 Minute Mail to keep your personal email out of potential spam.
</h3>

<h1 align="">
	Showcase
</h1>

[myPassShowcase.mp4](https://github.com/user-attachments/assets/0b750d0f-6423-4027-8956-797edcc99ab7)


## Installation

To run the Password Manager you will need to have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

1. Clone this repository:
   ```bash
   git clone https://github.com/DanEm95/passwordManager.git
2. Install the required packages:
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
