import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import sys
from db import get_connection, image_path     


from db import get_connection, image_path

# ---------- DB ----------
conn = get_connection()
cursor = conn.cursor()

# ---------- helpers ----------
def load_icon(filename: str, size=(24, 24)):
    """Load an icon from the image folder defined in .env (via db.image_path)."""
    path = image_path(filename)
    return ctk.CTkImage(Image.open(path).resize(size))

def open_script(script_name: str, *args):
    """Open another script in a new Python process (keeps this window open)."""
    subprocess.Popen([sys.executable, script_name, *[str(a) for a in args]])

def count(sql: str, params=()):
    """Return first column of first row for quick counters."""
    try:
        cursor.execute(sql, params)
        row = cursor.fetchone()
        return row[0] if row else 0
    except Exception:
        return "—"

# ---------- UI root ----------
app = ctk.CTk()
app.title("Gamers Guild Admin Dashboard")
app.geometry("1200x750")

# Close cleanly
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

# ---------- sidebar ----------
sidebar = ctk.CTkFrame(app, width=180, corner_radius=0, fg_color="#E0D6FA")
sidebar.pack(side="left", fill="y")
ctk.CTkLabel(sidebar, text="", height=20).pack()

sidebar_buttons = [
    ("Dashboard", "dashboard.png", "admin_dashboard.py"),
    ("Games", "games.png", "game_management.py"),
    ("Orders", "cart.png", "order_management.py"),
    ("Inventory", "inventory.png", "inventory_sales.py"),
    ("Users", "users.png", "user_management.py"),
]

for label, icon, script in sidebar_buttons:
    ctk.CTkButton(
        sidebar,
        text=label,
        image=load_icon(icon),
        compound="left",
        width=160,
        fg_color="transparent",
        hover_color="#D6C9F8",
        text_color="#000",
        command=lambda s=script: open_script(s),
    ).pack(pady=10)

# ---------- main area ----------
main_container = ctk.CTkFrame(app, fg_color="#F5F5FF")
main_container.pack(side="left", fill="both", expand=True)

main = ctk.CTkScrollableFrame(main_container, fg_color="#F5F5FF")
main.pack(fill="both", expand=True)

# header
header = ctk.CTkFrame(main, fg_color="#F9F9FF")
header.pack(fill="x")
ctk.CTkLabel(
    header, text="Admin Dashboard", font=("Helvetica", 18, "bold"), text_color="#000"
).pack(side="left", padx=20, pady=20)
ctk.CTkLabel(header, text="Admin", font=("Helvetica", 14), text_color="#000").pack(
    side="right", padx=20
)

# ---------- dashboard cards ----------
cards = [
    ("Total orders", count("SELECT COUNT(*) FROM `Order`"), "cart.png", "order_management.py"),
    ("Active Users", count("SELECT COUNT(*) FROM Customer WHERE ActiveStatus = 'Active'"), "users.png", "user_management.py"),
    ("Monthly Total Sales", "$22,500", "sales.png", "inventory_sales.py"),  # placeholder
    ("Games Listed", count("SELECT COUNT(*) FROM Game WHERE Stock <> 'Inactive'"), "games.png", "game_management.py"),
]

cards_frame = ctk.CTkFrame(main, fg_color="#F5F5FF")
cards_frame.pack(pady=10, padx=20, fill="x")

for title, value, icon, script in cards:
    ctk.CTkButton(
        cards_frame,
        text=f"{title}\n{value}",
        image=load_icon(icon),
        compound="top",
        width=200,
        height=100,
        corner_radius=10,
        fg_color="#F1E8FF",
        text_color="#000",
        font=("Helvetica", 12, "bold"),
        command=lambda s=script: open_script(s),
    ).pack(side="left", padx=10, pady=10)

# ---------- game management ----------
ctk.CTkLabel(
    main, text="Game Management", font=("Helvetica", 14, "bold"), text_color="#000"
).pack(anchor="w", padx=30, pady=(10, 0))

ctk.CTkButton(
    main,
    text="+ Add Game",
    command=lambda: open_script("add_game_form.py"),
    width=120,
    fg_color="#A58CF3",
    hover_color="#9278DF",
).pack(anchor="e", padx=30, pady=10)

games_frame = ctk.CTkFrame(main, fg_color="#F5F5FF")
games_frame.pack(padx=30, pady=10, fill="x")

def delete_game(gid: int, title: str):
    if messagebox.askyesno("Delete", f"Mark '{title}' as Inactive?"):
        try:
            cursor.execute("UPDATE Game SET Stock = 'Inactive' WHERE GameID = %s", (gid,))
            conn.commit()
            messagebox.showinfo("Updated", f"'{title}' is now Inactive.")
            refresh_games()
        except Exception as e:
            messagebox.showerror("Database Error", f"{e}")

def refresh_games():
    # clear
    for w in games_frame.winfo_children():
        w.destroy()

    # header
    headers = ["Game Title", "Genre", "Price", "Type", "Stock", "Actions"]
    head = ctk.CTkFrame(games_frame, fg_color="#F9F9FF")
    head.pack(fill="x")
    for h in headers:
        ctk.CTkLabel(head, text=h, width=140, anchor="w", text_color="#000").pack(
            side="left", padx=2, pady=4
        )

    # rows
    cursor.execute("SELECT GameID, Title, Genre, Price, Type, Stock FROM Game WHERE Stock <> 'Inactive'")
    for gid, title, genre, price, gtype, stock in cursor.fetchall():
        row = ctk.CTkFrame(games_frame, fg_color="#F1E8FF")
        row.pack(fill="x", pady=2)
        for val in [title, genre, price, gtype, stock]:
            ctk.CTkLabel(row, text=val, width=140, anchor="w", text_color="#000").pack(
                side="left", padx=2, pady=6
            )

        actions = ctk.CTkFrame(row, fg_color="#F1E8FF")
        actions.pack(side="left")

        # EDIT: pass the GameID to the edit form
        ctk.CTkButton(
            actions,
            image=load_icon("edit.png"),
            text="",
            width=40,
            fg_color="#E0D6FA",
            command=lambda gid=gid: open_script("edit_game_form.py", gid),
        ).pack(side="left", padx=2)

        ctk.CTkButton(
            actions,
            image=load_icon("delete.png"),
            text="",
            width=40,
            fg_color="#E0D6FA",
            command=lambda gid=gid, title=title: delete_game(gid, title),
        ).pack(side="left", padx=2)

refresh_games()

# ---------- order management (mini) ----------
ctk.CTkLabel(
    main, text="Order Management", font=("Helvetica", 14, "bold"), text_color="#000"
).pack(anchor="w", padx=30, pady=(20, 0))

search_entry = ctk.CTkEntry(main, placeholder_text="Search", width=160)
search_entry.pack(anchor="e", padx=30)

def refresh_orders(term=None):
    frame = getattr(refresh_orders, "_frame", None)
    if frame:
        for w in frame.winfo_children():
            w.destroy()
        frame.destroy()

    frame = ctk.CTkFrame(main, fg_color="#F5F5FF")
    frame.pack(padx=30, pady=10, fill="x")
    refresh_orders._frame = frame

    headers = ["Order ID", "Name", "Game(s)", "Total", "Status", "Date", "Actions"]
    head = ctk.CTkFrame(frame, fg_color="#F9F9FF")
    head.pack(fill="x")
    for h in headers:
        ctk.CTkLabel(head, text=h, width=120, anchor="w", text_color="#000").pack(
            side="left", padx=2, pady=4
        )

    query = """
        SELECT o.OrderID,
               CONCAT(c.FirstName, ' ', c.LastName) AS FullName,
               GROUP_CONCAT(g.Title SEPARATOR ', ') AS Titles,
               FORMAT(SUM(g.Price), 2) AS Total,
               o.Status,
               o.OrderDate
        FROM `Order` o
        JOIN Customer c   ON o.CustomerID = c.CustomerID
        JOIN OrderItems oi ON o.OrderID = oi.OrderID
        JOIN Game g        ON oi.GameID = g.GameID
    """
    params = ()
    if term:
        query += " WHERE c.FirstName LIKE %s OR c.LastName LIKE %s OR o.OrderID = %s "
        params = (f"%{term}%", f"%{term}%", term)
    query += " GROUP BY o.OrderID ORDER BY o.OrderID DESC LIMIT 3"

    try:
        cursor.execute(query, params)
    except Exception:
        messagebox.showwarning("Invalid Input", "Enter a valid Order ID or Name")
        return

    for row_data in cursor.fetchall():
        row = ctk.CTkFrame(frame, fg_color="#F1E8FF")
        row.pack(fill="x", pady=2)
        for i in range(6):
            ctk.CTkLabel(row, text=row_data[i], width=120, anchor="w", text_color="#000").pack(
                side="left", padx=2, pady=6
            )
        actions = ctk.CTkFrame(row, fg_color="#F1E8FF")
        actions.pack(side="left")
        ctk.CTkButton(actions, image=load_icon("done.png"), text="", width=40, fg_color="#E0D6FA").pack(side="left", padx=2)
        ctk.CTkButton(
            actions,
            image=load_icon("delete.png"),
            text="",
            width=40,
            fg_color="#E0D6FA",
            command=lambda: messagebox.showwarning("Restricted", "Orders cannot be deleted."),
        ).pack(side="left", padx=2)

ctk.CTkButton(
    main,
    text="Search",
    command=lambda: refresh_orders(search_entry.get().strip() or None),
    width=80,
).pack(anchor="e", padx=30, pady=(0, 10))

refresh_orders()

# ---------- go ----------
app.mainloop()
on_close()

<<<<<<< HEAD
=======


>>>>>>> 207446380f2c98b0f02157a6a88829d8b0279944