import customtkinter as ctk
from tkinter import messagebox
from db import get_connection
from mysql.connector import Error
from db import get_connection

# SQL connection
conn = get_connection()     
    cursor = conn.cursor()   

# Fetch admin names and emails from the database
cursor.execute("SELECT Name, Email FROM Admin")
admins = cursor.fetchall()
admin_names = [a[0] for a in admins]
admin_emails = [a[1] for a in admins]

# App window
app = ctk.CTk()
app.title("Add New Game")
app.geometry("500x650")

# Title
ctk.CTkLabel(app, text="Add New Game", font=("Arial", 20, "bold")).pack(pady=10)

# Admin Name dropdown
ctk.CTkLabel(app, text="Admin Name:").pack()
admin_name_var = ctk.StringVar()
admin_name_menu = ctk.CTkOptionMenu(app, variable=admin_name_var, values=admin_names)
admin_name_menu.pack(pady=5)

# Admin Email dropdown
ctk.CTkLabel(app, text="Admin Email:").pack()
admin_email_var = ctk.StringVar()
admin_email_menu = ctk.CTkOptionMenu(app, variable=admin_email_var, values=admin_emails)
admin_email_menu.pack(pady=5)

# Admin Password
ctk.CTkLabel(app, text="Admin Password:").pack()
admin_password_entry = ctk.CTkEntry(app, show="*")
admin_password_entry.pack(pady=5)

# Game Title
ctk.CTkLabel(app, text="Game Title:").pack()
title_entry = ctk.CTkEntry(app)
title_entry.pack(pady=5)

# Genre
ctk.CTkLabel(app, text="Genre:").pack()
genre_entry = ctk.CTkEntry(app)
genre_entry.pack(pady=5)

# Price
ctk.CTkLabel(app, text="Price:").pack()
price_entry = ctk.CTkEntry(app)
price_entry.pack(pady=5)

# Type dropdown
ctk.CTkLabel(app, text="Type:").pack()
type_var = ctk.StringVar(value="Physical")
type_menu = ctk.CTkOptionMenu(app, variable=type_var, values=["Physical", "Digital"])
type_menu.pack(pady=5)

# Stock field in frame (so we can show/hide it easily)
stock_frame = ctk.CTkFrame(app)
ctk.CTkLabel(stock_frame, text="Stock:").pack()
stock_entry = ctk.CTkEntry(stock_frame)
stock_entry.pack()
stock_frame.pack(pady=5)

# Function to toggle stock field
def toggle_stock(value):
    if value == "Physical":
        stock_frame.pack(pady=5)
    else:
        stock_frame.pack_forget()

type_menu.configure(command=toggle_stock)

# Function to add game
def add_game():
    name = admin_name_var.get()
    email = admin_email_var.get()
    password = admin_password_entry.get()
    title = title_entry.get()
    genre = genre_entry.get()
    price = price_entry.get()
    game_type = type_var.get()
    stock = stock_entry.get() if game_type == "Physical" else "∞"

    cursor.execute("SELECT AdminID FROM Admin WHERE Name=%s AND Email=%s AND Password=%s",
                   (name, email, password))
    result = cursor.fetchone()

    if result:
        admin_id = result[0]
        cursor.execute("""
            INSERT INTO Game (Title, Genre, Price, Type, Stock, AdminID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (title, genre, price, game_type, stock, admin_id))
        conn.commit()
        messagebox.showinfo("Success", "Game added successfully!")
        app.destroy()
    else:
        messagebox.showerror("Access Denied", "Invalid admin credentials")

# Submit and Clear buttons
ctk.CTkButton(app, text="Add Game", command=add_game).pack(pady=20)
ctk.CTkButton(app, text="Clear", command=lambda: [
    admin_password_entry.delete(0, 'end'),
    title_entry.delete(0, 'end'),
    genre_entry.delete(0, 'end'),
    price_entry.delete(0, 'end'),
    stock_entry.delete(0, 'end')
]).pack()

# Set stock field visibility on startup
toggle_stock(type_var.get())

app.mainloop()
cursor.close()
conn.close()

