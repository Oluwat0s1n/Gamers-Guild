# edit_game_form.py
import customtkinter as ctk
from tkinter import messagebox
import sys
from decimal import Decimal, InvalidOperation

from db import get_connection  

# --- read Game ID from admin_dashboard.py argument ---
if len(sys.argv) < 2:
    print("Game ID not provided.")
    sys.exit(1)

GAME_ID = sys.argv[1]

# --- DB connection ---
conn = get_connection()
cursor = conn.cursor()

# --- fetch current game + admins ---
cursor.execute(
    "SELECT Title, Genre, Price, Type, Stock FROM Game WHERE GameID = %s",
    (GAME_ID,),
)
game = cursor.fetchone()
if not game:
    print("Game not found.")
    sys.exit(1)

title0, genre0, price0, type0, stock0 = game

cursor.execute("SELECT Name, Email FROM Admin")
admins = cursor.fetchall()
admin_names  = [a[0] for a in admins]
admin_emails = [a[1] for a in admins]

# --- UI ---
app = ctk.CTk()
app.title("Edit Game")
app.geometry("500x650")

ctk.CTkLabel(app, text="Edit Game", font=("Arial", 20, "bold")).pack(pady=10)

# Admin creds
ctk.CTkLabel(app, text="Admin Name:").pack()
admin_name_var = ctk.StringVar(value=admin_names[0] if admin_names else "")
ctk.CTkOptionMenu(app, variable=admin_name_var, values=admin_names).pack(pady=5)

ctk.CTkLabel(app, text="Admin Email:").pack()
admin_email_var = ctk.StringVar(value=admin_emails[0] if admin_emails else "")
ctk.CTkOptionMenu(app, variable=admin_email_var, values=admin_emails).pack(pady=5)

ctk.CTkLabel(app, text="Admin Password:").pack()
admin_password_entry = ctk.CTkEntry(app, show="*")
admin_password_entry.pack(pady=5)

# Game fields
title_var = ctk.StringVar(value=str(title0))
genre_var = ctk.StringVar(value=str(genre0) if genre0 else "")
price_var = ctk.StringVar(value=str(price0))
type_var  = ctk.StringVar(value=str(type0))
stock_var = ctk.StringVar(value=str(stock0))

ctk.CTkLabel(app, text="Game Title:").pack()
ctk.CTkEntry(app, textvariable=title_var).pack(pady=5)

ctk.CTkLabel(app, text="Genre:").pack()
ctk.CTkEntry(app, textvariable=genre_var).pack(pady=5)

ctk.CTkLabel(app, text="Price:").pack()
ctk.CTkEntry(app, textvariable=price_var).pack(pady=5)

ctk.CTkLabel(app, text="Type:").pack()
type_menu = ctk.CTkOptionMenu(app, variable=type_var, values=["Physical", "Digital"])
type_menu.pack(pady=5)

stock_frame = ctk.CTkFrame(app)
ctk.CTkLabel(stock_frame, text="Stock:").pack()
ctk.CTkEntry(stock_frame, textvariable=stock_var).pack()
stock_frame.pack(pady=5)

def toggle_stock(value):
    # show stock box only for Physical items
    (stock_frame.pack if value == "Physical" else stock_frame.pack_forget)(pady=5)

type_menu.configure(command=toggle_stock)
toggle_stock(type_var.get())

# --- actions ---
def update_game():
    # admin check
    name  = admin_name_var.get().strip()
    email = admin_email_var.get().strip()
    pwd   = admin_password_entry.get()

    # game fields
    title    = title_var.get().strip()
    genre    = genre_var.get().strip()
    gtype    = type_var.get().strip()
    try:
        price = Decimal(price_var.get().strip())
    except InvalidOperation:
        messagebox.showerror("Invalid price", "Please enter a valid number for Price.")
        return

    stock = stock_var.get().strip() if gtype == "Physical" else "∞"

    if not title:
        messagebox.showerror("Missing title", "Game title is required.")
        return

    # verify admin (plain-text per your current schema)
    cursor.execute(
        "SELECT 1 FROM Admin WHERE Name=%s AND Email=%s AND Password=%s",
        (name, email, pwd),
    )
    if not cursor.fetchone():
        messagebox.showerror("Access Denied", "Invalid admin credentials.")
        return

    # update
    try:
        cursor.execute(
            """
            UPDATE Game
               SET Title=%s, Genre=%s, Price=%s, Type=%s, Stock=%s
             WHERE GameID=%s
            """,
            (title, genre, str(price), gtype, stock, GAME_ID),
        )
        conn.commit()
        messagebox.showinfo("Success", "Game updated successfully!")
        app.destroy()
    except Exception as e:
        messagebox.showerror("Database Error", f"{e}")

ctk.CTkButton(app, text="Update Game", command=update_game).pack(pady=20)

def on_close():
    try:
        cursor.close()
    except:
        pass
    try:
        conn.close()
    except:
        pass
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_close)
app.mainloop()
on_close()



