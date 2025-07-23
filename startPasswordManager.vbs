' File: startPasswordManager.vbs

Set fso = CreateObject("Scripting.FileSystemObject")
Set WshShell = CreateObject("WScript.Shell")
' Folder where the VBS file is located
base = fso.GetParentFolderName(WScript.ScriptFullName)
' Path to pythonw.exe in venv
pythonw = base & "\.venv\Scripts\pythonw.exe"
' Path to main.pyw in the same folder
mainpyw = base & "\main.pyw"
' Start, invisible (0)
WshShell.Run """" & pythonw & """ """ & mainpyw & """", 0
