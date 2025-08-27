import customtkinter as ctk
import tkinter as tk
from PIL import Image,ImageTk
from tkinter import messagebox
import re
import subprocess
from mysql.connector import Error

def open_dashboard(firstname):
    root = ctk.CTk()
    root.title("User Dashboard")
    root.geometry("780x550")
    root.resizable(False,False)

user_account_icon_path = image_path("dashboardUserIcon.png")
user_games_icon_path   = image_path("dashboardGameIcon.png")
game_library_icon_path = image_path("dashboardGameLibraryIcon.png")
cart_icon_path         = image_path("dashboardCartIcon.png")
signout_icon_path      = image_path("backButtonIcon.png")    
change_icon_path       = image_path("editIcon.png")

    user_account_icon    = ctk.CTkImage(light_image=Image.open(user_account_icon_path), size=(80, 80))
    user_games_icon      = ctk.CTkImage(light_image=Image.open(user_games_icon_path), size=(80, 80))
    game_library_icon    = ctk.CTkImage(light_image=Image.open(game_library_icon_path), size=(80, 80))
    cart_icon            = ctk.CTkImage(light_image=Image.open(cart_icon_path), size=(80, 80))
    signout_icon         = ctk.CTkImage(light_image=Image.open(signout_icon_path), size=(20, 20))

    def account():
        subprocess.Popen(["python", "user/UserAccount.py"])
        root.destroy()

    def login_user():
        subprocess.Popen(["python", "user/LoginUser.py"])
        root.destroy()

    def games():
        subprocess.Popen(["python", "Games.py"])
        root.destroy()

    def cart():
        subprocess.Popen(["python", "user/UserCart.py"])
        root.destroy()

    def open_library_page():
        subprocess.Popen(["python", "user/library.py"])
        root.destroy()

    def resize_image(size, image_url):
        original_image = Image.open(f'{image_url}')
        resized_image = original_image.resize((size[0], size[1]))
        tk_image = ImageTk.PhotoImage(resized_image)
        return tk_image

    # GUI Design

    user_dashboard_frame_right = ctk.CTkFrame(root, fg_color="#CDC6FF", width=530, height=550, corner_radius=0)
    user_dashboard_frame_right.pack_propagate(False)
    user_dashboard_frame_right.place(x=250, y=0)

    register_user_image = resize_image((900, 700), image_path("userDashboardImage.png"))
    logo_label = ctk.CTkLabel(user_dashboard_frame_right, text="", image=register_user_image)
    logo_label.place(x=-30, y=90)

    user_dashboard_outer_frame_left = ctk.CTkFrame(root, fg_color="#CDC6FF", width=250, height=550, corner_radius=0)
    user_dashboard_outer_frame_left.pack_propagate(False)
    user_dashboard_outer_frame_left.place(x=0, y=0)

    user_dashboard_inner_frame_left = ctk.CTkFrame(root, fg_color="#C1B7FF", bg_color="#CDC6FF", width=110, height=520, corner_radius=15)
    user_dashboard_inner_frame_left.pack_propagate(False)
    user_dashboard_inner_frame_left.place(x=15, y=15)

    # Buttons
    button_user_account = ctk.CTkButton(user_dashboard_inner_frame_left, text='', image=user_account_icon, width=10,
                                        height=10, corner_radius=50, fg_color="#C1B7FF", hover_color="#8E92E6", command=account)
    button_user_account.place(x=8, y=10)

    button_user_games = ctk.CTkButton(user_dashboard_inner_frame_left, text='', image=user_games_icon, width=10,
                                      height=10, corner_radius=50, fg_color="#C1B7FF", hover_color="#8E92E6", command=games)
    button_user_games.place(x=8, y=140)

    button_game_library = ctk.CTkButton(user_dashboard_inner_frame_left, text='', image=game_library_icon, width=10,
                                        height=10, corner_radius=50, fg_color="#C1B7FF", hover_color="#8E92E6", command=open_library_page)
    button_game_library.place(x=8, y=270)

    button_cart = ctk.CTkButton(user_dashboard_inner_frame_left, text='', image=cart_icon, width=10,
                                height=10, corner_radius=50, fg_color="#C1B7FF", hover_color="#8E92E6", command=cart)
    button_cart.place(x=8, y=410)

    button_signout = ctk.CTkButton(user_dashboard_frame_right, text='Signout', text_color="#493287", font=('Montserrat', 18, 'bold'),
                                   image=signout_icon, width=20, height=40, corner_radius=30, fg_color="#C1B7FF", border_color='#6350AE',
                                   border_width=1, hover_color="#8E92E6", command=login_user)
    button_signout.place(x=350, y=470)

    # Welcome Frame

    welcome_label = ctk.CTkLabel(user_dashboard_frame_right, text=f"Welcome to the Guild, ",
                                 font=('Montserrat', 30, 'bold'), text_color = "#493287")
    welcome_label.place(x=20, y=30)

    welcome_name_label = ctk.CTkLabel(user_dashboard_frame_right, text=firstname,
                                   font=('Montserrat', 30, 'bold'), text_color="#F67D48")
    
    welcome_name_label.place(x=345, y=30)

    root.mainloop()

