import customtkinter as ctk
import mysql.connector
from PIL import Image
from tkinter import messagebox
import subprocess
from UserDashboard import open_dashboard
import os

# SQL Connection
conn = mysql.connector.connect(
    host="...",
    user="...",
    password="...",
    database="...",
    port=...
)
cursor = conn.cursor()
)

# Root window
root = ctk.CTk()
root.title("User Game Library")
root.geometry("780x550")
root.resizable(False, False)

# Navigation functions
def account():
    subprocess.Popen(["python", "UserAccount.py"])
    root.destroy()

def user_dashboard():
    subprocess.Popen(["python", "UserDashboard.py"])
    root.destroy()

def games():
    subprocess.Popen(["python", "Games.py"])
    root.destroy()

def cart():
    subprocess.Popen(["python", "UserCart.py"])
    root.destroy()

def games_library():
    subprocess.Popen(["python", "library.py"])
    root.destroy()

def go_back_to_dashboard():
    try:
        # Read the stored customerID
        if os.path.exists("temp_customer_id.txt"):
            with open("temp_customer_id.txt", "r") as f:
                customerID = f.read().strip()

            # Connect to the database to get the FirstName
            conn = mysql.connector.connect(
    host="...",
    user="...",
    password="...",
    database="...",
    port=...
)
cursor = conn.cursor()

            )
            cursor = conn.cursor()

            fname_query = "SELECT FirstName FROM Customer WHERE CustomerID = %s"
            cursor.execute(fname_query, (customerID,))
            result = cursor.fetchone()

            if result:
                firstName = result[0]
                # Close the Games window (assuming it's using Tkinter)
                root.destroy()
                # Call the dashboard with the firstName
                open_dashboard(firstName)
            else:
                messagebox.showerror("Error", "Failed to retrieve user information.")

            cursor.close()
            conn.close()
        else:
            messagebox.showerror("Error", "Session expired. Please log in again.")
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

# User Dashboard Icons
all_image_path = r"C:\Users\...\Images\Icon.png"

user_account_icon = ctk.CTkImage(light_image=Image.open(user_account_icon_path), size=(80, 80))
user_games_icon = ctk.CTkImage(light_image=Image.open(user_games_icon_path), size=(80, 80))
game_library_icon = ctk.CTkImage(light_image=Image.open(game_library_icon_path), size=(80, 80))
cart_icon = ctk.CTkImage(light_image=Image.open(cart_icon_path), size=(80, 80))
back_icon = ctk.CTkImage(light_image=Image.open(back_icon_path), size=(35, 35))

# Layout setup
user_dashboard_outer_frame_right = ctk.CTkFrame(root, fg_color="#CDC6FF", width=630, height=550, corner_radius=0)
user_dashboard_outer_frame_right.place(x=150, y=0)

user_dashboard_inner_frame_right = ctk.CTkFrame(user_dashboard_outer_frame_right, fg_color="#C1B7FF", width=560, height=450, corner_radius=15)
user_dashboard_inner_frame_right.place(x=30, y=40)

label_user_details = ctk.CTkLabel(user_dashboard_outer_frame_right, text="Games Library",
                                  fg_color="#CDC6FF", text_color="#493287", font=('Montserrat', 20, 'bold'))
label_user_details.place(x=220, y=10)

user_dashboard_outer_frame_left = ctk.CTkFrame(root, fg_color="#CDC6FF", width=150, height=550, corner_radius=0)
user_dashboard_outer_frame_left.place(x=0, y=0)

user_dashboard_inner_frame_left = ctk.CTkFrame(user_dashboard_outer_frame_left, fg_color="#C1B7FF", width=110, height=520, corner_radius=15)
user_dashboard_inner_frame_left.place(x=20, y=15)

# Navigation Buttons
button_user_account = ctk.CTkButton(user_dashboard_inner_frame_left, text='', image=user_account_icon,
                                    width=10, height=10, corner_radius=50, fg_color="#C1B7FF",
                                    hover_color="#8E92E6", command=account)
button_user_account.place(x=8, y=10)

button_user_games = ctk.CTkButton(user_dashboard_inner_frame_left, text='', image=user_games_icon,
                                  width=10, height=10, corner_radius=50, fg_color="#C1B7FF",
                                  hover_color="#8E92E6", command=games)
button_user_games.place(x=8, y=140)

button_game_library = ctk.CTkButton(user_dashboard_inner_frame_left, text='', image=game_library_icon,
                                    width=10, height=10, corner_radius=50, fg_color="#C1B7FF",
                                    hover_color="#8E92E6", command=games_library)
button_game_library.place(x=8, y=270)

button_cart = ctk.CTkButton(user_dashboard_inner_frame_left, text='', image=cart_icon,
                            width=10, height=10, corner_radius=50, fg_color="#C1B7FF",
                            hover_color="#8E92E6", command=cart)
button_cart.place(x=8, y=410)

button_back = ctk.CTkButton(user_dashboard_outer_frame_right, text='Back', text_color="#493287",
                            font=('Montserrat', 18, 'bold'), image = back_icon,
                            width=15, height=30, corner_radius=30, fg_color="#C1B7FF",
                            border_color='#6350AE', bg_color="#CDC6FF",
                            border_width=1, hover_color="#8E92E6", command=go_back_to_dashboard)
button_back.place(x=470, y=500)

# Frame for Games
featured_games_frame = ctk.CTkFrame(user_dashboard_inner_frame_right, fg_color="#C1B7FF", width=500, height=400)
featured_games_frame.place(x=30, y=20)

# Helper function for Download
def download_game(game_title):
    messagebox.showinfo("Download", f"Download started for '{game_title}'!\nPlease wait...")

# Display Games from Library
def display_games_from_db():
    for widget in featured_games_frame.winfo_children():
        widget.destroy()

    try:
        cursor.execute("SELECT CustomerID, GameTitle, PurchaseDate FROM Library")
        games = cursor.fetchall()
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        return

    for i, game in enumerate(games):
        cust_id, title, purchase_date = game

        # Frame for each game
        game_frame = ctk.CTkFrame(featured_games_frame, fg_color="white", width=500, height=80, corner_radius=10)
        game_frame.grid(row=i, column=0, padx=20, pady=10, sticky="w")
        game_frame.pack_propagate(False)

        # Game Title
        title_label = ctk.CTkLabel(game_frame, text=title, fg_color="white", text_color="black",
                                   font=("Arial", 14, "bold"), anchor="w")
        title_label.place(x=20, y=10)

        # Purchase Date
        date_label = ctk.CTkLabel(game_frame, text=f"Purchased: {purchase_date.strftime('%Y-%m-%d')}",
                                  fg_color="white", text_color="gray", font=("Arial", 10), anchor="w")
        date_label.place(x=20, y=40)

        # Download Button
        download_button = ctk.CTkButton(
            game_frame,
            text="Download",
            fg_color="#493287",
            text_color="white",
            font=("Arial", 10, "bold"),
            width=80,
            height=30,
            corner_radius=8,
            command=lambda t=title: download_game(t)
        )
        download_button.place(x=400, y=20)

# Call function to display games
display_games_from_db()

root.mainloop()

