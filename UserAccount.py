import customtkinter as ctk
import tkinter as tk
import mysql.connector
from PIL import Image,ImageTk
from tkinter import messagebox
import re
import subprocess
import os
from UserDashboard import open_dashboard

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("User Account Details")
    root.geometry("780x550")
    root.resizable(False,False)
else:
    root = None

# Function to fetch user details from database
def fetch_user_details(customerID=None):
    # If no customerID provided, try to read from temp file
    if customerID is None and os.path.exists("temp_customer_id.txt"):
        try:
            with open("temp_customer_id.txt", "r") as f:
                customerID = f.read().strip()
        except:
            messagebox.showerror("Error", "Could not retrieve customer ID!")
            return
        
    if not customerID:
        messagebox.showerror("Error", "No customer ID provided!")
        return
    
    conn = mysql.connector.connect(
    host     = "141.209.241.57",
    port     = 3306,
    user     = "darap1s",
    password = "mypass",
    database = "BIS698M1530_GRP5"
    )
    cursor = conn.cursor()

    query = "SELECT FirstName, LastName, Address, Email, Password FROM Customer WHERE CustomerID = %s"
    cursor.execute(query, (customerID,))
    user = cursor.fetchone()

    if user:
        first_name, last_name, address, email, password = user

        # Temporarily make them writable, insert values, and then make readonly again.
        first_name_entry.configure(state="normal")
        first_name_entry.delete(0, tk.END)
        first_name_entry.insert(0, first_name)
        first_name_entry.configure(state="readonly")

        last_name_entry.configure(state="normal")
        last_name_entry.delete(0, tk.END)
        last_name_entry.insert(0, last_name)
        last_name_entry.configure(state="readonly")

        address_entry.configure(state="normal")
        address_entry.delete(0, tk.END)
        address_entry.insert(0, address)
        address_entry.configure(state="readonly")

        email_entry.configure(state="normal")
        email_entry.delete(0, tk.END)
        email_entry.insert(0, email)
        email_entry.configure(state="readonly")

        password_entry.configure(state="normal")
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)
        password_entry.configure(state="readonly")
    else:
        messagebox.showerror("Error", "User not found!")

    cursor.close()
    conn.close()

def enable_editing():
    address_entry.configure(state="normal", fg_color="#FFFFFF")
    # password_entry.configure(state="normal", fg_color="#FFFFFF")

def submit_changes():
    # Retrieve the new values from the entry fields
    customerID = open("temp_customer_id.txt").read().strip()
    new_address = address_entry.get().strip()
    new_password = new_password_entry.get().strip()

    conn = mysql.connector.connect(
        host="141.209.241.57",
        port=3306,
        user="darap1s",
        password="mypass",
        database="BIS698M1530_GRP5"
    )
    cursor = conn.cursor()

    if new_address and new_password:
        update_query = "UPDATE Customer SET Address = %s, Password = %s WHERE CustomerID = %s"
        cursor.execute(update_query, (new_address, new_password, customerID))
    elif new_address:
        update_query = "UPDATE Customer SET Address = %s WHERE CustomerID = %s"
        cursor.execute(update_query, (new_address, customerID))
    else:
        update_query = "UPDATE Customer SET Password = %s WHERE CustomerID = %s"
        cursor.execute(update_query, (new_password, customerID))

    conn.commit()

    # Update the password_entry field after successful update
    if new_password:
        password_entry.configure(state="normal")
        password_entry.delete(0, tk.END)
        password_entry.insert(0, new_password)
        password_entry.configure(state="readonly")

    messagebox.showinfo("Success", "Your details have been updated!")

    cursor.close()
    conn.close()


# Move all UI creation inside a main() function or under if __name__ == "__main__":
if __name__ == "__main__":
    #User Account Icons
    user_icon_path = r"C:\Users\darap\PycharmProjects\darap1s_project\BIS 698_Group 5\Images\userIcon.png"
    email_icon_path = r"C:\Users\darap\PycharmProjects\darap1s_project\BIS 698_Group 5\Images\emailIcon.png"
    password_icon_path = r"C:\Users\darap\PycharmProjects\darap1s_project\BIS 698_Group 5\Images\passwordIcon.png"
    address_icon_path = r"C:\Users\darap\PycharmProjects\darap1s_project\BIS 698_Group 5\Images\addressIcon.png"

    user_icon = ctk.CTkImage(light_image=Image.open(user_icon_path), size=(20, 20))
    email_icon = ctk.CTkImage(light_image=Image.open(email_icon_path), size=(20, 20))
    password_icon = ctk.CTkImage(light_image=Image.open(password_icon_path), size=(20, 20))
    address_icon = ctk.CTkImage(light_image=Image.open(address_icon_path), size=(20, 20))

    #User Dashboard Icons
    user_account_icon_path = r"C:\Users\darap\PycharmProjects\darap1s_project\BIS 698_Group 5\Images\dashboardUserIcon.png"
    user_games_icon_path   = r"C:\Users\darap\PycharmProjects\darap1s_project\BIS 698_Group 5\Images\dashboardGameIcon.png"
    game_library_icon_path = r"C:\Users\darap\PycharmProjects\darap1s_project\BIS 698_Group 5\Images\dashboardGameLibraryIcon.png"
    cart_icon_path         = r"C:\Users\darap\PycharmProjects\darap1s_project\BIS 698_Group 5\Images\dashboardCartIcon.png"
    back_icon_path         = r"C:\Users\darap\PycharmProjects\darap1s_project\BIS 698_Group 5\Images\backButtonIcon.png"
    change_icon_path       = r"C:\Users\darap\PycharmProjects\darap1s_project\BIS 698_Group 5\Images\editIcon.png"

    user_account_icon    = ctk.CTkImage(light_image=Image.open(user_account_icon_path), size=(80, 80))
    user_games_icon      = ctk.CTkImage(light_image=Image.open(user_games_icon_path), size=(80, 80))
    game_library_icon    = ctk.CTkImage(light_image=Image.open(game_library_icon_path), size=(80, 80))
    cart_icon            = ctk.CTkImage(light_image=Image.open(cart_icon_path), size=(80, 80))
    back_icon            = ctk.CTkImage(light_image=Image.open(back_icon_path), size=(35, 35))
    change_icon          = ctk.CTkImage(light_image=Image.open(change_icon_path), size=(15, 15))

    def account():
        subprocess.Popen(["python","UserAccount.py"])
        root.destroy()

    
    def games_library():
        subprocess.Popen(["python", "library.py"])
        root.destroy()

    def user_dashboard():

        user_email = email_entry.get().strip()
        user_password = password_entry.get().strip()

        conn = mysql.connector.connect(
        host     = "141.209.241.57",
        port     = 3306,
        user     = "darap1s",
        password = "mypass",
        database = "BIS698M1530_GRP5"
        )
        cursor = conn.cursor() 

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

           
        # root.destroy()

    def games():
        subprocess.Popen(["python","Games.py"])
        root.destroy()

    def checkbox_password():
        if checkbox_status.get():
            password_entry.configure(show="")  
            new_password_entry.configure(show="") # Show text
        else:
            password_entry.configure(show="*")  
            new_password_entry.configure(show="*") # Hide text

    checkbox_status = ctk.BooleanVar()

    def enable_newPassword_submitButton():

        enable_editing()

        # Show the New Password widgets & submit button
        new_password_icon_label.place(x = 20,y = 325)
        new_password_label.place(x = 50,y = 325)
        new_password_entry.place(x = 180,y = 325)
        show_password_checkbox.place(x = 320,y = 365)
        button_submit.place(x=180, y=400)


        # Enable typing and checkbox
        new_password_entry.configure(state="normal")
        show_password_checkbox.configure(state="normal")

    def cart():
        subprocess.Popen(["python","UserCart.py"])
        root.destroy()

    #Outer Right Part of the Customer Registration Frame
    user_dashboard_outer_frame_right = ctk.CTkFrame(root,fg_color = "#CDC6FF",width =630,height =550, corner_radius = 0)
    user_dashboard_outer_frame_right.pack_propagate(False)
    user_dashboard_outer_frame_right.place(x = 150,y =0)

    #Inner Right Part of the User Dashboard Frame
    user_dashboard_inner_frame_right = ctk.CTkFrame(user_dashboard_outer_frame_right,fg_color = "#C1B7FF", bg_color="#CDC6FF",
                                                    width = 560,height = 450, corner_radius = 15)
    user_dashboard_inner_frame_right.pack_propagate(False)
    user_dashboard_inner_frame_right.place(x = 30,y = 40)

    #User Details Label
    label_user_details = ctk.CTkLabel(user_dashboard_outer_frame_right,text = "User Details",
                                           fg_color = "#CDC6FF",text_color = "#493287",font = ('Montserrat', 20, 'bold'))
    label_user_details.place(x = 50, y = 10)

    #Outer Left Part of the User Dashboard Frame
    user_dashboard_outer_frame_left = ctk.CTkFrame(root,fg_color = "#CDC6FF",width = 150,height =550, corner_radius = 0)
    user_dashboard_outer_frame_left.pack_propagate(False)
    user_dashboard_outer_frame_left.place(x =0,y =0)

    #Inner Left Part of the User Dashboard Frame
    user_dashboard_inner_frame_left = ctk.CTkFrame(root,fg_color = "#C1B7FF", bg_color="#CDC6FF",width = 110,height = 520,
                                                  corner_radius = 15)
    user_dashboard_inner_frame_left.pack_propagate(False)
    user_dashboard_inner_frame_left.place(x = 15,y = 15)

    #User Account Button
    button_user_account = ctk.CTkButton(user_dashboard_inner_frame_left, text='', image=user_account_icon, width = 10,
                                        height = 10, corner_radius=50, fg_color="#C1B7FF", hover_color="#8E92E6", command=account)
    button_user_account.place(x=8, y=10)

    #User Games Button
    button_user_games = ctk.CTkButton(user_dashboard_inner_frame_left, text='', image = user_games_icon, width = 10,
                                        height = 10, corner_radius=50, fg_color="#C1B7FF", hover_color="#8E92E6", command=games)
    button_user_games.place(x=8, y=140)

    #Game Library Button
    button_game_library = ctk.CTkButton(user_dashboard_inner_frame_left, text='', image = game_library_icon, width = 10,
                                        height = 10, corner_radius=50, fg_color="#C1B7FF", hover_color="#8E92E6", command=games_library)
    button_game_library.place(x=8, y=270)

    #User Cart Button
    button_cart = ctk.CTkButton(user_dashboard_inner_frame_left, text='', image = cart_icon, width = 10,
                                        height = 10, corner_radius=50, fg_color="#C1B7FF", hover_color="#8E92E6", command=cart)
    button_cart.place(x=8, y=410)

    #First Name Icon
    first_name_icon_label = ctk.CTkLabel(user_dashboard_inner_frame_right, image=user_icon, text = "", compound="left")
    first_name_icon_label.place(x = 20,y = 25)

    #First Name Label
    first_name_label = ctk.CTkLabel(user_dashboard_inner_frame_right,text = "First Name",fg_color = "#C1B7FF",
                                    text_color = '#493287',font = ('Montserrat',18))
    first_name_label.place(x = 45,y = 25)

    #First Name Entry Widget
    first_name_entry = ctk.CTkEntry(user_dashboard_inner_frame_right,text_color = "#171717",font = ('Montserrat',16),
                                    width = 270, height = 35,border_width = 1, border_color = '#6350AE',
                                    fg_color = "#A9A9A9", corner_radius = 5, state = "readonly")
    first_name_entry.place(x = 180,y = 25)

    #Last Name Icon
    last_name_icon_label = ctk.CTkLabel(user_dashboard_inner_frame_right, image=user_icon, text = "", compound="left")
    last_name_icon_label.place(x = 20,y = 85)

    #Last Name Label
    last_name_label = ctk.CTkLabel(user_dashboard_inner_frame_right,text = "Last Name",fg_color = "#C1B7FF",
                                   text_color = '#493287',font = ('Montserrat',18))
    last_name_label.place(x = 45,y = 85)

    #Last Name Entry Widget
    last_name_entry = ctk.CTkEntry(user_dashboard_inner_frame_right,text_color = "#171717",font = ('Montserrat',14),
                                   width = 270, height = 35,border_width = 1 ,border_color = '#6350AE',
                                   fg_color = "#A9A9A9", corner_radius = 5, state = "readonly")
    last_name_entry.place(x = 180,y = 85)

    #Address Icon
    address_icon_label = ctk.CTkLabel(user_dashboard_inner_frame_right, image=address_icon, text = "", compound="left")
    address_icon_label.place(x = 20,y = 145)

    #Address Label
    email_label = ctk.CTkLabel(user_dashboard_inner_frame_right,text = "Address",fg_color = "#C1B7FF", text_color = '#493287',
                               font = ('Montserrat',18))
    email_label.place(x = 50,y = 145)

    #Address Entry Widget
    address_entry = ctk.CTkEntry(user_dashboard_inner_frame_right,text_color = "#171717",font = ('Montserrat',14),
                               width = 270, height = 35,border_width = 1, border_color = '#6350AE', fg_color = "#A9A9A9",
                               corner_radius = 5, state = "readonly")
    address_entry.place(x = 180,y = 145)

    #Email Icon
    email_icon_label = ctk.CTkLabel(user_dashboard_inner_frame_right, image=email_icon, text = "", compound="left")
    email_icon_label.place(x = 20,y = 205)

    #Email Label
    email_label = ctk.CTkLabel(user_dashboard_inner_frame_right,text = "Email",fg_color = "#C1B7FF", text_color = '#493287',
                               font = ('Montserrat',18))
    email_label.place(x = 50,y = 205)

    #Email Entry Widget
    email_entry = ctk.CTkEntry(user_dashboard_inner_frame_right,text_color = "#171717",font = ('Montserrat',14),
                               width = 270, height = 35,border_width = 1, border_color = '#6350AE', fg_color = "#A9A9A9",
                               corner_radius = 5, state = "readonly")
    email_entry.place(x = 180,y = 205)

    #Password Icon
    password_icon_label = ctk.CTkLabel(user_dashboard_inner_frame_right, image=password_icon, text = "", compound="left")
    password_icon_label.place(x = 20,y = 265)

    #Password Label
    password_label = ctk.CTkLabel(user_dashboard_inner_frame_right,text = "Password",fg_color = "#C1B7FF",
                                  text_color = '#493287',font = ('Montserrat',18))
    password_label.place(x = 50,y = 265)

    #Password Entry Widget
    password_entry = ctk.CTkEntry(user_dashboard_inner_frame_right,text_color = "#171717", show= "*",
                                  font = ('Montserrat',16),width = 270, height = 35,border_width = 1,
                                  border_color = '#6350AE', fg_color = "#A9A9A9", corner_radius = 5, state = "readonly")
    password_entry.place(x = 180,y = 265)

    #New Password Icon
    new_password_icon_label = ctk.CTkLabel(user_dashboard_inner_frame_right, image=password_icon, text = "", compound="left")

    #New Password Label
    new_password_label = ctk.CTkLabel(user_dashboard_inner_frame_right,text = "New Password",fg_color = "#C1B7FF",
                                  text_color = '#493287',font = ('Montserrat',18))

    #New Password Entry Widget
    new_password_entry = ctk.CTkEntry(user_dashboard_inner_frame_right,text_color = "#171717", show= "*",
                                  font = ('Montserrat',16),width = 270, height = 35,border_width = 1,
                                  border_color = '#6350AE', fg_color = "#FFFFFF", corner_radius = 5, state="disabled")

    # Show Password Checkbox
    show_password_checkbox = ctk.CTkCheckBox(user_dashboard_inner_frame_right, text="Show Password", text_color = '#493287',
                                             font = ('Montserrat',14) ,variable = checkbox_status,
                                             command = checkbox_password)

    #Change Button
    button_change = ctk.CTkButton(user_dashboard_inner_frame_right, text='Change',text_color = "#493287",font = ('Montserrat', 16, 'bold'),
                                image = change_icon, width = 2, height = 2, corner_radius=50, fg_color="#C1B7FF", border_color = '#6350AE',
                                bg_color="#CDC6FF",  border_width=1,hover_color="#8E92E6", command= enable_newPassword_submitButton)
    button_change.place(x=460, y=270)

    #Submit Button
    button_submit = ctk.CTkButton(user_dashboard_inner_frame_right, text='Submit',text_color = "#FFFFFF",font = ('Montserrat', 16, 'bold'),
                                 width = 270, height = 35, corner_radius=20, fg_color="#493287", border_color = '#6350AE',
                                bg_color="#C1B7FF", border_width=1, hover_color="#25285E", command = submit_changes)
    # button_submit.place(x=180, y=400)

    #Back Button
    button_back = ctk.CTkButton(user_dashboard_outer_frame_right, text='Back',text_color = "#493287",font = ('Montserrat', 18, 'bold'),
                                image = back_icon, width = 15, height = 30, corner_radius=30, fg_color="#C1B7FF", border_color = '#6350AE',
                                bg_color="#CDC6FF",  border_width=1,hover_color="#8E92E6", command = user_dashboard)
    button_back.place(x=470, y=500)

    # Read customer ID from file and populate fields
    fetch_user_details()

    root.mainloop()

