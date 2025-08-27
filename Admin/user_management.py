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
user_account_icon_path = image_path("......png")

def load_icon(filename):
    return ctk.CTkImage(Image.open(os.path.join(ICON_PATH, filename)).resize((22, 22)))

# App window
app = ctk.CTk()
app.title("Gamers Guild - User Management")
app.geometry("1200x750")

# Sidebar
sidebar = ctk.CTkFrame(app, width=180, corner_radius=0, fg_color="#E0D6FA")
sidebar.pack(side="left", fill="y")

ctk.CTkLabel(sidebar, text="", height=20).pack()

sidebar_buttons = [
    ("Dashboard", "dashboard.png", "admin_dashboard.py"),
    ("Game Management", "games.png", "admin/game_management.py"),
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

ctk.CTkLabel(header, text="User Management", font=("Helvetica", 18, "bold"), text_color="#000").pack(side="left", padx=20, pady=20)

# Statistic Box
stat_frame = ctk.CTkFrame(main_frame, fg_color="#F1E8FF")
stat_frame.pack(padx=30, pady=(5, 10), fill="x")

def update_stats():
    cursor.execute("SELECT COUNT(*) FROM Customer WHERE ActiveStatus = 'Active'")
    active = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Customer WHERE ActiveStatus = 'Inactive'")
    inactive = cursor.fetchone()[0]
    active_label.configure(text=f"Active Users: {active}")
    inactive_label.configure(text=f"Inactive Users: {inactive}")

active_label = ctk.CTkLabel(stat_frame, text="", font=("Helvetica", 14), text_color="#000")
active_label.pack(side="left", padx=20, pady=10)

inactive_label = ctk.CTkLabel(stat_frame, text="", font=("Helvetica", 14), text_color="#000")
inactive_label.pack(side="left", padx=20, pady=10)

update_stats()

# Search, Refresh, Filter, Sort Bar
search_frame = ctk.CTkFrame(main_frame, fg_color="#F5F5FF")
search_frame.pack(fill="x", padx=30, pady=(0, 10))

search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search User Name", width=300)
search_entry.pack(side="left", padx=(0, 10))

ctk.CTkButton(search_frame, text="Search", width=80, command=lambda: refresh_users()).pack(side="left", padx=(0, 5))
ctk.CTkButton(search_frame, text="Refresh", width=80, command=lambda: refresh_users()).pack(side="left", padx=(0, 5))
ctk.CTkButton(search_frame, image=load_icon("filter.png"), text="", width=50, command=lambda: filter_users()).pack(side="left", padx=5)
ctk.CTkButton(search_frame, image=load_icon("sort.png"), text="", width=50, command=lambda: sort_users()).pack(side="left", padx=5)
ctk.CTkButton(search_frame, text="+ Add New User", width=130, fg_color="#A58CF3", hover_color="#9278DF",
              command=lambda: open_script("Register_User.py")).pack(side="right", padx=(5, 0))

# Scrollable User Frame
scrollable_frame = ctk.CTkScrollableFrame(main_frame, fg_color="#F5F5FF", width=1000, height=550)
scrollable_frame.pack(padx=30, pady=10, fill="both", expand=True)

def refresh_users():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    headers = ["First Name", "Last Name", "Email", "Status", "Actions"]
    header_row = ctk.CTkFrame(scrollable_frame, fg_color="#F9F9FF")
    header_row.pack(fill="x", padx=5, pady=5)

    for h in headers:
        ctk.CTkLabel(header_row, text=h, width=140, anchor="w", text_color="#000", font=("Helvetica", 12, "bold")).pack(side="left", padx=5)

    query = "SELECT CustomerID, FirstName, LastName, Email, ActiveStatus FROM Customer"
    search = search_entry.get()

    if search:
        query += " WHERE FirstName LIKE %s OR LastName LIKE %s"
        cursor.execute(query, (f"%{search}%", f"%{search}%"))
    else:
        cursor.execute(query)

    users = cursor.fetchall()

    for user in users:
        uid, first, last, email, status = user
        row = ctk.CTkFrame(scrollable_frame, fg_color="#F1E8FF")
        row.pack(fill="x", pady=2, padx=5)

        for val in [first, last, email, status]:
            ctk.CTkLabel(row, text=val, width=140, anchor="w", text_color="#000").pack(side="left", padx=5)

        act = ctk.CTkFrame(row, fg_color="#D9CFFF")
        act.pack(side="left")

        ctk.CTkButton(act, image=load_icon("info.png"), text="", width=40, fg_color="#D9CFFF",
                      command=lambda uid=uid: view_user(uid)).pack(side="left", padx=2)
        ctk.CTkButton(act, image=load_icon("edit.png"), text="", width=40, fg_color="#D9CFFF",
                      command=lambda uid=uid: edit_user(uid)).pack(side="left", padx=2)
        if status == "Active":
            ctk.CTkButton(act, image=load_icon("delete.png"), text="", width=40, fg_color="#D9CFFF",
                          command=lambda uid=uid: deactivate_user(uid)).pack(side="left", padx=2)
        else:
            ctk.CTkButton(act, image=load_icon("refresh.png"), text="", width=40, fg_color="#D9CFFF",
                          command=lambda uid=uid: reactivate_user(uid)).pack(side="left", padx=2)

def view_user(uid):
    cursor.execute("SELECT FirstName, LastName, Email, Address FROM Customer WHERE CustomerID = %s", (uid,))
    user = cursor.fetchone()

    if user:
        first, last, email, address = user
        popup = ctk.CTkToplevel(app)
        popup.title("User Details")
        popup.geometry("400x300")

        ctk.CTkLabel(popup, text=f"First Name: {first}", font=("Helvetica", 14)).pack(pady=10)
        ctk.CTkLabel(popup, text=f"Last Name: {last}", font=("Helvetica", 14)).pack(pady=10)
        ctk.CTkLabel(popup, text=f"Email: {email}", font=("Helvetica", 14)).pack(pady=10)
        ctk.CTkLabel(popup, text=f"Address: {address}", font=("Helvetica", 14)).pack(pady=10)

def edit_user(uid):
    cursor.execute("SELECT FirstName, LastName, Email, Address FROM Customer WHERE CustomerID=%s", (uid,))
    user = cursor.fetchone()

    if user:
        popup = ctk.CTkToplevel(app)
        popup.title("Edit User")
        popup.geometry("400x400")

        fname_entry = ctk.CTkEntry(popup, placeholder_text="First Name", width=300)
        fname_entry.insert(0, user[0])
        fname_entry.pack(pady=10)

        lname_entry = ctk.CTkEntry(popup, placeholder_text="Last Name", width=300)
        lname_entry.insert(0, user[1])
        lname_entry.pack(pady=10)

        email_entry = ctk.CTkEntry(popup, placeholder_text="Email", width=300)
        email_entry.insert(0, user[2])
        email_entry.pack(pady=10)

        address_entry = ctk.CTkEntry(popup, placeholder_text="Address", width=300)
        address_entry.insert(0, user[3])
        address_entry.pack(pady=10)

        def save_changes():
            cursor.execute("""
                UPDATE Customer SET FirstName=%s, LastName=%s, Email=%s, Address=%s WHERE CustomerID=%s
            """, (fname_entry.get(), lname_entry.get(), email_entry.get(), address_entry.get(), uid))
            conn.commit()
            messagebox.showinfo("Success", "User updated successfully!")
            popup.destroy()
            refresh_users()

        ctk.CTkButton(popup, text="Save Changes", command=save_changes).pack(pady=20)

def deactivate_user(uid):
    cursor.execute("UPDATE Customer SET ActiveStatus='Inactive' WHERE CustomerID=%s", (uid,))
    conn.commit()
    messagebox.showinfo("Deactivated", "User is now Inactive.")
    refresh_users()

def reactivate_user(uid):
    cursor.execute("UPDATE Customer SET ActiveStatus='Active' WHERE CustomerID=%s", (uid,))
    conn.commit()
    messagebox.showinfo("Reactivated", "User is now Active.")
    refresh_users()

def filter_users():
    popup = ctk.CTkToplevel(app)
    popup.title("Filter Users")
    popup.geometry("300x150")

    def apply_filter(status):
        cursor.execute("SELECT CustomerID, FirstName, LastName, Email, ActiveStatus FROM Customer WHERE ActiveStatus = %s", (status,))
        users = cursor.fetchall()

        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        headers = ["First Name", "Last Name", "Email", "Status", "Actions"]
        header_row = ctk.CTkFrame(scrollable_frame, fg_color="#F9F9FF")
        header_row.pack(fill="x", padx=5, pady=5)

        for h in headers:
            ctk.CTkLabel(header_row, text=h, width=140, anchor="w", text_color="#000", font=("Helvetica", 12, "bold")).pack(side="left", padx=5)

        for user in users:
            uid, first, last, email, status = user
            row = ctk.CTkFrame(scrollable_frame, fg_color="#F1E8FF")
            row.pack(fill="x", pady=2, padx=5)

            for val in [first, last, email, status]:
                ctk.CTkLabel(row, text=val, width=140, anchor="w", text_color="#000").pack(side="left", padx=5)

            act = ctk.CTkFrame(row, fg_color="#D9CFFF")
            act.pack(side="left")

            ctk.CTkButton(act, image=load_icon("info.png"), text="", width=40, fg_color="#D9CFFF",
                          command=lambda uid=uid: view_user(uid)).pack(side="left", padx=2)
            ctk.CTkButton(act, image=load_icon("edit.png"), text="", width=40, fg_color="#D9CFFF",
                          command=lambda uid=uid: edit_user(uid)).pack(side="left", padx=2)
            if status == "Active":
                ctk.CTkButton(act, image=load_icon("delete.png"), text="", width=40, fg_color="#D9CFFF",
                              command=lambda uid=uid: deactivate_user(uid)).pack(side="left", padx=2)
            else:
                ctk.CTkButton(act, image=load_icon("refresh.png"), text="", width=40, fg_color="#D9CFFF",
                              command=lambda uid=uid: reactivate_user(uid)).pack(side="left", padx=2)

        popup.destroy()

    ctk.CTkButton(popup, text="Active Users", command=lambda: apply_filter("Active")).pack(pady=10)
    ctk.CTkButton(popup, text="Inactive Users", command=lambda: apply_filter("Inactive")).pack(pady=10)

def sort_users():
    popup = ctk.CTkToplevel(app)
    popup.title("Sort Users")
    popup.geometry("300x150")

    def sort_direction(order):
        cursor.execute(f"SELECT CustomerID, FirstName, LastName, Email, ActiveStatus FROM Customer ORDER BY FirstName {order}")
        users = cursor.fetchall()

        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        headers = ["First Name", "Last Name", "Email", "Status", "Actions"]
        header_row = ctk.CTkFrame(scrollable_frame, fg_color="#F9F9FF")
        header_row.pack(fill="x", padx=5, pady=5)

        for h in headers:
            ctk.CTkLabel(header_row, text=h, width=140, anchor="w", text_color="#000", font=("Helvetica", 12, "bold")).pack(side="left", padx=5)

        for user in users:
            uid, first, last, email, status = user
            row = ctk.CTkFrame(scrollable_frame, fg_color="#F1E8FF")
            row.pack(fill="x", pady=2, padx=5)

            for val in [first, last, email, status]:
                ctk.CTkLabel(row, text=val, width=140, anchor="w", text_color="#000").pack(side="left", padx=5)

            act = ctk.CTkFrame(row, fg_color="#D9CFFF")
            act.pack(side="left")

            ctk.CTkButton(act, image=load_icon("info.png"), text="", width=40, fg_color="#D9CFFF",
                          command=lambda uid=uid: view_user(uid)).pack(side="left", padx=2)
            ctk.CTkButton(act, image=load_icon("edit.png"), text="", width=40, fg_color="#D9CFFF",
                          command=lambda uid=uid: edit_user(uid)).pack(side="left", padx=2)
            if status == "Active":
                ctk.CTkButton(act, image=load_icon("delete.png"), text="", width=40, fg_color="#D9CFFF",
                              command=lambda uid=uid: deactivate_user(uid)).pack(side="left", padx=2)
            else:
                ctk.CTkButton(act, image=load_icon("refresh.png"), text="", width=40, fg_color="#D9CFFF",
                              command=lambda uid=uid: reactivate_user(uid)).pack(side="left", padx=2)

        popup.destroy()

    ctk.CTkButton(popup, text="Sort A-Z", command=lambda: sort_direction("ASC")).pack(pady=10)
    ctk.CTkButton(popup, text="Sort Z-A", command=lambda: sort_direction("DESC")).pack(pady=10)

refresh_users()

# Main loop
app.mainloop()
cursor.close()
conn.close()

