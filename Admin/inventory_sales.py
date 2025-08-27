import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image
import os
import sys
import csv
from fpdf import FPDF
import datetime
from mysql.connector import Error
from core.db import get_connection

# SQL Connection
conn = get_connection()
cursor = conn.cursor()

# Correct ICON PATH
ICON_PATH = "C:/Users/file_path/Images/"

def load_icon(filename):
    return ctk.CTkImage(Image.open(os.path.join(ICON_PATH, filename)).resize((22, 22)))

# App window
app = ctk.CTk()
app.title("Gamers Guild - Inventory & Sales Management")
app.geometry("1200x750")

# Sidebar
sidebar = ctk.CTkFrame(app, width=180, corner_radius=0, fg_color="#E0D6FA")
sidebar.pack(side="left", fill="y")
ctk.CTkLabel(sidebar, text="", height=20).pack()

sidebar_buttons = [
    ("Dashboard", "dashboard.png", "admin_dashboard.py"),
    ("Games", "games.png", "admin/game_management.py"),
    ("Users", "users.png", "admin/user_management.py")
]

def open_script(script_name):
    os.system(f"{sys.executable} {script_name}")
    app.destroy()

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
ctk.CTkLabel(header, text="Inventory & Sales Management", font=("Helvetica", 20, "bold"), text_color="#000").pack(side="left", padx=20, pady=20)

# Top Statistics Frame
stats_frame = ctk.CTkFrame(main_frame, fg_color="#F5F5FF")
stats_frame.pack(fill="x", padx=20, pady=10)

def get_count(query):
    cursor.execute(query)
    return cursor.fetchone()[0]

total_orders = get_count("SELECT COUNT(*) FROM `Order`")
top_game_query = "SELECT g.Title, COUNT(oi.GameID) as SoldCount FROM OrderItems oi JOIN Game g ON oi.GameID = g.GameID GROUP BY oi.GameID ORDER BY SoldCount DESC LIMIT 1"
cursor.execute(top_game_query)
top_game = cursor.fetchone()
top_game_name = top_game[0] if top_game else "No Sales Yet"
low_stock = get_count("SELECT COUNT(*) FROM Game WHERE Stock <= 5 AND Stock != 'Inactive'")
total_games = get_count("SELECT COUNT(*) FROM Game")

stats = [
    ("Total Orders", total_orders, "cart.png"),
    ("Top Selling Game", top_game_name, "games.png"),
    ("Low Stock Games", low_stock, "inventory.png"),
    ("Total Games", total_games, "dashboard.png")
]

for title, value, icon in stats:
    card = ctk.CTkFrame(stats_frame, fg_color="#E0D6FA", width=200, height=100, corner_radius=10)
    card.pack(side="left", padx=10, pady=10)
    ctk.CTkLabel(card, text=title, font=("Helvetica", 13, "bold"), text_color="#493287").pack(pady=5)
    ctk.CTkLabel(card, text=value, font=("Helvetica", 15, "bold"), text_color="#171717").pack()

# Inventory Section
inventory_header = ctk.CTkLabel(main_frame, text="Inventory Overview", font=("Helvetica", 16, "bold"), text_color="#000")
inventory_header.pack(anchor="w", padx=30, pady=(10, 0))

# Inventory Action Buttons
inventory_actions = ctk.CTkFrame(main_frame, fg_color="#F5F5FF")
inventory_actions.pack(fill="x", padx=30, pady=5)

ctk.CTkButton(inventory_actions, text="Refresh", width=80, command=lambda: refresh_inventory()).pack(side="left", padx=5)
ctk.CTkButton(inventory_actions, text="Export CSV", width=100, command=lambda: export_csv()).pack(side="left", padx=5)

# Inventory Table
inventory_table = ctk.CTkScrollableFrame(main_frame, fg_color="#F5F5FF", width=1100, height=250)
inventory_table.pack(padx=30, pady=10)

# Sales Section
sales_header = ctk.CTkLabel(main_frame, text="Sales Overview", font=("Helvetica", 16, "bold"), text_color="#000")
sales_header.pack(anchor="w", padx=30, pady=(20, 0))

# Sales Action Buttons
sales_actions = ctk.CTkFrame(main_frame, fg_color="#F5F5FF")
sales_actions.pack(fill="x", padx=30, pady=5)

ctk.CTkButton(sales_actions, text="Export Sales PDF", width=150, command=lambda: export_sales_pdf()).pack(side="left", padx=5)

# Sales Table
sales_table = ctk.CTkScrollableFrame(main_frame, fg_color="#F5F5FF", width=1100, height=250)
sales_table.pack(padx=30, pady=10)

def refresh_inventory():
    for widget in inventory_table.winfo_children():
        widget.destroy()

    headers = ["Title", "Genre", "Price", "Type", "Stock"]
    header_row = ctk.CTkFrame(inventory_table, fg_color="#D9CFFF")
    header_row.pack(fill="x", padx=5, pady=5)
    for h in headers:
        ctk.CTkLabel(header_row, text=h, width=140, anchor="w", text_color="#000").pack(side="left", padx=5)

    query = "SELECT Title, Genre, Price, Type, Stock FROM Game ORDER BY Stock ASC"
    cursor.execute(query)
    games = cursor.fetchall()

    for game in games:
        row = ctk.CTkFrame(inventory_table, fg_color="#F1E8FF")
        row.pack(fill="x", pady=2, padx=5)
        for val in game:
            ctk.CTkLabel(row, text=str(val), width=140, anchor="w", text_color="#000").pack(side="left", padx=5)

def export_csv():
    file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV Files", '*.csv')])
    if not file_path:
        return

    cursor.execute("SELECT Title, Genre, Price, Type, Stock FROM Game ORDER BY Stock ASC")
    games = cursor.fetchall()

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Genre", "Price", "Type", "Stock"])
        for game in games:
            writer.writerow(game)

    messagebox.showinfo("Exported", "Inventory exported successfully!")

def refresh_sales():
    for widget in sales_table.winfo_children():
        widget.destroy()

    headers = ["Game Title", "Times Sold", "Total Revenue"]
    header_row = ctk.CTkFrame(sales_table, fg_color="#D9CFFF")
    header_row.pack(fill="x", padx=5, pady=5)
    for h in headers:
        ctk.CTkLabel(header_row, text=h, width=140, anchor="w", text_color="#000").pack(side="left", padx=5)

    query = """
        SELECT g.Title, COUNT(oi.GameID) as SoldCount, SUM(g.Price) as Revenue
        FROM OrderItems oi
        JOIN Game g ON oi.GameID = g.GameID
        GROUP BY oi.GameID
        ORDER BY SoldCount DESC
    """
    cursor.execute(query)
    sales = cursor.fetchall()

    for sale in sales:
        row = ctk.CTkFrame(sales_table, fg_color="#F1E8FF")
        row.pack(fill="x", pady=2, padx=5)
        for val in sale:
            ctk.CTkLabel(row, text=str(val), width=140, anchor="w", text_color="#000").pack(side="left", padx=5)

def export_sales_pdf():
    now = datetime.datetime.now()
    filename = f"Sales_Report_{now.strftime('%B_%Y')}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Gamers Guild - Sales Report", ln=True, align='C')
    pdf.cell(0, 10, f"Month: {now.strftime('%B %Y')}", ln=True, align='C')
    pdf.ln(10)

    headers = ["Game Title", "Times Sold", "Revenue"]
    for header in headers:
        pdf.cell(60, 10, header, 1, 0, 'C')
    pdf.ln()

    cursor.execute("""
        SELECT g.Title, COUNT(oi.GameID) as SoldCount, SUM(g.Price) as Revenue
        FROM OrderItems oi
        JOIN Game g ON oi.GameID = g.GameID
        GROUP BY oi.GameID
        ORDER BY SoldCount DESC
    """)
    sales = cursor.fetchall()

    for sale in sales:
        for val in sale:
            pdf.cell(60, 10, str(val), 1, 0, 'C')
        pdf.ln()

    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], initialfile=filename)
    if file_path:
        pdf.output(file_path)
        messagebox.showinfo("Exported", "Sales report exported successfully!")

# Initial loading
refresh_inventory()
refresh_sales()

# Main loop
app.mainloop()
cursor.close()
conn.close()

