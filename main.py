# Author: Rohit Sharma
import datetime
import tkinter as tk
import os
import cv2
from PIL import Image, ImageTk  # to convert PIL images into a format that can be displayed on a Tkinter window
import subprocess  # Import the missing subprocess module
import util

class App:
    def __init__(self):
        self.main_window = tk.Tk()  # to display the main window
        self.main_window.geometry("1080x720+300+75")  # geometry of the main window
        self.main_window.title("SmartAttend")  # title of the main window
        
        self.login_button_main_window = tk.Button(self.main_window, text='login', bg='green', command=self.login)  # self.login_button is a button to login
        self.login_button_main_window.place(x=750, y=300)  # place the login button
        
        self.register_new_user_button_main_window = tk.Button(self.main_window, text='register', bg='gray', fg='black', command=self.register_new_user)  # self.register_new_user_button is a button to register a new user
        self.register_new_user_button_main_window.place(x=750, y=400)  # place the register button
        
        self.webcam_label = tk.Label(self.main_window)  # to display the webcam feed
        self.webcam_label.place(x=10, y=0, width=600, height=500)  # place the webcam label
        
        self.add_webcam(self.webcam_label)  # add the webcam feed to the label
        
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
            
        self.log_path = ',/log.txt'
            
    def add_webcam(self, label):  # function to add the webcam feed to the label
        if 'cap' not in self.__dict__:  # if the webcam is not already opened
            self.cap = cv2.VideoCapture(0)  # Change to the correct camera index if needed
        self.label = label  # add the webcam to the label
        self.process_webcam()  # process the webcam
        
    def process_webcam(self):  # function self .process_webcam to process the webcam feed
        ret, frame = self.cap.read()  # read the frame from the webcam
        if ret:  # if the frame is read successfully
            self.most_recent_capture_arr = frame  # update the most recent capture array
            img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)  # convert the frame to RGB
            self.most_recent_capture_pil = Image.fromarray(img_)  # convert the frame to PIL image
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)  # convert the PIL image to a format that can be displayed on a Tkinter window
            self.label.imgtk = imgtk  # update the label with the new image
            self.label.configure(image=imgtk)  # update the label with the new image
        self.label.after(20, self.process_webcam)  # update the label
        
    def login(self):  # function to login
        unknown_image_path = './.tmp.jpg'
        
        cv2.imwrite(unknown_image_path, self.most_recent_capture_arr)
        output = subprocess.check_output(['face_recognition', self.db_dir, unknown_image_path])
        name = output.split(',')[1][:-3]
        
        if name in ['unknown_person', 'on_person_found']:
            util.msg_box('ups...', ' Unknown user . please register new user or try again.')
        else:
            util.msg_box('welcome...', f'Welcome {name}.')
            with open(self.log_path, 'a') as f:
                f.write(f'{name}, {datetime.now()}\n') # write the date and time for the log file name and datetime object
                f.close() # close the log file
            
        os.remove(unknown_image_path)
    
    def register_new_user(self):  # this is creating a new user window for new registration 
        self.register_new_user_window = tk.Toplevel(self.main_window)  # create a new window for registration
        self.register_new_user_window.geometry("1080x720+350+70")  # geometry of the new window 
            
        self.accept_button_register_new_user_window = tk.Button(self.register_new_user_window, text='accept', bg='green', command=self.accept_register_new_user)  # self.accept_button is a button to accept the registration
        self.accept_button_register_new_user_window.place(x=750, y=300)  # place the accept button
        
        self.try_again_button_register_new_user_window = tk.Button(self.register_new_user_window, text='try again', bg='blue', command=self.try_again_register_new_user)  # self.try_again_button is a button to try again
        self.try_again_button_register_new_user_window.place(x=750, y=400)  # place the try again button
        
        self.capture_label = tk.Label(self.register_new_user_window)  # to display the capture   
        self.capture_label.place(x=10, y=0, width=600, height=500)  # place the capture label
        
        self.add_img_to_label(self.capture_label)  # add the image to the label
        
        # Correct the method name to get_enter_text
        self.entry_text_register_new_user = util.get_enter_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=700, y=150)
        
        self.try_again_register_new_user_label = util.get_text_label(self.register_new_user_window, 'please,/n input username:')
        self.try_again_register_new_user_label.place(x=700, y=120)
        
    def try_again_register_new_user(self):  # function to try again
        self.register_new_user_window.destroy() # destroy the window that was previously registered
        
    def add_img_to_label(self, label):  # function to add the image to the label
        img = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)  # convert the frame to RGB
        self.most_recent_capture_pil = Image.fromarray(img)  # convert the frame to PIL image
        self.most_recent_capture_imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)  # convert the image to PIL image
        label.imgtk = self.most_recent_capture_imgtk  # convert the image to
        label.configure(image=self.most_recent_capture_imgtk)  # update the label with the new image
        self.register_new_user_capture = self.most_recent_capture_arr.copy() # copy the most recent capture
        
    def start(self):  # function to start the application
        self.main_window.protocol("WM_DELETE_WINDOW", self.on_closing)  # this is to close the application when the window is closed
        self.main_window.mainloop()  # start the main loop of the application
    
    def accept_register_new_user(self):  # function to accept the new user registration
        name = self.entry_text_register_new_user.get(1.0, "end-1c") # get the text from the entry field
        
        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture) # capture the image and save it to the database
        
        util.msg_box('success!', 'user was registered successfully') # show a message box to confirm the registration
        
        self.register_new_user_window.destroy()  # destroy the registration window
        
    def on_closing(self):  # function to close the application
        if self.cap:  # if the camera is open
            self.cap.release()  # Release the webcam
        self.main_window.destroy()  # Destroy the main window

if __name__ == "__main__":  # if the script is run directly
    app = App()  # instance of the App class is created
    app.start()  # Start the application
