@echo off

echo este programa requiere mega cmd

python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt

python main.py
