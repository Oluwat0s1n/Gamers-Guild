import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
import os
import sys

# App setup
app = ctk.CTk()
app.title("Reset Password")
app.geometry("400x350")
app.resizable(True, True)

# SQL connection
conn = mysql.connector.connect(
    host="...",
    user="...",
    password="...",
    database="...",
    port=...
)
cursor = conn.cursor()

# Variables
role_var = ctk.StringVar(value="User")
email_var = ctk.StringVar()
new_pass_var = ctk.StringVar()
confirm_pass_var = ctk.StringVar()

# UI Layout
ctk.CTkLabel(app, text="Reset Password", font=("Helvetica", 18, "bold")).pack(pady=15)

ctk.CTkLabel(app, text="Select Role:").pack()
ctk.CTkOptionMenu(app, values=["User", "Admin"], variable=role_var).pack(pady=5)

ctk.CTkLabel(app, text="Email:").pack()
ctk.CTkEntry(app, textvariable=email_var, width=250).pack(pady=5)

ctk.CTkLabel(app, text="New Password:").pack()
ctk.CTkEntry(app, textvariable=new_pass_var, show="*", width=250).pack(pady=5)

ctk.CTkLabel(app, text="Confirm New Password:").pack()
ctk.CTkEntry(app, textvariable=confirm_pass_var, show="*", width=250).pack(pady=5)

# Reset logic
def reset_password():
    email = email_var.get().strip()
    new_pass = new_pass_var.get().strip()
    confirm_pass = confirm_pass_var.get().strip()
    role = role_var.get()

    if not email or not new_pass or not confirm_pass:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    if new_pass != confirm_pass:
        messagebox.showerror("Mismatch", "Passwords do not match.")
        return

    table = "Customer" if role == "User" else "Admin"
    try:
        cursor.execute(f"UPDATE {table} SET Password=%s WHERE Email=%s", (new_pass, email))
        conn.commit()
        if cursor.rowcount == 0:
            messagebox.showerror("Error", f"No {role.lower()} found with that email.")
        else:
            messagebox.showinfo("Success", "Password updated successfully!")
            app.destroy()
            os.execl(sys.executable, sys.executable, "login_user.py")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# Button
ctk.CTkButton(app, text="Reset Password", command=reset_password, width=160).pack(pady=15)

# Main loop
app.mainloop()
cursor.close()
conn.close()

