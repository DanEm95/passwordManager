' Datei: startPasswordManager.vbs

Set fso = CreateObject("Scripting.FileSystemObject")
Set WshShell = CreateObject("WScript.Shell")
' Ordner, in dem die VBS-Datei liegt
base = fso.GetParentFolderName(WScript.ScriptFullName)
' Pfad zu pythonw.exe im venv
pythonw = base & "\.venv\Scripts\pythonw.exe"
' Pfad zu main.pyw im selben Ordner
mainpyw = base & "\main.pyw"
' Starten, unsichtbar (0)
WshShell.Run """" & pythonw & """ """ & mainpyw & """", 0
