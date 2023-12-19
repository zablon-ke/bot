import requests
from bs4 import BeautifulSoup
import os
import re


url=""
#modify the global variable outside its current scope and meaning. 
global run
run=True
def scrape(url): 
    try:
        resposne=requests.get(url=url)
        if resposne.status_code !=200: #the request has succeeded.
            run=False
            return
        content=resposne.content
        soup=BeautifulSoup(content,"html.parser")
        section=soup.find("section",class_="card -fh")
        products=section.find_all(class_="prd _fb col c-prd")
        
        for product in products:
            link= product.find("a")
            info=link.find(class_="info")
            name=info.find("h3").text
            price=info.find(class_="prc").text.replace(",","").strip()
            price1=re.sub("[KSh]","",price)
            old_price=info.find(class_="old").text.replace(",","").strip()
            price2=re.sub("[KSh]","",old_price) 
            discount=info.find(class_="bdg _dsct _sm").text.replace("%","").strip()
            stars=info.find(class_="stars _s")
            ratings=0
            if stars is not None:
                ratings= stars.text.split("out of")[0].strip()
            file.write(f"{name},{price1},{price2},{discount},{ratings} \n")
        print(f"scraping {url}")

    except Exception as e:
        if str(e).__contains__("NoneType"):
            run=False
filename="products.csv"
file=open(filename,"w")
file.write(f"Name,Price,Old Price,% Discount,Ratings \n")

scrape(url=url)

n=2
while run:
    url=f"https://www.jumia.co.ke/mlp-defacto-store/?page={n}#catalog-listing"
    print(f"scraping {url}")
    scrape(url=url)
    #The most common way to increment a variable 
    n +=1
file.close()