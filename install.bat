@echo off
echo Creating venv
python -m venv venv
echo Activation venv
call venv\Scripts\activate
echo Installing dependencies
pip install -r requirements.txt
echo Installation completed. Please run run.bat.
pause