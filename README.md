<h1 align="center">
	Password Manager
<p align=center>
<a href="http://makeapullrequest.com"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg"></a>
<a href="https://github.com/DanEm95"><img src="https://img.shields.io/badge/lead-DanEm95-lightblue"></a>
<a href="https://github.com/DanEm95/passwordManager/releases"><img src="https://img.shields.io/github/v/release/DanEm95/passwordManager.svg?label=version "></a>
</p>
</h1>

<h3 align="center">
Password Manager is a simple Python application that helps you securely store and manage your passwords.
</h3>

<h1 align="center">Showcase</h1>
	<div align="center" >
		<h3>MyPass</h3>
		<img src="https://github.com/DanEm95/passwordManager/blob/main/passwordManager.PNG" alt="passwordManager">
	</div>
	<div align="center" >
		<h3>MyMinuteMail BETA</h3>
		<img src="https://github.com/DanEm95/passwordManager/blob/main/myMinuteMail.PNG" alt="passwordManager">
	</div>

## Installation

To run the Password Manager you will need to have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

1. Clone this repository:
   ```bash
   git clone https://github.com/DanEm95/passwordManager.git
2. Install the required packages:
   ```bash
   pip install pyperclip requests beautifulsoup4

## MyPass Usage
````
1. Open the main.pyw file to launch the application.
2. Fill in the fields:
 	- Website: Enter the name of the website for which you want to save the password.
 	- Email/Username: Enter your email or username associated with this website.
3. Click Generate Password to generate a strong password.
	- The generated password will automatically be copied to your clipboard.
4. Click Add to securely store your details in the JSON.
5. You can now paste the password directly where you need it by pressing Ctrl + V.
6. To retrieve a saved password, enter the website name and click on Search.

## MyMinuteMail usage
### Note: To return to MyPass, simply click on the logo
````
1. Click on the 'Generate a 10 MinuteMail with MyMinuteMail' button in MyPass.
2. Generate a temporary email:
	- Click "Generate email" to obtain a temporary email address.
	- The email will be automatically filled in the Email/Username field.
3. Email Viewer:
	- Double-click an email in the list to view its contents.

## Features
 - Generate strong, random passwords.
 - Securely store and retrieve passwords.
 - Automatically copy generated passwords to clipboard for easy access.
 - Manage temporary 10 minute emails for website signups to avoid using your personal email

## Updated v1.1.2 changes
 - Update README with new features and changes.
 - Improved UI: Includes improved navigation between password management and temporary email features.
 - Bug fixes and performance enhancements: Various updates to ensure a smoother operation and better user experience.

## Contribute
Pull requests are welcome! If you have suggestions for improvements or new features, please open a new issue to discuss what you would like to see changed.