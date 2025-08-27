import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import re
import subprocess
from mysql.connector import Error
from core.db import get_connection

# Database Connection
def connect_database():
    return get_connection()

root = ctk.CTk()
root.title("Register User")
root.geometry("780x550")
root.resizable(False, False)

def resize_image(size, image_url):
    original_image = Image.open(f'{image_url}')
    resized_image = original_image.resize((size[0], size[1]))
    return ImageTk.PhotoImage(resized_image)

def checkbox_password():
    password_entry.configure(show="" if checkbox_status.get() else "*")

def login_in():
    subprocess.Popen(["python", "user/LoginUser.py"])
    root.destroy()

def on_clear_click():
    first_name_entry.delete(0, ctk.END)
    last_name_entry.delete(0, ctk.END)
    address_entry.delete(0, ctk.END)
    email_entry.delete(0, ctk.END)
    password_entry.delete(0, ctk.END)
    error_message_label.configure(text="")

# Validation & Database Logic
def field_validation():
    user_fname = first_name_entry.get().strip()
    user_lname = last_name_entry.get().strip()
    user_email = email_entry.get().strip()
    user_address = address_entry.get().strip()
    user_password = password_entry.get().strip()

    if not re.match(r"^[a-zA-Z]+$", user_fname):
        error_message_label.configure(text="Invalid First Name", text_color="red")
    elif not re.match(r"^[a-zA-Z]+$", user_lname):
        error_message_label.configure(text="Invalid Last Name", text_color="red")
    elif not re.match(r"^.{10,119}$", user_address):
        error_message_label.configure(text="Address must be 10-119 characters long", text_color="red")
    elif not re.match(r"^[a-zA-Z0-9_.-]+@[a-zA-Z]+\.[a-zA-Z]{2,}$", user_email):
        error_message_label.configure(text="Enter a valid email address", text_color="red")
    elif len(user_password) < 6:
        error_message_label.configure(text="Password must be at least 6 characters", text_color="red")
    else:
        try:
            conn = connect_database()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Customer (FirstName, LastName, Address, Email, Password)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_fname, user_lname, user_address, user_email, user_password))
            conn.commit()
            cursor.close()
            conn.close()
            error_message_label.configure(text="Successfully Registered", text_color="green")
            on_clear_click()

            login_in()

        except Error as err:
            error_message_label.configure(text=f"Database Error: {err}", text_color="red")

#  GUI Layout
checkbox_status = ctk.BooleanVar()

#Left Part of the Customer Registration Frame
registration_frame_left = ctk.CTkFrame(root,fg_color = "#CDC6FF",width =360,height =550, corner_radius = 0)
registration_frame_left.pack_propagate(False)
registration_frame_left.place(x =0,y =0)

#Outer Right Part of the Customer Registration Frame
registration_outer_frame_right = ctk.CTkFrame(root,fg_color = "#CDC6FF",width =420,height =550, corner_radius = 0)
registration_outer_frame_right.pack_propagate(False)
registration_outer_frame_right.place(x =360,y =0)

#Inner Right Part of the Customer Registration Frame
registration_inner_frame_right = ctk.CTkFrame(root,fg_color = "#C1B7FF", bg_color="#CDC6FF",width =390,height =520,
                                              corner_radius = 15)
registration_inner_frame_right.pack_propagate(False)
registration_inner_frame_right.place(x =360,y =15)

#File Path to the image and its size along with its image placement
register_user_image = resize_image((670,550),image_path("Transparent Background - Gamepad Image.png"))
logo_label = ctk.CTkLabel(registration_frame_left,text = "",image = register_user_image)
logo_label.place(x = 20, y = 130)

#Register Customer Label
register_customer_label = ctk.CTkLabel(registration_inner_frame_right,text = "Register And Join The Guild!",
                                       fg_color = "#C1B7FF",text_color = "#493287",font = ('Montserrat', 20, 'bold'))
register_customer_label.place(x = 70, y = 5)

user_icon_path = image_path("userIcon.png")
email_icon_path = image_path("emailIcon.png")
password_icon_path = image_path("passwordIcon.png")
address_icon_path = image_path("addressIcon.png")

user_icon = ctk.CTkImage(light_image=Image.open(user_icon_path), size=(18, 18))
email_icon = ctk.CTkImage(light_image=Image.open(email_icon_path), size=(18, 18))
password_icon = ctk.CTkImage(light_image=Image.open(password_icon_path), size=(18, 18))
address_icon = ctk.CTkImage(light_image=Image.open(address_icon_path), size=(18, 18))

#First Name Icon
first_name_icon_label = ctk.CTkLabel(registration_inner_frame_right, image=user_icon, text = "", compound="left")
first_name_icon_label.place(x = 50,y = 45)

#First Name Label
first_name_label = ctk.CTkLabel(registration_inner_frame_right,text = "First Name",fg_color = "#C1B7FF",
                                text_color = '#493287',font = ('Montserrat',16))
first_name_label.place(x = 76,y = 45)

#First Name Entry Widget
first_name_entry = ctk.CTkEntry(registration_inner_frame_right,text_color = "#171717",font = ('Montserrat',14),
                                width = 300, height = 35,border_width = 1, border_color = '#6350AE',
                                fg_color = "#FFFFFF", corner_radius = 5)
first_name_entry.place(x = 50,y = 70)

#Last Name Icon
last_name_icon_label = ctk.CTkLabel(registration_inner_frame_right, image=user_icon, text = "", compound="left")
last_name_icon_label.place(x = 50,y = 115)

#Last Name Label
last_name_label = ctk.CTkLabel(registration_inner_frame_right,text = "Last Name",fg_color = "#C1B7FF",
                               text_color = '#493287',font = ('Montserrat',16))
last_name_label.place(x = 76,y = 115)

#Last Name Entry Widget
last_name_entry = ctk.CTkEntry(registration_inner_frame_right,text_color = "#171717",font = ('Montserrat',14),
                               width = 300, height = 35,border_width = 1 ,border_color = '#6350AE',
                               fg_color = "#FFFFFF", corner_radius = 5)
last_name_entry.place(x = 50,y = 140)

#Address Icon
address_icon_label = ctk.CTkLabel(registration_inner_frame_right, image=address_icon, text = "", compound="left")
address_icon_label.place(x = 50,y = 185)

#Address Label
email_label = ctk.CTkLabel(registration_inner_frame_right,text = "Address",fg_color = "#C1B7FF", text_color = '#493287',
                           font = ('Montserrat',16))
email_label.place(x = 76,y = 185)

#Address Entry Widget
address_entry = ctk.CTkEntry(registration_inner_frame_right,text_color = "#171717",font = ('Montserrat',14),
                           width = 300, height = 35,border_width = 1, border_color = '#6350AE', fg_color = "#FFFFFF",
                           corner_radius = 5)
address_entry.place(x = 50,y = 210)


#Email Icon
email_icon_label = ctk.CTkLabel(registration_inner_frame_right, image=email_icon, text = "", compound="left")
email_icon_label.place(x = 50,y = 260)

#Email Label
email_label = ctk.CTkLabel(registration_inner_frame_right,text = "Email",fg_color = "#C1B7FF", text_color = '#493287',
                           font = ('Montserrat',16))
email_label.place(x = 76,y = 260)

#Email Entry Widget
email_entry = ctk.CTkEntry(registration_inner_frame_right,text_color = "#171717",font = ('Montserrat',14),
                           width = 300, height = 35,border_width = 1, border_color = '#6350AE', fg_color = "#FFFFFF",
                           corner_radius = 5)
email_entry.place(x = 50,y = 285)

#Password Icon
password_icon_label = ctk.CTkLabel(registration_inner_frame_right, image=password_icon, text = "", compound="left")
password_icon_label.place(x = 50,y = 330)

#Password Label
password_label = ctk.CTkLabel(registration_inner_frame_right,text = "Password",fg_color = "#C1B7FF",
                              text_color = '#493287',font = ('Montserrat',16))
password_label.place(x = 76,y = 330)

#Password Entry Widget
password_entry = ctk.CTkEntry(registration_inner_frame_right,text_color = "#171717", show= "*",
                              font = ('Montserrat',16),width = 300, height = 35,border_width = 1,
                              border_color = '#6350AE', fg_color = "#FFFFFF", corner_radius = 5)
password_entry.place(x = 50,y = 355)

# Show Password Checkbox
show_password_checkbox = ctk.CTkCheckBox(registration_inner_frame_right, text="Show Password", text_color = '#493287',
                                         font = ('Montserrat',14) ,variable = checkbox_status,
                                         command = checkbox_password)
show_password_checkbox.place(x = 220,y = 400)


# Update Register Button's command to perform validation
register_button = ctk.CTkButton(registration_inner_frame_right, text="Register", text_color="#FFFFFF", width=120,
                                height=44, border_color='#6350AE', fg_color="#493287", hover_color="#25285E",
                                font=('Montserrat', 14, 'bold'), command=field_validation)
register_button.place(x=47, y=460)


# #Clear Button
clear_button = ctk.CTkButton(registration_inner_frame_right,text = "Clear",text_color = "#493287",width = 120,
                             height = 44, border_color = '#6350AE',fg_color = "#FFFFFF",hover_color = "#8E92E6",
                             font = ('Montserrat',14, 'bold'),command = on_clear_click)
clear_button.place(x = 227, y = 460)

#Error Message Label
error_message_label = ctk.CTkLabel(registration_inner_frame_right,text = "", text_color = '#E85854',font = ('inter',15))
error_message_label.place(x = 120,y = 30)


root.mainloop()

