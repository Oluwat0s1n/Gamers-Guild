# edit_game_form.py
import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import sys

# Get Game ID from command line
if len(sys.argv) < 2:
    print("Game ID not provided.")
    sys.exit()

GAME_ID = sys.argv[1]

# SQL connection
conn = mysql.connector.connect(
    host="...",
    user="...",
    password="...",
    database="...",
    port=...
)
cursor = conn.cursor()

# Fetch game data
cursor.execute("SELECT Title, Genre, Price, Type, Stock, AdminID FROM Game WHERE GameID = %s", (GAME_ID,))
game_data = cursor.fetchone()

if not game_data:
    print("Game not found.")
    sys.exit()

# Fetch admin names and emails
cursor.execute("SELECT Name, Email FROM Admin")
admins = cursor.fetchall()
admin_names = [a[0] for a in admins]
admin_emails = [a[1] for a in admins]

# GUI window
app = ctk.CTk()
app.title("Edit Game")
app.geometry("500x650")

ctk.CTkLabel(app, text="Edit Game", font=("Arial", 20, "bold")).pack(pady=10)

# Admin Credentials
ctk.CTkLabel(app, text="Admin Name:").pack()
admin_name_var = ctk.StringVar()
admin_name_menu = ctk.CTkOptionMenu(app, variable=admin_name_var, values=admin_names)
admin_name_menu.pack(pady=5)

ctk.CTkLabel(app, text="Admin Email:").pack()
admin_email_var = ctk.StringVar()
admin_email_menu = ctk.CTkOptionMenu(app, variable=admin_email_var, values=admin_emails)
admin_email_menu.pack(pady=5)

ctk.CTkLabel(app, text="Admin Password:").pack()
admin_password_entry = ctk.CTkEntry(app, show="*")
admin_password_entry.pack(pady=5)

# Game fields
title_var = ctk.StringVar(value=game_data[0])
genre_var = ctk.StringVar(value=game_data[1])
price_var = ctk.StringVar(value=game_data[2])
type_var = ctk.StringVar(value=game_data[3])
stock_var = ctk.StringVar(value=game_data[4])

ctk.CTkLabel(app, text="Game Title:").pack()
title_entry = ctk.CTkEntry(app, textvariable=title_var)
title_entry.pack(pady=5)

ctk.CTkLabel(app, text="Genre:").pack()
genre_entry = ctk.CTkEntry(app, textvariable=genre_var)
genre_entry.pack(pady=5)

ctk.CTkLabel(app, text="Price:").pack()
price_entry = ctk.CTkEntry(app, textvariable=price_var)
price_entry.pack(pady=5)

ctk.CTkLabel(app, text="Type:").pack()
type_menu = ctk.CTkOptionMenu(app, variable=type_var, values=["Physical", "Digital"])
type_menu.pack(pady=5)

stock_frame = ctk.CTkFrame(app)
ctk.CTkLabel(stock_frame, text="Stock:").pack()
stock_entry = ctk.CTkEntry(stock_frame, textvariable=stock_var)
stock_entry.pack()
stock_frame.pack(pady=5)

def toggle_stock(value):
    if value == "Physical":
        stock_frame.pack(pady=5)
    else:
        stock_frame.pack_forget()

type_menu.configure(command=toggle_stock)
toggle_stock(type_var.get())

# Update function
def update_game():
    name = admin_name_var.get()
    email = admin_email_var.get()
    password = admin_password_entry.get()

    title = title_var.get()
    genre = genre_var.get()
    price = price_var.get()
    game_type = type_var.get()
    stock = stock_var.get() if game_type == "Physical" else "∞"

    cursor.execute("SELECT AdminID FROM Admin WHERE Name=%s AND Email=%s AND Password=%s",
                   (name, email, password))
    result = cursor.fetchone()

    if result:
        cursor.execute("""
            UPDATE Game
            SET Title=%s, Genre=%s, Price=%s, Type=%s, Stock=%s
            WHERE GameID=%s
        """, (title, genre, price, game_type, stock, GAME_ID))
        conn.commit()
        messagebox.showinfo("Success", "Game updated successfully!")
        app.destroy()
    else:
        messagebox.showerror("Access Denied", "Invalid admin credentials")

ctk.CTkButton(app, text="Update Game", command=update_game).pack(pady=20)

app.mainloop()
cursor.close()
conn.close()

