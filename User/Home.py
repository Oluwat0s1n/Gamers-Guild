import customtkinter as ctk
import tkinter as tk

from PIL import Image,ImageTk
from tkinter import messagebox
import re
import sys
import subprocess
from mysql.connector import Error

root = ctk.CTk()
root.title("Home")
root.geometry("780x550")
root.resizable(False,False)

def login_in():
    Subprocess.Propen(["python","user/LoginUser.py"])
    root.destroy()

def register():
    subprocess.Popen(["python", "RegisterUser.py"])
    root.destroy()

#Function to resize an image
def resize_image(size, image_url):
    # Load the original image
    original_image = Image.open(f'{image_url}')
    resized_image = original_image.resize((size[0], size[1]))
    tk_image = ImageTk.PhotoImage(resized_image)
    return tk_image

#Left Part of Home Frame 
home_frame_left = ctk.CTkFrame(root,fg_color = "#CDC6FF",width =780,height =550, corner_radius = 0)
home_frame_left.pack_propagate(False)
home_frame_left.place(x =0,y =0)

#Right Part of the Home Frame
home_frame_right = ctk.CTkFrame(root,fg_color = "#CDC6FF",width =420,height =550, corner_radius = 0)
home_frame_right.pack_propagate(False)
home_frame_right.place(x =360,y =0)

#Inner Right Part of Home Frame
home_inner_frame_right = ctk.CTkFrame(home_frame_right,fg_color = "#C1B7FF", bg_color="#CDC6FF",width =390,height =520,
                                              corner_radius = 15)
home_inner_frame_right.pack_propagate(False)
home_inner_frame_right.place(x =3,y =15)

#File Path to the image and its size along with its image placement
home_image = resize_image((600,600),image_path("GG_image.png"))
home_logo_label = ctk.CTkLabel(home_frame_left,text = "",image = home_image, bg_color="#CDC6FF")
home_logo_label.place(x = 30, y = 50)

#Label for Gamers Guild Logo 
gamers_guild_label = ctk.CTkLabel(home_frame_left,text = "   Gamers \n Guild",
                                       fg_color = "#CDC6FF",text_color = "#493287",font = ('Segoe', 50, 'bold'))
gamers_guild_label.place(x = 50, y = 350)


#Label for Login Button 
login_customer_label = ctk.CTkLabel(home_inner_frame_right,text = "Already An Existing User? \n Click here to",
                                       fg_color = "#C1B7FF",text_color = "#493287",font = ('Montserrat', 23, 'bold'))
login_customer_label.place(x = 50, y = 80)

#Login Button
login_button = ctk.CTkButton(home_inner_frame_right,text = "Login",text_color = "#FFFFFF",width = 120,
                                height = 44, border_color = '#6350AE',fg_color = "#493287",hover_color = "#25285E",
                                font = ('Montserrat',14, 'bold'), command=login_in)
login_button.place(x = 130, y = 150)

#Label for Register Button 
register_customer_label = ctk.CTkLabel(home_inner_frame_right,text = "   New Here? \n Click here to",
                                       fg_color = "#C1B7FF",text_color = "#493287",font = ('Montserrat', 23, 'bold'))
register_customer_label.place(x = 115, y = 310)


#Register Button
register_button = ctk.CTkButton(home_inner_frame_right,text = "Register",text_color = "#FFFFFF",width = 120,
                                height = 44, border_color = '#6350AE',fg_color = "#493287",hover_color = "#25285E",
                                font = ('Montserrat',14, 'bold'), command=register)
register_button.place(x = 130, y = 380)



root.mainloop()
