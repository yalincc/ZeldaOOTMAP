@echo off
cd /d "%~dp0"
if not exist ootnavi-pc.exe (
  go build -trimpath -ldflags "-s -w" -o ootnavi-pc.exe .
)
ootnavi-pc.exe
pause
