# Gamers Guild

A simple desktop **Game Store** built with **Python (CustomTkinter)** and **MySQL**.  
Users can sign in, browse games, add to cart, and manage their library.  
Admins can manage inventory, orders, and users — the whole shop floor.

---

## What it does

**For users**
- Sign in / register
- Browse & search games
- Add to cart, checkout
- View library & update account

**For admins**
- Add / edit / delete games
- Manage orders & inventory
- View least-purchasing customers
- Basic user management

---

## Tech

Python · CustomTkinter · Pillow · MySQL · `mysql-connector-python` · `python-dotenv`

---

## File guide (main scripts)

- `LoginUser.py`, `RegisterUser.py`, `Home.py`
- `Games.py`, `UserCart.py`, `cart.py`, `library.py`, `UserAccount.py`
- `admin_dashboard.py`, `UserDashboard.py`
- `game_management.py`, `order_management.py`, `inventory_sales.py`, `user_management.py`
- `add_game_form.py`, `edit_game_form.py`, `forgot_password.py`
- `db.py` — small helper that reads DB settings from `.env` and returns a MySQL connection

---

## Run it locally (Mac)

1. **Python 3.11+** installed.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate

## Database scripts
Schema lives in [`sql/GamersGuild_DB.sql`](sql/GamersGuild_DB.sql).
Run (MySQL):
```bash
mysql -u <user> -p < sql/GamersGuild_DB.sql

