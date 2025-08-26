import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import mysql.connector
import os
import sys

# SQL Connection
conn = mysql.connector.connect(
    host="...",
    user="...",
    password="...",
    database="...",
    port=...
)
cursor = conn.cursor()

# ICON PATH
ICON_PATH = "C:/Users/darap/PycharmProjects/darap1s_project/BIS 698_Group 5/Images/"

def load_icon(filename):
    return ctk.CTkImage(Image.open(os.path.join(ICON_PATH, filename)).resize((22, 22)))

# Open scripts with sys executable
def open_script(script_name):
    os.execl(sys.executable, sys.executable, script_name)

# App window
app = ctk.CTk()
app.title("Gamers Guild - Order Management")
app.geometry("1200x750")

# Sidebar
sidebar = ctk.CTkFrame(app, width=180, corner_radius=0, fg_color="#E0D6FA")
sidebar.pack(side="left", fill="y")

ctk.CTkLabel(sidebar, text="", height=20).pack()

sidebar_buttons = [
    ("Dashboard", "dashboard.png", "admin_dashboard.py"),
    ("Game Management", "games.png", "game_management.py"),
    ("Orders", "cart.png", "order_management.py"),
    ("Inventory & Sales", "inventory.png", "inventory_sales.py"),
    ("User Management", "users.png", "user_management.py")
]

for label, icon, script in sidebar_buttons:
    btn = ctk.CTkButton(sidebar, text=label, image=load_icon(icon), compound="left", width=160,
                        fg_color="transparent", hover_color="#D6C9F8", text_color="#000",
                        command=lambda script=script: open_script(script))
    btn.pack(pady=10)

# Main Frame
main_frame = ctk.CTkFrame(app, fg_color="#F5F5FF")
main_frame.pack(side="left", fill="both", expand=True)

# Header
header = ctk.CTkFrame(main_frame, fg_color="#F9F9FF")
header.pack(fill="x")

ctk.CTkLabel(header, text="Order Management", font=("Helvetica", 18, "bold"), text_color="#000").pack(side="left", padx=20, pady=20)

# Search, Refresh
search_frame = ctk.CTkFrame(main_frame, fg_color="#F5F5FF")
search_frame.pack(fill="x", padx=30, pady=(0, 10))

search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search Order ID or Customer Name", width=300)
search_entry.pack(side="left", padx=(0, 10))

ctk.CTkButton(search_frame, text="Search", width=80, command=lambda: refresh_orders()).pack(side="left", padx=(0, 5))
ctk.CTkButton(search_frame, text="Refresh", width=80, command=lambda: refresh_orders()).pack(side="left", padx=(0, 5))

# Scrollable Orders Frame
scrollable_frame = ctk.CTkScrollableFrame(main_frame, fg_color="#F5F5FF", width=1000, height=550)
scrollable_frame.pack(padx=30, pady=10, fill="both", expand=True)

def refresh_orders():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    headers = ["Order ID", "Customer", "Total Amount", "Status", "Date", "Actions"]
    header_row = ctk.CTkFrame(scrollable_frame, fg_color="#F9F9FF")
    header_row.pack(fill="x", padx=5, pady=5)

    for h in headers:
        ctk.CTkLabel(header_row, text=h, width=140, anchor="w", text_color="#000", font=("Helvetica", 12, "bold")).pack(side="left", padx=5)

    search = search_entry.get()
    query = """
        SELECT o.OrderID, CONCAT(c.FirstName, ' ', c.LastName), FORMAT(SUM(g.Price),2), o.Status, o.OrderDate
        FROM `Order` o
        JOIN Customer c ON o.CustomerID = c.CustomerID
        JOIN OrderItems oi ON o.OrderID = oi.OrderID
        JOIN Game g ON oi.GameID = g.GameID
    """
    params = ()
    if search:
        query += " WHERE c.FirstName LIKE %s OR c.LastName LIKE %s OR o.OrderID = %s"
        params = (f"%{search}%", f"%{search}%", search)

    query += " GROUP BY o.OrderID ORDER BY o.OrderDate DESC"

    cursor.execute(query, params)
    orders = cursor.fetchall()

    for order in orders:
        oid, customer, total, status, date = order
        row = ctk.CTkFrame(scrollable_frame, fg_color="#F1E8FF")
        row.pack(fill="x", pady=2, padx=5)

        for val in [oid, customer, f"${total}", status, str(date)]:
            ctk.CTkLabel(row, text=val, width=140, anchor="w", text_color="#000").pack(side="left", padx=5)

        act = ctk.CTkFrame(row, fg_color="#D9CFFF")
        act.pack(side="left")

        ctk.CTkButton(act, image=load_icon("info.png"), text="", width=40, fg_color="#D9CFFF",
                      command=lambda oid=oid: view_order_details(oid)).pack(side="left", padx=2)

def view_order_details(order_id):
    cursor.execute("""
        SELECT o.OrderID, CONCAT(c.FirstName, ' ', c.LastName), GROUP_CONCAT(g.Title SEPARATOR ', '), FORMAT(SUM(g.Price),2), o.Status, o.OrderDate
        FROM `Order` o
        JOIN Customer c ON o.CustomerID = c.CustomerID
        JOIN OrderItems oi ON o.OrderID = oi.OrderID
        JOIN Game g ON oi.GameID = g.GameID
        WHERE o.OrderID = %s
        GROUP BY o.OrderID
    """, (order_id,))
    order = cursor.fetchone()

    if order:
        oid, customer, games, total, status, date = order
        popup = ctk.CTkToplevel(app)
        popup.title("Order Details")
        popup.geometry("450x400")

        ctk.CTkLabel(popup, text=f"Order ID: {oid}", font=("Helvetica", 14)).pack(pady=10)
        ctk.CTkLabel(popup, text=f"Customer: {customer}", font=("Helvetica", 14)).pack(pady=10)
        ctk.CTkLabel(popup, text=f"Games: {games}", font=("Helvetica", 14), wraplength=400).pack(pady=10)
        ctk.CTkLabel(popup, text=f"Total Amount: ${total}", font=("Helvetica", 14)).pack(pady=10)
        ctk.CTkLabel(popup, text=f"Status: {status}", font=("Helvetica", 14)).pack(pady=10)
        ctk.CTkLabel(popup, text=f"Date: {date}", font=("Helvetica", 14)).pack(pady=10)

refresh_orders()

# Main loop
app.mainloop()
cursor.close()
conn.close()

