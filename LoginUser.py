import customtkinter as ctk
import tkinter as tk
import mysql.connector
from PIL import Image,ImageTk
from tkinter import messagebox
import re
import subprocess
import os
import json
import sys

root = ctk.CTk()
root.title("User or Admin Login")
root.geometry("780x550")
root.resizable(False,False)

def user_dashboard():
    subprocess.Popen(["python","UserDashboard.py"])
    root.destroy()

# Function to resize an image
def resize_image(size, image_url):
    # Load the original image
    original_image = Image.open(f'{image_url}')
    resized_image = original_image.resize((size[0], size[1]))
    tk_image = ImageTk.PhotoImage(resized_image)
    return tk_image

def checkbox_password():
    if checkbox_status.get():
        password_entry.configure(show="")  # Show text
    else:
        password_entry.configure(show="*")  # Hide text

checkbox_status = ctk.BooleanVar()

def login_user():
    user_email = email_entry.get().strip()
    user_password = password_entry.get().strip()

    if not user_email or not user_password:
        messagebox.showwarning("Missing Fields", "Please enter both email and password.")
        return
    try:
        conn = mysql.connector.connect(
            host="141.209.241.57",
            port=3306,
            user="darap1s",
            password="mypass",
            database="BIS698M1530_GRP5"
        )
        cursor = conn.cursor()

         # -------- Check Admin login first --------
        admin_query = "SELECT Email FROM Admin WHERE Email = %s AND Password = %s"
        cursor.execute(admin_query, (user_email, user_password))
        admin_result = cursor.fetchone()

        if admin_result:
            # Admin login successful
            messagebox.showinfo("Admin Login", f"Welcome Admin: {user_email}")
            root.destroy()

            # You can launch your AdminDashboard here
            subprocess.Popen(["python", "admin_dashboard.py"])
            return  # Skip customer check


        fname_and_custId_query = "SELECT CustomerID, FirstName FROM Customer WHERE Email = %s AND Password = %s"
        cursor.execute(fname_and_custId_query, (user_email, user_password))
        fname_and_custId_result = cursor.fetchone()  # CustomerID & Firstname from the query

        if fname_and_custId_result:
            customerID = fname_and_custId_result[0]
            firstName = fname_and_custId_result[1]

            # Store the customerID in a file for UserAccount.py to read
            with open("temp_customer_id.txt", "w") as f:
                f.write(str(customerID))

            root.destroy() # Closes the Login Window
            
            # Import functions only when needed to avoid circular imports
            from UserDashboard import open_dashboard
            open_dashboard(firstName)
            
            # Launch UserAccount separately with the customerID
            # subprocess.Popen(["python", "UserAccount.py"])
            
        else:
            messagebox.showerror("Login Failed", "Invalid Email or Password.")

        cursor.close()
        conn.close()

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

#Function to delete text in the Entry Widgets
def on_clear_click():
    email_entry.delete(0, ctk.END)
    password_entry.delete(0, ctk.END)

#Left Part of the Customer Registration Frame
login_frame_left = ctk.CTkFrame(root,fg_color = "#CDC6FF",width =360,height =550, corner_radius = 0)
login_frame_left.pack_propagate(False)
login_frame_left.place(x =0,y =0)

#Outer Right Part of the Customer Registration Frame
login_outer_frame_right = ctk.CTkFrame(root,fg_color = "#CDC6FF",width =420,height =550, corner_radius = 0)
login_outer_frame_right.pack_propagate(False)
login_outer_frame_right.place(x =360,y =0)

#Inner Right Part of the Customer Registration Frame
login_inner_frame_right = ctk.CTkFrame(root,fg_color = "#C1B7FF", bg_color="#CDC6FF",width =390,height =450,
                                              corner_radius = 15)
login_inner_frame_right.pack_propagate(False)
login_inner_frame_right.place(x =360,y = 50)

#File Path to the image and its size along with its image placement
login_image = resize_image((600,600),r"C:\Users\darap\PycharmProjects\darap1s_project\BIS 698_Group 5\Images\loginPage_image.png")
logo_label = ctk.CTkLabel(root,text = "",image = login_image, bg_color="#CDC6FF")
logo_label.place(x = 30, y = 110)

#Login Customer Label
login_customer_label = ctk.CTkLabel(login_inner_frame_right,text = "Welcome Back To The Guild!",
                                       fg_color = "#C1B7FF",text_color = "#493287",font = ('Montserrat', 22, 'bold'))
login_customer_label.place(x = 50, y = 75)

email_icon_path = r"C:\Users\darap\PycharmProjects\darap1s_project\BIS 698_Group 5\Images\emailIcon.png"
password_icon_path = r"C:\Users\darap\PycharmProjects\darap1s_project\BIS 698_Group 5\Images\passwordIcon.png"

email_icon = ctk.CTkImage(light_image=Image.open(email_icon_path), size=(18, 18))
password_icon = ctk.CTkImage(light_image=Image.open(password_icon_path), size=(18, 18))

#Email Icon
email_icon_label = ctk.CTkLabel(login_inner_frame_right, image=email_icon, text = "", compound="left")
email_icon_label.place(x = 50,y = 130)

#Email Label
email_label = ctk.CTkLabel(login_inner_frame_right,text = "Email",fg_color = "#C1B7FF", text_color = '#493287',
                           font = ('Montserrat',18))
email_label.place(x = 76,y = 130)

#Email Entry Widget
email_entry = ctk.CTkEntry(login_inner_frame_right,text_color = "#171717",font = ('Montserrat',14),
                           width = 300, height = 35,border_width = 1, border_color = '#6350AE', fg_color = "#FFFFFF",
                           corner_radius = 5)
email_entry.place(x = 50,y = 160)

#Password Icon
password_icon_label = ctk.CTkLabel(login_inner_frame_right, image=password_icon, text = "", compound="left")
password_icon_label.place(x = 50,y = 210)

#Password Label
password_label = ctk.CTkLabel(login_inner_frame_right,text = "Password",fg_color = "#C1B7FF",
                              text_color = '#493287',font = ('Montserrat',18))
password_label.place(x = 76,y = 210)

#Password Entry Widget
password_entry = ctk.CTkEntry(login_inner_frame_right,text_color = "#171717", show= "*",
                              font = ('Montserrat',16),width = 300, height = 35,border_width = 1,
                              border_color = '#6350AE', fg_color = "#FFFFFF", corner_radius = 5)
password_entry.place(x = 50,y = 240)

# Show Password Checkbox
show_password_checkbox = ctk.CTkCheckBox(login_inner_frame_right, text="Show Password", text_color = '#493287',
                                         font = ('Montserrat',14) ,variable = checkbox_status,
                                         command = checkbox_password)
show_password_checkbox.place(x = 220,y = 285)

#Login Button
login_button = ctk.CTkButton(login_inner_frame_right,text = "Login",text_color = "#FFFFFF",width = 120,
                                height = 44, border_color = '#6350AE',fg_color = "#493287",hover_color = "#25285E",
                                font = ('Montserrat',14, 'bold'), command = login_user)
login_button.place(x = 47, y = 345)

#Clear Button
clear_button = ctk.CTkButton(login_inner_frame_right,text = "Clear",text_color = "#493287",width = 120,
                             height = 44, border_color = '#6350AE',fg_color = "#FFFFFF",hover_color = "#8E92E6",
                             font = ('Montserrat',14, 'bold'),command = on_clear_click)
clear_button.place(x = 227, y = 345)

# Only run this if this file is executed directly
if __name__ == "__main__":
    root.mainloop()