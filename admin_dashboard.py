import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import sys
from db import get_connection, image_path     

# SQL Connection
conn = get_connection()
cursor = conn.cursor()

# Correct ICON PATH
ICON_PATH = "C:/Users/file_path/Images/"

def load_icon(filename):
    return ctk.CTkImage(Image.open(os.path.join(ICON_PATH, filename)).resize((24, 24)))

# Open scripts using sys
def open_script(script_name):
    os.execl(sys.executable, sys.executable, script_name)

# App Window
app = ctk.CTk()
app.title("Gamers Guild Admin Dashboard")
app.geometry("1200x750")

# Sidebar
sidebar = ctk.CTkFrame(app, width=180, corner_radius=0, fg_color="#E0D6FA")
sidebar.pack(side="left", fill="y")
ctk.CTkLabel(sidebar, text="", height=20).pack()

# Sidebar Buttons
sidebar_buttons = [
    ("Dashboard", "dashboard.png", "admin_dashboard.py"),
    ("Games", "games.png", "game_management.py"),
    ("Orders", "cart.png", "order_management.py"),
    ("Inventory", "inventory.png", "inventory_sales.py"),
    ("Users", "users.png", "user_management.py")
]

for label, icon, script in sidebar_buttons:
    btn = ctk.CTkButton(sidebar, text=label, image=load_icon(icon), compound="left", width=160,
                        fg_color="transparent", hover_color="#D6C9F8", text_color="#000",
                        command=lambda script=script: open_script(script))
    btn.pack(pady=10)

# Main Frame (Scrollable)
main_frame_container = ctk.CTkFrame(app, fg_color="#F5F5FF")
main_frame_container.pack(side="left", fill="both", expand=True)

main_frame = ctk.CTkScrollableFrame(main_frame_container, fg_color="#F5F5FF")
main_frame.pack(fill="both", expand=True)

# Header
header = ctk.CTkFrame(main_frame, fg_color="#F9F9FF")
header.pack(fill="x")
ctk.CTkLabel(header, text="Admin Dashboard", font=("Helvetica", 18, "bold"), text_color="#000").pack(side="left", padx=20, pady=20)

# Hardcoded Admin Name for now
admin_name = "Admin"
ctk.CTkLabel(header, text=admin_name, font=("Helvetica", 14), text_color="#000").pack(side="right", padx=20)

# Dashboard Cards
def count(query):
    cursor.execute(query)
    return cursor.fetchone()[0]

dashboard_cards_data = [
    ("Total orders", count("SELECT COUNT(*) FROM `Order`"), "cart.png", "order_management.py"),
    ("Active Users", count("SELECT COUNT(*) FROM Customer WHERE ActiveStatus = 'Active'"), "users.png", "user_management.py"),
    ("Monthly Total Sales", "$22,500", "sales.png", "inventory_sales.py"),
    ("Games Listed", count("SELECT COUNT(*) FROM Game WHERE Stock != 'Inactive'"), "games.png", "game_management.py")
]

cards_frame = ctk.CTkFrame(main_frame, fg_color="#F5F5FF")
cards_frame.pack(pady=10, padx=20, fill="x")

for title, value, icon, script in dashboard_cards_data:
    card = ctk.CTkButton(cards_frame, text=f"{title}\n{value}", image=load_icon(icon),
                         compound="top", width=200, height=100, corner_radius=10,
                         fg_color="#F1E8FF", text_color="#000",
                         font=("Helvetica", 12, "bold"),
                         command=lambda script=script: open_script(script))
    card.pack(side="left", padx=10, pady=10)

# Game Management Section
ctk.CTkLabel(main_frame, text="Game Management", font=("Helvetica", 14, "bold"), text_color="#000").pack(anchor="w", padx=30, pady=(10, 0))
ctk.CTkButton(main_frame, text="+ Add Game", command=lambda: open_script("add_game_form.py"),
              width=120, fg_color="#A58CF3", hover_color="#9278DF").pack(anchor="e", padx=30, pady=10)

game_frame = ctk.CTkFrame(main_frame, fg_color="#F5F5FF")
game_frame.pack(padx=30, pady=10, fill="x")

def refresh_games():
    for widget in game_frame.winfo_children():
        widget.destroy()

    headers = ["Game Title", "Genre", "Price", "Type", "Stock", "Actions"]
    header_row = ctk.CTkFrame(game_frame, fg_color="#F9F9FF")
    header_row.pack(fill="x")
    for h in headers:
        ctk.CTkLabel(header_row, text=h, width=140, anchor="w", text_color="#000").pack(side="left", padx=2, pady=4)

    cursor.execute("SELECT GameID, Title, Genre, Price, Type, Stock FROM Game WHERE Stock != 'Inactive'")
    games = cursor.fetchall()
    for game in games:
        gid, title, genre, price, gtype, stock = game
        row = ctk.CTkFrame(game_frame, fg_color="#F1E8FF")
        row.pack(fill="x", pady=2)
        for val in [title, genre, price, gtype, stock]:
            ctk.CTkLabel(row, text=val, width=140, anchor="w", text_color="#000").pack(side="left", padx=2, pady=6)
        act = ctk.CTkFrame(row, fg_color="#F1E8FF")
        act.pack(side="left")
        ctk.CTkButton(act, image=load_icon("edit.png"), text="", width=40, fg_color="#E0D6FA",
                      command=lambda gid=gid: open_script("edit_game_form.py")).pack(side="left", padx=2)
        ctk.CTkButton(act, image=load_icon("delete.png"), text="", width=40, fg_color="#E0D6FA",
                      command=lambda gid=gid, title=title: delete_game(gid, title)).pack(side="left", padx=2)

def delete_game(gid, title):
    if messagebox.askyesno("Delete", f"Are you sure you want to mark '{title}' as Inactive?"):
        cursor.execute("UPDATE Game SET Stock = 'Inactive' WHERE GameID = %s", (gid,))
        conn.commit()
        messagebox.showinfo("Updated", f"'{title}' is now Inactive.")
        refresh_games()

refresh_games()

# Order Management Section
ctk.CTkLabel(main_frame, text="Order Management", font=("Helvetica", 14, "bold"), text_color="#000").pack(anchor="w", padx=30, pady=(20, 0))
search_entry = ctk.CTkEntry(main_frame, placeholder_text="Search", width=160)
search_entry.pack(anchor="e", padx=30)
ctk.CTkButton(main_frame, text="Search", command=lambda: refresh_orders(search_entry.get()), width=80).pack(anchor="e", padx=30, pady=(0, 10))

orders_frame = ctk.CTkFrame(main_frame, fg_color="#F5F5FF")
orders_frame.pack(padx=30, pady=10, fill="x")

def refresh_orders(search_term=None):
    for widget in orders_frame.winfo_children():
        widget.destroy()

    headers = ["Order ID", "Name", "Game(s)", "Total", "Status", "Date", "Actions"]
    header_row = ctk.CTkFrame(orders_frame, fg_color="#F9F9FF")
    header_row.pack(fill="x")
    for h in headers:
        ctk.CTkLabel(header_row, text=h, width=120, anchor="w", text_color="#000").pack(side="left", padx=2, pady=4)

    query = """
        SELECT o.OrderID, CONCAT(c.FirstName, ' ', c.LastName), GROUP_CONCAT(g.Title SEPARATOR ', '),
               FORMAT(SUM(g.Price), 2), o.Status, o.OrderDate
        FROM `Order` o
        JOIN Customer c ON o.CustomerID = c.CustomerID
        JOIN OrderItems oi ON o.OrderID = oi.OrderID
        JOIN Game g ON oi.GameID = g.GameID
    """
    if search_term:
        query += " WHERE c.FirstName LIKE %s OR c.LastName LIKE %s OR o.OrderID = %s "
    query += " GROUP BY o.OrderID LIMIT 3"

    if search_term:
        try:
            cursor.execute(query, (f"%{search_term}%", f"%{search_term}%", search_term))
        except:
            messagebox.showwarning("Invalid Input", "Enter a valid Order ID or Name")
            return
    else:
        cursor.execute(query)

    for row_data in cursor.fetchall():
        row = ctk.CTkFrame(orders_frame, fg_color="#F1E8FF")
        row.pack(fill="x", pady=2)
        for i in range(6):
            ctk.CTkLabel(row, text=row_data[i], width=120, anchor="w", text_color="#000").pack(side="left", padx=2, pady=6)
        act = ctk.CTkFrame(row, fg_color="#F1E8FF")
        act.pack(side="left")
        ctk.CTkButton(act, image=load_icon("done.png"), text="", width=40, fg_color="#E0D6FA").pack(side="left", padx=2)
        ctk.CTkButton(act, image=load_icon("delete.png"), text="", width=40, fg_color="#E0D6FA",
                      command=lambda: messagebox.showwarning("Restricted", "Orders cannot be deleted.")).pack(side="left", padx=2)

refresh_orders()

# Mainloop
app.mainloop()
cursor.close()
conn.close()


