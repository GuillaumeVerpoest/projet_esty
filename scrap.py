from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
from connect_mongodb import Conn



class Scrap_esty():
    def __init__(self) -> None:
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.list_df = []

    def scraping(self, html_text, produit):
        soup = BeautifulSoup(html_text, 'html.parser')
        all_li = soup.find_all("li", {"class":"wt-list-unstyled"})
        cpt = 0
        for i in all_li:   
            dict_df = {}
            price = i.find("span",{"class", "currency-value"}).text.replace(",","")
            lien = i.find("a",href=True)["href"]
            profil = i.find("p",{"class", "wt-text-caption"}).text
            desc = i.find("h3",{"class", "wt-mb-xs-0"}).text.replace("\n","")

            dict_df["date"] = self.today
            dict_df["produit"] = produit
            dict_df["price"] = price
            dict_df["lien"] = lien
            dict_df["profil"] = profil
            dict_df["desc"] = desc
            dict_df["id"] = cpt
            self.list_df.append(dict_df)
            cpt+=1


    @staticmethod
    def create_url(produit):
        url = f'https://www.etsy.com/c/jewelry/bracelets/{produit}?explicit=1&locationQuery=3017382'
        print(url)
        return url

    def bracelets(self):
        for produit in ["beaded-bracelets", "charm-bracelets","woven-and-braided-bracelets","bangles","cuff-bracelets","chain-and-link-bracelets"]:
            print("in process..... ", produit)
            url = self.create_url(produit)
            html_text = requests.get(url).text
            self.scraping(html_text, produit)
        # push mongodb
        df = pd.json_normalize(self.list_df)
        import json
        with open('data.json', 'w') as f:
            json.dump(self.list_df, f)
        df.to_csv("test.csv")
        Conn().insert_many(self.list_df)
    


if __name__ == "__main__":
    Scrap_esty().bracelets()



 



