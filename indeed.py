from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import os


url=""
def process_job(content):
    soup=BeautifulSoup(content,"html.parser")
    link=os.path.join(url,soup.find("a")['href'][1:])
    title=soup.find(class_="jobTitle").text
    details=soup.find(class_="company_location").find("div")
    company=details.find("span")
    if company is not None:
        company=company.text
    location=details.find("div").text
    job_type=soup.find(class_="tapItem-gutter").text

    return f"{title},{company},{location},{job_type.replace(',',' ')},{link}\n"

def bot(driver,search_term,file):
    locations=["Boston","Chicago","NewYork","Houston","Los Angeles","Atlanta"]
    for location in locations:
        id="text-input-what"
        try:
            search_input= WebDriverWait(driver,10).until(
                        EC.presence_of_element_located((By.ID,id))
            )
            search_input.send_keys(Keys.CONTROL + "a")
            search_input.send_keys(Keys.BACKSPACE)
            search_input.send_keys(search_term)

            search_where= WebDriverWait(driver,10).until(
                        EC.presence_of_element_located((By.ID,"text-input-where"))
            )
            search_where.send_keys(Keys.CONTROL + "a")
            search_where.send_keys(Keys.BACKSPACE)
            search_where.send_keys(location)

            search_input.submit()
            time.sleep(2)

            jobs=WebDriverWait(driver,15).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME,"resultContent"))
            )
            if jobs is not None:
                
                for job in jobs:
                    tag=job.get_attribute("innerHTML")
                    file.write(process_job(tag))
                # close a file
        
        except Exception as e:
             pass
    file.close()

    driver.quit()
if __name__ =="__main__":
    driver = webdriver.Chrome()
    url="https://www.indeed.com/"
    d= driver.get(url)
    driver.maximize_window()
    time.sleep(2)
    search=input("Enter Search term: ")
    if search !="":
        filename=f"{search}.csv"
        file=open(filename,"w")
        file.write(f"title,company,location,job details ,other,Website\n")
        bot(driver=driver,search_term=search,file=file)