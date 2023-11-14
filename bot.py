import tkinter as tk
from tkinter import *
from tkinter import messagebox
from Window import Window
import socket
import os
import subprocess
import pyrebase

class Win:
    def __init__(self,PORT):
        self.email_entry=None
        self.password_entry=None
        self.mess1_entry=None
        self.mess2_entry=None
        self.PORT=PORT
        self.root=tk.Tk()
        self.db=  Db(self.root)
        self.widgets()

    def execute_command(self):
        email=self.email_entry.get()
        password=self.password_entry.get()
    
        if email =="" or password =="":
            messagebox.showerror("Validation Failed","All fields required")
        else:
            self.db.login(email,password)
    def widgets(self): 
        self.root.title("Login ")
        width,height=self.root.winfo_screenwidth() , self.root.winfo_screenheight()
        w,h=435,200
        x,y= (width-w) //2 , (height-h) // 2

        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.resizable(width=False,height=False)
  
        frame=tk.Frame(self.root,bg="white")
        frame.grid(row=0,column=0,padx=10,pady=10)
        label1=tk.Label(frame,text="Email",fg="black",anchor="w",bg="white",font="Georgia 12",padx=10,pady=10)
        label1.grid(row=0,column=0,pady=10,padx=10,sticky=W)

        self.email_entry=tk.Entry(frame,width="30",font="Georgia 12")
        self.email_entry.grid(row=0,column=1)

        label2=tk.Label(frame,text="Password",anchor="w",fg="black",bg="white",font="Georgia 12",padx=10,pady=10)
        label2.grid(row=1,column=0,pady=10,padx=10,sticky=W)

        self.password_entry=tk.Entry(frame,width="30",font="Georgia 12",show="*")
        self.password_entry.grid(row=1,column=1)

        button_login =tk.Button(self.root,text="Login",width="15", font="georgia 14",fg="black",bg="green",relief="sunken",command=self.execute_command)
        button_login.grid(column=0,row=1,columnspan=2)
        self.root.mainloop()
        
class Db:
    def __init__(self,root):
        self.win=root
        self.user=None
        self.user_data=None
        self.firebaseConfig = {
            "apiKey": "AIzaSyCjBWCL--pu5A7dNl9o9zsITYO0ff0gRtU",
            "authDomain": "studybot-4d001.firebaseapp.com",
            "databaseURL": "https://studybot-4d001-default-rtdb.firebaseio.com",
            "projectId": "studybot-4d001",
            "storageBucket": "studybot-4d001.appspot.com",
            'messagingSenderId': "346106816697",
            "appId": "1:346106816697:web:169aa587dac6aef9ee9368",
            "measurementId": "G-FRJJPQGNX0"
             }
        self.filepath=os.path.join(os.path.dirname(__file__) ,'data','secret.json')
        try:
            self.firebase=pyrebase.initialize_app(self.firebaseConfig)
           
        except Exception as e:
            messagebox.showerror("Failure","Validation failed contact admin ")
    def login(self,email,password):
        try:
            auth=self.firebase.auth()
            user=auth.sign_in_with_email_and_password(email=email,password=password)
            
            if user:
                user=auth.current_user
                self.user=user
                self.get_info()  
                
        except Exception as e:
             messagebox.showerror("Failure","Wrong Credentials Validation failed contact admin ")
    def save_info(self):
        try:
            pass
        except Exception as e:  
             print(e)
    def get_info(self):
        try:
            db=self.firebase.database()
            ref=db.child(f"users/{self.user['localId']}")
            new_dict=ref.get().val()
            self.user_data=new_dict
            
            if self.user_data['validated']:
                self.win.destroy()
                Window(PORT)
            else:
               messagebox.showerror("Failure","Validation failed contact admin ")
        except Exception as ex:
            print(ex)
def is_port_open(host,port):
    try:
        socket.create_connection((host,port))
        return True
    except Exception as e:
        return False   
if __name__ =="__main__":
    PORT=9292
    HOST="localhost"
    dir=os.path.dirname(__file__)
    folder=os.path.join(dir,"dev")
    if not os.path.exists(folder):
        os.mkdir(folder)
    if is_port_open(HOST,PORT):
        Win(PORT)
    else:
        chrome_path="C:\Program Files\Google\Chrome\Application\chrome.exe"
        command=f'"{chrome_path}" --incognito --remote-debugging-port={PORT} --user-data-dir={folder}'
        try:
            r=subprocess.Popen(command,shell=True)
            if r.pid:
                Win(PORT)
        except Exception as e:
            print(e)
        





 


