import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import sys
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
app.title("Gamers Guild - Game Management")
app.geometry("1200x750")

# Sidebar
sidebar = ctk.CTkFrame(app, width=180, corner_radius=0, fg_color="#E0D6FA")
sidebar.pack(side="left", fill="y")

ctk.CTkLabel(sidebar, text="", height=20).pack()

sidebar_buttons = [
    ("Dashboard", "dashboard.png", "admin_dashboard.py"),
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

ctk.CTkLabel(header, text="Game Management", font=("Helvetica", 18, "bold"), text_color="#000").pack(side="left", padx=20, pady=20)

# Search, Refresh, Filter, Sort Bar
search_frame = ctk.CTkFrame(main_frame, fg_color="#F5F5FF")
search_frame.pack(fill="x", padx=30, pady=(0, 10))

search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search Game Title", width=300)
search_entry.pack(side="left", padx=(0, 10))

ctk.CTkButton(search_frame, text="Search", width=80, command=lambda: search_games()).pack(side="left", padx=(0, 10))
ctk.CTkButton(search_frame, text="Refresh", width=80, command=lambda: refresh_games()).pack(side="left", padx=(0, 10))
ctk.CTkButton(search_frame, image=load_icon("filter.png"), text="", width=50, command=lambda: filter_games()).pack(side="left", padx=5)
ctk.CTkButton(search_frame, image=load_icon("sort.png"), text="", width=50, command=lambda: sort_games()).pack(side="left", padx=5)
ctk.CTkButton(search_frame, text="+ Add Game", width=120, fg_color="#A58CF3", hover_color="#9278DF",
              command=lambda: os.system(f"{sys.executable} admin/add_game_form.py")).pack(side="right", padx=(0, 5))

# Scrollable Game Frame
scrollable_frame = ctk.CTkScrollableFrame(main_frame, fg_color="#F5F5FF", width=1000, height=550)
scrollable_frame.pack(padx=30, pady=10, fill="both", expand=True)

def refresh_games():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    headers = ["Title", "Genre", "Price", "Type", "Stock", "Actions"]
    header_row = ctk.CTkFrame(scrollable_frame, fg_color="#F9F9FF")
    header_row.pack(fill="x", padx=5, pady=5)

    for h in headers:
        ctk.CTkLabel(header_row, text=h, width=140, anchor="w", text_color="#000", font=("Helvetica", 12, "bold")).pack(side="left", padx=5)

    cursor.execute("SELECT GameID, Title, Genre, Price, Type, Stock FROM Game WHERE Stock != 'Inactive'")
    games = cursor.fetchall()

    for game in games:
        gid, title, genre, price, gtype, stock = game
        row = ctk.CTkFrame(scrollable_frame, fg_color="#F1E8FF")
        row.pack(fill="x", pady=2, padx=5)

        for val in [title, genre, f"${price}", gtype, stock]:
            ctk.CTkLabel(row, text=val, width=140, anchor="w", text_color="#000").pack(side="left", padx=5)

        act = ctk.CTkFrame(row, fg_color="#F1E8FF")
        act.pack(side="left")

        ctk.CTkButton(act, image=load_icon("edit.png"), text="", width=40, fg_color="#E0D6FA",
                      command=lambda gid=gid: edit_game(gid)).pack(side="left", padx=2)
        ctk.CTkButton(act, image=load_icon("delete.png"), text="", width=40, fg_color="#E0D6FA",
                      command=lambda gid=gid, title=title: deactivate_game(gid, title)).pack(side="left", padx=2)

def deactivate_game(gid, title):
    if messagebox.askyesno("Confirm", f"Mark '{title}' as Inactive?"):
        cursor.execute("UPDATE Game SET Stock = 'Inactive' WHERE GameID = %s", (gid,))
        conn.commit()
        messagebox.showinfo("Success", f"'{title}' is now Inactive.")
        refresh_games()

def edit_game(gid):
    os.system(f"{sys.executable} admin/edit_game_form.py {gid}")
    app.destroy()

def filter_games():
    popup = ctk.CTkToplevel(app)
    popup.title("Filter Games")
    popup.geometry("300x200")

    def apply_filter(selected_type):
        cursor.execute("SELECT GameID, Title, Genre, Price, Type, Stock FROM Game WHERE Type = %s AND Stock != 'Inactive'", (selected_type,))
        games = cursor.fetchall()
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        headers = ["Title", "Genre", "Price", "Type", "Stock", "Actions"]
        header_row = ctk.CTkFrame(scrollable_frame, fg_color="#F9F9FF")
        header_row.pack(fill="x", padx=5, pady=5)

        for h in headers:
            ctk.CTkLabel(header_row, text=h, width=140, anchor="w", text_color="#000", font=("Helvetica", 12, "bold")).pack(side="left", padx=5)

        for game in games:
            gid, title, genre, price, gtype, stock = game
            row = ctk.CTkFrame(scrollable_frame, fg_color="#F1E8FF")
            row.pack(fill="x", pady=2, padx=5)

            for val in [title, genre, f"${price}", gtype, stock]:
                ctk.CTkLabel(row, text=val, width=140, anchor="w", text_color="#000").pack(side="left", padx=5)

            act = ctk.CTkFrame(row, fg_color="#F1E8FF")
            act.pack(side="left")

            ctk.CTkButton(act, image=load_icon("edit.png"), text="", width=40, fg_color="#E0D6FA",
                          command=lambda gid=gid: edit_game(gid)).pack(side="left", padx=2)
            ctk.CTkButton(act, image=load_icon("delete.png"), text="", width=40, fg_color="#E0D6FA",
                          command=lambda gid=gid, title=title: deactivate_game(gid, title)).pack(side="left", padx=2)

        popup.destroy()

    ctk.CTkButton(popup, text="Filter Physical", command=lambda: apply_filter("Physical")).pack(pady=20)
    ctk.CTkButton(popup, text="Filter Digital", command=lambda: apply_filter("Digital")).pack(pady=20)

def sort_games():
    popup = ctk.CTkToplevel(app)
    popup.title("Sort Games")
    popup.geometry("300x150")

    def apply_sort(order):
        cursor.execute(f"SELECT GameID, Title, Genre, Price, Type, Stock FROM Game WHERE Stock != 'Inactive' ORDER BY Title {order}")
        games = cursor.fetchall()
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        headers = ["Title", "Genre", "Price", "Type", "Stock", "Actions"]
        header_row = ctk.CTkFrame(scrollable_frame, fg_color="#F9F9FF")
        header_row.pack(fill="x", padx=5, pady=5)

        for h in headers:
            ctk.CTkLabel(header_row, text=h, width=140, anchor="w", text_color="#000", font=("Helvetica", 12, "bold")).pack(side="left", padx=5)

        for game in games:
            gid, title, genre, price, gtype, stock = game
            row = ctk.CTkFrame(scrollable_frame, fg_color="#F1E8FF")
            row.pack(fill="x", pady=2, padx=5)

            for val in [title, genre, f"${price}", gtype, stock]:
                ctk.CTkLabel(row, text=val, width=140, anchor="w", text_color="#000").pack(side="left", padx=5)

            act = ctk.CTkFrame(row, fg_color="#F1E8FF")
            act.pack(side="left")

            ctk.CTkButton(act, image=load_icon("edit.png"), text="", width=40, fg_color="#E0D6FA",
                          command=lambda gid=gid: edit_game(gid)).pack(side="left", padx=2)
            ctk.CTkButton(act, image=load_icon("delete.png"), text="", width=40, fg_color="#E0D6FA",
                          command=lambda gid=gid, title=title: deactivate_game(gid, title)).pack(side="left", padx=2)

        popup.destroy()

    ctk.CTkButton(popup, text="Sort A-Z", command=lambda: apply_sort("ASC")).pack(pady=10)
    ctk.CTkButton(popup, text="Sort Z-A", command=lambda: apply_sort("DESC")).pack(pady=10)

def search_games():
    query = search_entry.get()
    cursor.execute("SELECT GameID, Title, Genre, Price, Type, Stock FROM Game WHERE Title LIKE %s AND Stock != 'Inactive'", (f"%{query}%",))
    games = cursor.fetchall()

    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    headers = ["Title", "Genre", "Price", "Type", "Stock", "Actions"]
    header_row = ctk.CTkFrame(scrollable_frame, fg_color="#F9F9FF")
    header_row.pack(fill="x", padx=5, pady=5)

    for h in headers:
        ctk.CTkLabel(header_row, text=h, width=140, anchor="w", text_color="#000", font=("Helvetica", 12, "bold")).pack(side="left", padx=5)

    for game in games:
        gid, title, genre, price, gtype, stock = game
        row = ctk.CTkFrame(scrollable_frame, fg_color="#F1E8FF")
        row.pack(fill="x", pady=2, padx=5)

        for val in [title, genre, f"${price}", gtype, stock]:
            ctk.CTkLabel(row, text=val, width=140, anchor="w", text_color="#000").pack(side="left", padx=5)

        act = ctk.CTkFrame(row, fg_color="#F1E8FF")
        act.pack(side="left")

        ctk.CTkButton(act, image=load_icon("edit.png"), text="", width=40, fg_color="#E0D6FA",
                      command=lambda gid=gid: edit_game(gid)).pack(side="left", padx=2)
        ctk.CTkButton(act, image=load_icon("delete.png"), text="", width=40, fg_color="#E0D6FA",
                      command=lambda gid=gid, title=title: deactivate_game(gid, title)).pack(side="left", padx=2)

refresh_games()

# Main loop
app.mainloop()
cursor.close()
conn.close()

