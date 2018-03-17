# Python Telegram Bot for Find Nearest Pharmacies

Multi-Language(**EN, TR**) Telegram Pharmacy Bot with Python.

Finds Nearest Pharmacies According To Your Current Location or Specific Location, Thanks To Google Services.

For Launch the Bot You have to filling tokens.py requirements like:

_TELEGRAM_BOT_STAGING_TOKEN = ""

_GOOGLE_API_KEY = ""

create a virtual-env for project:
**mkdir venv**

select this folder as a Project Interpreter

install requirements:
**pip install -r requirements.text**

activate it:
**source venv/bin/activate**

then start with command:
**python -m pharmacy_bot_staging.py**

This Telegram Python Bot uses Google's **Maps Geocoding API** and **Places API Web Service** with **Python-Telegram-Bot** SDK.

This bot uses **TimedRotatingFileHandler** for logging user behaviour and information.

Acceptable Commands are :

** /pharmacy
** /eczane
** /pharmacy Austin,Texas
** /eczane Ankara,Turkey
