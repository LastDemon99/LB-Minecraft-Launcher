@echo off

IF NOT EXIST venv (
    echo Creating venv...
    python -m venv venv
    echo Activating venv...
    call venv\Scripts\activate
    echo Installing required packages...
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

python LB_Launcher.py