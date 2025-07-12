@echo off
setlocal

REM ---- Check if Python is installed ----
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python not found. Downloading and installing Python...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe -OutFile python-installer.exe"
    start /wait python-installer.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
    del python-installer.exe
    set "PATH=%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python312\Scripts;%PATH%"
    echo Python installed.
) else (
    echo Python is already installed. Updating to the latest version...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.12.3/python-3.12.3-amd64.exe -OutFile python-installer.exe"
    start /wait python-installer.exe /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
    del python-installer.exe
    set "PATH=%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python312\Scripts;%PATH%"
    echo Python updated.
)

REM ---- Upgrade pip ----
python -m pip install --upgrade pip

REM ---- Create virtual environment ----
python -m venv .venv

REM ---- Activate virtual environment ----
call .venv\Scripts\activate

REM ---- Upgrade pip in venv ----
python -m pip install --upgrade pip

REM ---- Install or upgrade required packages ----
pip install --upgrade beautifulsoup4 selenium pyperclip requests keyring

REM ---- Start the main program ----
start "" ".venv\Scripts\pythonw.exe" "%CD%\main.pyw"

echo.
echo Setup complete! The Password Manager should now be running.
