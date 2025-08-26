import customtkinter as ctk
import tkinter as tk
from tkinter import Entry
import mysql.connector
from PIL import Image,ImageTk
from tkinter import messagebox
import re
import subprocess
from decimal import Decimal

root = ctk.CTk()
root.title("Cart 111")
root.geometry("780x550")
root.resizable(False,False)

conn = mysql.connector.connect(
    host="...",
    user="...",
    password="...",
    database="...",
    port=...
)
cursor = conn.cursor()

# Icons
icon_path = r"C:\Users\file_path\Images\Icon.png"

user_account_icon    = ctk.CTkImage(light_image=Image.open(user_account_icon_path), size=(80, 80))
user_games_icon      = ctk.CTkImage(light_image=Image.open(user_games_icon_path), size=(80, 80))
game_library_icon    = ctk.CTkImage(light_image=Image.open(game_library_icon_path), size=(80, 80))
cart_icon            = ctk.CTkImage(light_image=Image.open(cart_icon_path), size=(80, 80))
back_icon            = ctk.CTkImage(light_image=Image.open(back_icon_path), size=(35, 35))
cart_button_icon     = ctk.CTkImage(light_image=Image.open(cart_icon_path), size=(20, 20))
change_icon          = ctk.CTkImage(light_image=Image.open(change_icon_path), size=(15, 15))

def account():
    subprocess.Popen(["python","UserAccount.py"])
    root.destroy()

def featured_games():
    subprocess.Popen(["python","Games.py"])
    root.destroy()

def user_dashboard():
    subprocess.Popen(["python","UserDashboard.py"])
    root.destroy()

def cart():
    subprocess.Popen(["python", "cart.py"])
    root.destroy()

user_dashboard_outer_frame_right = ctk.CTkFrame(root, fg_color="#CDC6FF", width=630, height=550, corner_radius=0)
user_dashboard_outer_frame_right.place(x=150, y=0)

user_dashboard_outer_frame_left = ctk.CTkFrame(root, fg_color="#CDC6FF", width=150, height=550, corner_radius=0)
user_dashboard_outer_frame_left.place(x=0, y=0)

user_dashboard_inner_frame_left = ctk.CTkFrame(user_dashboard_outer_frame_left, fg_color="#C1B7FF", width=110, height=520, corner_radius=15)
user_dashboard_inner_frame_left.place(x=20, y=15)

# Left Side Navigation Buttons
button_user_account = ctk.CTkButton(user_dashboard_inner_frame_left, text='', image=user_account_icon,
                                    width=10, height=10, corner_radius=50, fg_color="#C1B7FF", hover_color="#8E92E6",
                                    command=account)
button_user_account.place(x=8, y=10)

button_user_games = ctk.CTkButton(user_dashboard_inner_frame_left, text='', image=user_games_icon,
                                  width=10, height=10, corner_radius=50, fg_color="#C1B7FF", hover_color="#8E92E6",
                                  command=featured_games)
button_user_games.place(x=8, y=140)

button_game_library = ctk.CTkButton(user_dashboard_inner_frame_left, text='', image=game_library_icon,
                                    width=10, height=10, corner_radius=50, fg_color="#C1B7FF", hover_color="#8E92E6",
                                    command=user_dashboard)
button_game_library.place(x=8, y=270)

button_cart = ctk.CTkButton(user_dashboard_inner_frame_left, text='', image=cart_icon,
                            width=10, height=10, corner_radius=50, fg_color="#C1B7FF", hover_color="#8E92E6",
                            command=cart)
button_cart.place(x=8, y=410)

# Helper to highlight entry fields
def highlight_entry(entry_widget, color):
    entry_widget.configure(border_color=color)

# Fetch Cart Items
def fetch_cart_items():
    try:
        # cursor.execute("SELECT GameTitle, Price FROM Cart")
        with open('temp_customer_id.txt', 'r') as file:
            customer_id = int(file.read().strip())
        cursor.execute("SELECT GameTitle, Price FROM Cart WHERE CustomerID = %s", (customer_id,))

        return cursor.fetchall()
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        return []

# Calculate Total Price with Tax
def calculate_total_price(cart_items):
    total = sum(price for _, price in cart_items)
    total_with_tax = total * Decimal('1.06')
    return round(total_with_tax, 2)

# Display Cart Items and Total Price
def display_cart_items():
    for widget in cart_items_frame.winfo_children():
        widget.destroy()

    cart_items = fetch_cart_items()
    y_position = 10

    if not cart_items:
        empty_label = ctk.CTkLabel(cart_items_frame, text="Your cart is empty!", text_color="black", font=("Arial", 14, "bold"))
        empty_label.place(x=150, y=20)
        
        # Clear total price if empty
        total_price_label.configure(text="Total Price: $0.00")
        return

    for item in cart_items:
        title, price = item

        title_label = ctk.CTkLabel(cart_items_frame, text=title, text_color="black", font=("Arial", 12, "bold"))
        title_label.place(x=30, y=y_position)

        price_label = ctk.CTkLabel(cart_items_frame, text=f"${price:.2f}", text_color="green", font=("Arial", 12))
        price_label.place(x=250, y=y_position)

        y_position += 30

    # Show total price
    total_price = calculate_total_price(cart_items)
    total_price_label.configure(text=f"Total Price (incl. tax): ${total_price:.2f}")

# Clear Cart Items (with confirmation)
def clear_cart():
    confirm = messagebox.askyesno("Confirm Clear Cart", "Are you sure you want to clear your cart and payment details?")
    if confirm:
        try:
            cursor.execute("DELETE FROM Cart")
            conn.commit()
            display_cart_items()

            # Reset Entry fields
            card_number.delete(0, "end")
            expiration_date.delete(0, "end")
            security_code.delete(0, "end")

            # Reset Entry colors
            highlight_entry(card_number, "gray")
            highlight_entry(expiration_date, "gray")
            highlight_entry(security_code, "gray")

            messagebox.showinfo("Cart Cleared", "All items and payment fields have been cleared.")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

def open_library_page():
    subprocess.Popen(["python", "library.py"])
    root.destroy()

# def complete_payment():
#     card_num = card_number.get()
#     exp_date = expiration_date.get()
#     cvv = security_code.get()

#     # Reset all entries to normal color first
#     highlight_entry(card_number, "gray")
#     highlight_entry(expiration_date, "gray")
#     highlight_entry(security_code, "gray")

#     # Validate Card Number (16 digits)
#     if not re.fullmatch(r'\d{16}', card_num):
#         highlight_entry(card_number, "red")
#         messagebox.showerror("Invalid Card Number", "Card number must be exactly 16 digits.")
#         return

#     # Validate Expiration Date (MM/YY format)
#     if not re.fullmatch(r'(0[1-9]|1[0-2])\/\d{2}', exp_date):
#         highlight_entry(expiration_date, "red")
#         messagebox.showerror("Invalid Expiration Date", "Expiration date must be in MM/YY format (e.g., 05/26).")
#         return

#     # Validate CVV (3 digits)
#     if not re.fullmatch(r'\d{3}', cvv):
#         highlight_entry(security_code, "red")
#         messagebox.showerror("Invalid Security Code", "Security code must be exactly 3 digits.")
#         return

#     # If everything is valid
#     messagebox.showinfo(
#         "Payment Successful",
#         "Payment Completed Successfully!\nYou can view your game in your Library.\nThank you!"
#     )

#     # Insert purchased games into Library
#     try:
#         cursor.execute("SELECT GameTitle FROM Cart")
#         games = cursor.fetchall()

#         for game in games:
#             cursor.execute("INSERT INTO Library (GameTitle) VALUES (%s)", (game[0],))

#         conn.commit()

#     except mysql.connector.Error as e:
#         messagebox.showerror("Database Error", f"An error occurred: {e}")

#     # Clear Cart after inserting into Library
#     clear_cart()

#     # open Library page
#     open_library_page()

def complete_payment():
    card_num = card_number.get()
    exp_date = expiration_date.get()
    cvv = security_code.get()

    # Reset all entries to normal color first
    highlight_entry(card_number, "white")
    highlight_entry(expiration_date, "white")
    highlight_entry(security_code, "white")

    # Validate Card Number (16 digits)
    if not re.fullmatch(r'\d{16}', card_num):
        highlight_entry(card_number, "red")
        messagebox.showerror("Invalid Card Number", "Card number must be exactly 16 digits.")
        return

    # Validate Expiration Date (MM/YY format)
    if not re.fullmatch(r'(0[1-9]|1[0-2])\/\d{2}', exp_date):
        highlight_entry(expiration_date, "red")
        messagebox.showerror("Invalid Expiration Date", "Expiration date must be in MM/YY format (e.g., 05/26).")
        return

    # Validate CVV (3 digits)
    if not re.fullmatch(r'\d{3}', cvv):
        highlight_entry(security_code, "red")
        messagebox.showerror("Invalid Security Code", "Security code must be exactly 3 digits.")
        return

    # Read CustomerID from the text file
    try:
        with open('temp_customer_id.txt', 'r') as file:
            customer_id = int(file.read().strip())
    except Exception as e:
        messagebox.showerror("Error", f"Could not read Customer ID: {e}")
        return

    # If everything is valid
    messagebox.showinfo(
        "Payment Successful",
        "Payment Completed Successfully!\nYou can view your game in your Library.\nThank you!"
    )

    # Insert purchased games into Library
    try:
        cursor.execute("SELECT GameTitle FROM Cart")
        games = cursor.fetchall()

        for game in games:
            cursor.execute(
                "INSERT INTO Library (CustomerID, GameTitle) VALUES (%s, %s)",
                (customer_id, game[0])
            )

        conn.commit()

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

    # Clear Cart after inserting into Library
    clear_cart()

    # Open Library page
    open_library_page()


# Title
label_user_details = ctk.CTkLabel(user_dashboard_outer_frame_right, text="Cart",
                                  fg_color="#CDC6FF", text_color="#493287", font=('Montserrat', 30, 'bold'))
label_user_details.place(x=250, y=20)

# Main Right Inner Frame
user_dashboard_inner_frame_right = ctk.CTkFrame(user_dashboard_outer_frame_right, fg_color="#C1B7FF", width=560, height=450, corner_radius=15)
user_dashboard_inner_frame_right.place(x=30, y=60)

# Cart Items Frame
cart_items_frame = ctk.CTkFrame(user_dashboard_inner_frame_right, fg_color="#C1B7FF", width=500, height=120)
cart_items_frame.place(x=30, y=20)

# Total Price Label
total_price_label = ctk.CTkLabel(user_dashboard_inner_frame_right, text="Total Price: $0.00",
                                 text_color="black", font=("Arial", 14, "bold"))
total_price_label.place(x=30, y=150)

display_cart_items()

# Payment Method Section
ctk.CTkLabel(user_dashboard_inner_frame_right, text="PAYMENT METHOD", font=("Arial", 14, "bold"), text_color="black").place(x=30, y=190)

payment_methods = ["Visa", "MasterCard", "PayPal", "American Express"]
selected_payment_method = ctk.StringVar(value="Visa")
ctk.CTkLabel(user_dashboard_inner_frame_right, text="Select a payment method", font=("Arial", 12)).place(x=30, y=230)
ctk.CTkOptionMenu(user_dashboard_inner_frame_right, variable=selected_payment_method, values=payment_methods, width=200).place(x=250, y=230)

# Card Info
ctk.CTkLabel(user_dashboard_inner_frame_right, text="Card number", font=("Arial", 12)).place(x=30, y=270)
card_number = ctk.CTkEntry(user_dashboard_inner_frame_right, width=250)
card_number.place(x=250, y=270)

ctk.CTkLabel(user_dashboard_inner_frame_right, text="Expiration date", font=("Arial", 12)).place(x=30, y=310)
expiration_date = ctk.CTkEntry(user_dashboard_inner_frame_right, width=100)
expiration_date.place(x=250, y=310)

ctk.CTkLabel(user_dashboard_inner_frame_right, text="Security code", font=("Arial", 12)).place(x=30, y=350)
security_code = ctk.CTkEntry(user_dashboard_inner_frame_right, width=100)
security_code.place(x=250, y=350)

# Buttons
complete_payment_button = ctk.CTkButton(
    user_dashboard_inner_frame_right,
    text="Complete Payment",
    fg_color="lightgreen",
    text_color="black",
    font=("Arial", 10, "bold"),
    image=cart_button_icon,
    compound="left",
    command=complete_payment
)
complete_payment_button.place(x=100, y=400)

clear_cart_button = ctk.CTkButton(
    user_dashboard_inner_frame_right,
    text="Clear Cart",
    fg_color="red",
    text_color="white",
    font=("Arial", 10, "bold"),
    image=change_icon,
    compound="left",
    command=clear_cart
)
clear_cart_button.place(x=300, y=400)


root.mainloop()

