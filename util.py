import tkinter as tk # this imports the tkinter library
from tkinter import messagebox # this is use to popup the message  from the massagebox dialog frome the tkinter


def get_button (window, text, color, commond, fg='white'): # this function is used to get the button to form a specific window
    button = tk.Button( 
        window,
        text=text,
        activebackground="black",
        activeforeground="white",
        fg=fg,
        bg=color,
        command=commond,
        height=3,
        width=30,
        font=('helvetica bold', 20)
        
    ) # this function is used to get the button to 



def get_enter_text(window):
    inputtxt = tk.Text(window, height=2, width=15, font=("Arial", 32)) 
    return inputtxt


def get_text_label(window, text):
    label = tk.Label(window, text=text, font=("Arial", 12))
    return label


def get_enter_text(window): # this function is used to get the multiple line text from the user
    inputtxt = tk.Text (window,
                       height= 2,
                       width=15, font=("Arial", 32)) # created the text widget with the specified height and width
    return inputtxt # returns the created  text input area 

def msg_box(title, message):
    messagebox.showinfo(title, message)# displays  a massage box with the specified title and description 
    