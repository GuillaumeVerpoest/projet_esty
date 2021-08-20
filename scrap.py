from connect_mongodb import Conn
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime



class Scrap_esty():
    def __init__(self) -> None:
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.list_df = []

    def scraping(self, html_text, produit):
        dict_df = {}
        soup = BeautifulSoup(html_text, 'html.parser')
        all_li = soup.find_all("li", {"class":"wt-list-unstyled"})
        for i in all_li:    
            try:           
                price = i.find("span",{"class", "currency-value"}).text
                lien = i.find("a",href=True)["href"]
                profil = i.find("p",{"class", "text-gray-lighter"}).text
                desc= i.find("h3",{"class", "text-gray"}).text.replace("\n","")
                dict_df["date"] = self.today
                dict_df["produit"] = produit
                dict_df["price"] = price
                dict_df["lien"] = lien
                dict_df["profil"] = profil
                dict_df["desc"] = desc
                self.list_df.append(dict_df)
            except:
                pass
            
        
    @staticmethod
    def create_url(produit):
        return f'https://www.etsy.com/c/jewelry/bracelets/{produit}?explicit=1&locationQuery=3017382'

    def bracelets(self):
        for produit in ["beaded-bracelets", "charm-bracelets","woven-and-braided-bracelets","bangles","cuff-bracelets","chain-and-link-bracelets"]:
            print("in process..... ", produit)
            url = self.create_url(produit)
            html_text = requests.get(url).text
            self.scraping(html_text, produit)
        # push mongodb
        Conn().insert_many(self.list_df)
    


if __name__ == "__main__":
    Scrap_esty().bracelets()



 



