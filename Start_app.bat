@echo off
title My Streamlit App Launcher
cd /d "%~dp0"

echo ----------------------------------------
echo Launching Streamlit App...
echo Please wait while the server starts!
echo ----------------------------------------

streamlit run app.py

echo ----------------------------------------
echo Press any key to close this window.
pause > nul
exit
