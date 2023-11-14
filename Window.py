import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException, ElementNotInteractableException,StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup as Soup
import threading 
import os


PATH=os.path.abspath(os.path.dirname(__file__))
class Bot:
    def __init__(self,email,password,mess1,mess2,run,PORT=8989):
        self.questions=[]
        self.url="https://studydaddy.com/"
        self.PORT=PORT
        self.mess1=mess1
        self.email=email
        self.password=password
        self.mess2=mess2
        self.run=run
    def check_if_logged_in(self,driver):
        try:
            links= WebDriverWait(driver,10).until(
                        EC.presence_of_all_elements_located((By.XPATH,"//a"))
                    )
            for link in links:
                if link.get_attribute("innerHTML").__contains__("Sign in"):
                    link.click()
                    return  True
        except Exception as e:
             return False
    
    def find_questions(self,driver,text):
        try:
            found=False
            links=None
            while not found:
                links= WebDriverWait(driver,10).until(
                            EC.presence_of_all_elements_located((By.XPATH,"//a"))
                        )
                if links is not None:
                    found=True
            if found:
                for link in links:
                    if link.get_attribute("innerHTML").strip().__contains__(text):
                        time.sleep(1)
                        link.click()
                        return True
        except Exception as e:     
             return False

    def find_all_Questions(self,driver):
        try:
                q=WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.CLASS_NAME,"accounting-list__title"))
                )
                if q is None:
                    self.find_questions(driver,"Homework Answers")
                items=WebDriverWait(driver,20).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME,"accounting-item"))
                )
                if items is not None:
                    price=""
                    quiz =""
                    n=0
                    f=0
                    for item in items:
                        item=items[n].get_attribute("innerHTML")
                        soup=Soup(item,"html.parser")
                        quiz=soup.find(class_="accounting-item__link").text.strip()
                        price=soup.find(class_="account-item__price").find("div").text.split("$")[1].strip()
                        subject=soup.find(class_="account-item__price").find(class_="accounting-item__price-caption").text.strip()
                        links=WebDriverWait(driver,15).until(
                            EC.presence_of_all_elements_located((By.XPATH,"//a[@class='accounting-item__link']"))
                        )
                        if not quiz in self.questions:
                            links[n].click()
                            time.sleep(1)
                            self.send_propoosal(driver,price)
                            self.questions.append(quiz)
                            break
                        elif n < 5 and f ==0:
                            n +=1
                        elif n ==5 and f ==0:
                            n=0
                            f=1
                else:
                    print("No Questions found")
        except Exception as e:
            pass

    def send_propoosal(self,driver,price):
        try:
            btn_proposal=WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.CLASS_NAME,"js-handshake"))

            )
            if btn_proposal is not None:
                btn_proposal.click()
                message_field=WebDriverWait(driver,10).until(
                EC.presence_of_element_located((By.ID,"proposalform-description"))
                )
                message_field.send_keys(self.mess1)
                price_field=WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.ID,"proposalform-price"))
                )
                price_field.send_keys(price)
                label=WebDriverWait(driver,10).until(
                    EC.presence_of_element_located((By.XPATH,"//label[@class='error-caption']"))
                )
                label.click()
                time.sleep(1)
                message_field.submit()
                mess_body=WebDriverWait(driver,5).until(
                    EC.presence_of_element_located((By.ID,"messageform-body"))
                )
                time.sleep(1)
                mess_body.send_keys(self.mess2)
                btn_chat_btn=WebDriverWait(driver,5).until(
                    EC.presence_of_element_located((By.XPATH,"//span[@class,'js-chat-send-btn']"))
                )
                btn_chat_btn.click()

        except Exception as e:
            pass
        
    def login(self,driver,sign_in):
        try:
            while self.run:
                if sign_in:
                    sign_= WebDriverWait(driver,10).until(
                            EC.presence_of_element_located((By.CLASS_NAME,"js-modal-login"))
                        )
                    # sign_in=driver.find_element(By.CLASS_NAME,'navigation__link_type_login')
                    if sign_ is not None:
                        sign_.click()
                        time.sleep(1)
                        login_user_id="loginform-useridentifier"
                        login_pass_id="loginform-password"
                        
                        user_field= WebDriverWait(driver,10).until(
                            EC.presence_of_element_located((By.ID,login_user_id))
                        )
                        pass_field= WebDriverWait(driver,10).until(
                            EC.presence_of_element_located((By.ID,login_pass_id))
                        )
                        if user_field.get_attribute("value")  !="":
                            user_field.clear()
                        if  pass_field .get_attribute("value") !="":
                            pass_field.clear()

                        user_field.send_keys(self.email)
                        pass_field.send_keys(self.password)
                        pass_field.submit()
                        time.sleep(1)  
                        sign_in =self.check_if_logged_in(driver)
                        if not sign_in:
                            q_found=self.find_questions(driver,"Homework Answers")
                            if q_found:
                                    time.sleep(2)
                                    self.find_all_Questions(driver)         
                     
                elif not sign_in:
                        sign_in =self.check_if_logged_in(driver)
                        if not sign_in:
                            q_found=self.find_questions(driver,"Homework Answers")
                            if q_found:
                                    time.sleep(2)
                                    self.find_all_Questions(driver) 
            print("Execution completed")
        except Exception as e:
            pass                   
    def initialize(self):
        try:
            options=Options()
            options.debugger_address = f"localhost:{self.PORT}"
            options.add_experimental_option("debuggerAddress",f"localhost:{self.PORT}")
            driver = webdriver.Chrome(options=options) 
            driver.get(self.url)
            driver.maximize_window()
            time.sleep(5)
            sign_in=self.check_if_logged_in(driver)
            self.login(driver,sign_in)
            driver.quit()
        except Exception as e:
            pass
class Window:
    def __init__(self,PORT):
        self.email_entry=None
        self.password_entry=None
        self.mess1_entry=None
        self.mess2_entry=None
        self.PORT=PORT
        self.sec_file=".env"
        self.threads=[]
        self.bot=None
        self.flag=True
        self.root=None
        self.widgets()
    def launch(self,run):
        email=self.email_entry.get()
        password=self.password_entry.get()
        mess1=self.mess1_entry.get("1.0",END)
        mess2=self.mess2_entry.get("1.0",END)
        data=(email,password,mess1,mess2)
        self.bot=Bot(email,password,mess1,mess2,run=run,PORT=self.PORT)
        self.bot.initialize()
    def execute_command(self):
        email=self.email_entry.get()
        password=self.password_entry.get()
        mess1=self.mess1_entry.get("1.0",END)
        mess2=self.mess2_entry.get("1.0",END)

        if email =="" or password =="" or mess1 =="" or mess2 =="":
            messagebox.showerror("Validation Failed","All fields required")
        else:
            for t in self.threads:
                self.flag=False
                self.threads.remove(t)
            self.flag=True
            t1=threading.Thread(target=self.launch,args=(self.flag,))
            t1.start()
            self.threads.append(t1)
    def quit(self):
        if self.bot:
            self.bot.run=False
            self.root.destroy()
            print("Exiting....")
        else:
            self.root.destroy()

    def widgets(self):           
        self.root=tk.Tk()
        self.root.title("AutoBidder Bot")
        self.root.geometry("700x350")
        width,height=self.root.winfo_screenwidth() , self.root.winfo_screenheight()
        w,h=700 ,350
        x,y= (width-w) //2 , (height-h) // 2

        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.resizable(width=False,height=False)
        frame=tk.Frame(self.root,bg="white")
        frame.grid(row=0,column=0,padx=10,pady=10)
        label1=tk.Label(frame,text="Email",fg="black",anchor="w",bg="white",font="Georgia 12",padx=10,pady=10)
        label1.grid(row=0,column=0,pady=10,padx=10,sticky=W)

        self.email_entry=tk.Entry(frame,width="30",font="Georgia 12")
        self.email_entry.grid(row=1,column=0)

        label2=tk.Label(frame,text="Password",anchor="w",fg="black",bg="white",font="Georgia 12",padx=10,pady=10)
        label2.grid(row=0,column=1,pady=10,padx=10,sticky=W)

        self.password_entry=tk.Entry(frame,width="30",font="Georgia 12",show="*")
        self.password_entry.grid(row=1,column=1)

        label3=tk.Label(frame,text="Message 1",anchor="w",fg="black",bg="white",font="Georgia 12",padx=10,pady=10)
        label3.grid(row=2,column=0,pady=10,padx=10,sticky=W)

        self.mess1_entry=scrolledtext.ScrolledText(frame,font="Georgia 12",width=30,height=6)
        self.mess1_entry.grid(row=3,column=0,pady=10,padx=10)

        label4=tk.Label(frame,text="Message 2",fg="black",anchor="w",bg="white",font="Georgia 12",padx=10,pady=10)
        label4.grid(row=2,column=1,pady=10,padx=10,sticky=W)

        self.mess2_entry=scrolledtext.ScrolledText(frame,font="Georgia 12",width=30,height=6)
        self.mess2_entry.grid(row=3,column=1,pady=10,padx=10)
        button_login =tk.Button(self.root,text="Start",width="15", font="georgia 14",fg="black",bg="green",relief="sunken",command=self.execute_command)
        button_login.grid(column=0,row=1,columnspan=2)
       
        self.root.protocol("WM_DELETE_WINDOW",self.quit)
        self.root.mainloop()
