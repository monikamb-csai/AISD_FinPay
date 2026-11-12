# FinPay – Digital Payment System (Student Demo)

FinPay is a small Flask web application demonstrating account registration, login,
simulated money transfers, balance updates, and transaction history.

## Architecture
- Presentation layer: HTML templates and CSS in `templates/` and `static/`
- Application/controller layer: routes in `app.py`
- Business logic layer: transfer rules in `services.py`
- Data access layer: queries in `repository.py`
- Database layer: SQLite schema and connection setup in `database.py`

## Run on Windows
1. Install Python 3.
2. Open PowerShell in this folder.
3. Create a virtual environment: `py -m venv .venv`
4. Activate it: `.venv\Scripts\Activate.ps1`
5. Install dependencies: `pip install -r requirements.txt`
6. Start the app: `python app.py`
7. Open `http://127.0.0.1:5000`

Register two demo accounts using different email addresses, then transfer between them.

## Important
This is an educational simulation only. It does not connect to banks, payment gateways,
UPI, cards, or real funds. Do not use real passwords or sensitive financial information.
Before any public deployment, replace the demo secret key, disable debug mode, add CSRF
protection, validation, tests, and production security controls.
