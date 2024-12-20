# Author: Rohit Sharma
import datetime
import tkinter as tk
import os
import cv2
from PIL import Image, ImageTk  
import subprocess  
import util

class App:
    def __init__(self):
        self.main_window = tk.Tk()  
        self.main_window.geometry("1080x720+300+75") 
        self.main_window.title("ATTENDYNAMIX")  
        
        self.login_button_main_window = tk.Button(self.main_window, text='login', bg='green', command=self.login) 
        self.login_button_main_window.place(x=750, y=300) 
        
        self.register_new_user_button_main_window = tk.Button(self.main_window, text='register', bg='gray', fg='black', command=self.register_new_user) 
        self.register_new_user_button_main_window.place(x=750, y=400)  
        
        self.webcam_label = tk.Label(self.main_window) 
        self.webcam_label.place(x=10, y=0, width=600, height=500)  
        
        self.add_webcam(self.webcam_label) 
        
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
            
        self.log_path = ',/log.txt'
            
    def add_webcam(self, label): 
        if 'cap' not in self.__dict__:  
            self.cap = cv2.VideoCapture(0) 
        self.label = label  
        self.process_webcam() 
        
    def process_webcam(self):  
        ret, frame = self.cap.read()  
        if ret:  
            self.most_recent_capture_arr = frame  
            img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)  
            self.most_recent_capture_pil = Image.fromarray(img_) 
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)  
            self.label.imgtk = imgtk 
            self.label.configure(image=imgtk) 
        self.label.after(20, self.process_webcam) 
        
    def login(self): 
        unknown_image_path = './.tmp.jpg'
        
        cv2.imwrite(unknown_image_path, self.most_recent_capture_arr)
        output = subprocess.check_output(['face_recognition', self.db_dir, unknown_image_path])
        name = output.split(',')[1][:-3]
        
        if name in ['unknown_person', 'on_person_found']:
            util.msg_box('ups...', ' Unknown user . please register new user or try again.')
        else:
            util.msg_box('welcome...', f'Welcome {name}.')
            with open(self.log_path, 'a') as f:
                f.write(f'{name}, {datetime.now()}\n')
                f.close() 
            
        os.remove(unknown_image_path)
    
    def register_new_user(self): 
        self.register_new_user_window = tk.Toplevel(self.main_window)  
        self.register_new_user_window.geometry("1080x720+350+70")   
            
        self.accept_button_register_new_user_window = tk.Button(self.register_new_user_window, text='accept', bg='green', command=self.accept_register_new_user) 
        self.accept_button_register_new_user_window.place(x=750, y=300)  
        
        self.try_again_button_register_new_user_window = tk.Button(self.register_new_user_window, text='try again', bg='blue', command=self.try_again_register_new_user) 
        self.try_again_button_register_new_user_window.place(x=750, y=400)  
        
        self.capture_label = tk.Label(self.register_new_user_window)     
        self.capture_label.place(x=10, y=0, width=600, height=500) 
        
        self.add_img_to_label(self.capture_label) 
        
       
        self.entry_text_register_new_user = util.get_enter_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=700, y=150)
        
        self.try_again_register_new_user_label = util.get_text_label(self.register_new_user_window, 'please,/n input username:')
        self.try_again_register_new_user_label.place(x=700, y=120)
        
    def try_again_register_new_user(self): 
        self.register_new_user_window.destroy()
        
    def add_img_to_label(self, label): 
        img = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)  
        self.most_recent_capture_pil = Image.fromarray(img)  
        self.most_recent_capture_imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)  
        label.imgtk = self.most_recent_capture_imgtk 
        label.configure(image=self.most_recent_capture_imgtk)  
        self.register_new_user_capture = self.most_recent_capture_arr.copy()
        
    def start(self): 
        self.main_window.protocol("WM_DELETE_WINDOW", self.on_closing)  
        self.main_window.mainloop()  
    
    def accept_register_new_user(self): 
        name = self.entry_text_register_new_user.get(1.0, "end-1c") 
        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture) 
        
        util.msg_box('success!', 'user was registered successfully')
        
        self.register_new_user_window.destroy() 
        
    def on_closing(self): 
        if self.cap: 
            self.cap.release()  
        self.main_window.destroy()  
if __name__ == "__main__":  
    app = App() 
    app.start()  
