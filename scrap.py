from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
from connect_mongodb import Conn
import re



class Scrap_esty():
    def __init__(self) -> None:
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.list_df = []
        self.dict_bracelet_fr = {"beaded-bracelets":"bracelets-perles",
                                "bangles":"bracelets-jonc",
                                "charm-bracelets": "bracelets-breloques",
                                "woven-and-braided-bracelets":"bracelets-tissés-tressés",
                                "cuff-bracelets": "Bracelets manchette",
                                "chain-and-link-bracelets":"Bracelets-chaînes-maillons"}

        self.dict_collier_fr = {"pendants":"Pendentifs",
                                "chokers":"ras-de-cou",
                                "charm-necklaces":"colliers-breloques",
                                "crystal-necklaces":"colliers-cristal",
                                "monogram-and-name-necklaces":"collier-prenom-monogramme",
                                "beaded-necklaces": "collier-perles",
                                "chains":"chaines",
                                "bib-necklaces":"colliers-plastron",
                                "tassel-necklaces":"collier-ponpon"
                                }




    def scraping(self, html_text, produit, jewel):
        soup = BeautifulSoup(html_text, 'html.parser')
        all_li = soup.find_all("li", {"class":"wt-list-unstyled"})
        cpt = 0
        for i in all_li:   
            dict_df = {}
            try:
                price = i.find("span",{"class", "currency-value"}).text.replace(",","")
            except:
                pass
            lien = i.find("a",href=True)["href"]
            profil = i.find("p",{"class", "wt-text-caption"}).text
            desc = i.find("h3",{"class", "wt-mb-xs-0"}).text.replace("\n","")

            dict_df["date"] = self.today
            dict_df["produit"] = produit
            dict_df["jewel"] = jewel
            dict_df["price"] = price
            dict_df["lien"] = lien
            dict_df["profil"] = re.sub(' +', ' ', profil)
            dict_df["desc"] = re.sub(' +', ' ', desc.replace('"',""))
            dict_df["id"] = cpt
            self.list_df.append(dict_df)
            cpt+=1


    @staticmethod
    def create_url(jewel, produit):
        url = f'https://www.etsy.com/c/jewelry/{jewel}/{produit}?explicit=1&locationQuery=3017382'
        print(url)
        return url

    def bracelets(self):
        jewel = "bracelets"
        for produit in ["beaded-bracelets", "charm-bracelets","woven-and-braided-bracelets","bangles","cuff-bracelets","chain-and-link-bracelets"]:
            print("in process..... ", produit)
            url = self.create_url(jewel, produit)
            html_text = requests.get(url).text
            self.scraping(html_text, self.dict_bracelet_fr[produit], jewel)
        jewel = "necklaces"
        for produit in ["pendants", "chokers","charm-necklaces","crystal-necklaces","monogram-and-name-necklaces","beaded-necklaces","chains","bib-necklaces","tassel-necklaces"]:
            print("in process..... ", produit)
            url = self.create_url(jewel, produit)
            html_text = requests.get(url).text
            self.scraping(html_text, self.dict_collier_fr[produit],jewel)
        # push mongodb
        df = pd.json_normalize(self.list_df)
        df.desc.replace(r'\r+|\n+|\t+','', regex=True, inplace=True)
        df.profil.replace(r'\r+|\n+|\t+','', regex=True, inplace=True)

        df.to_csv("test.csv")
        print(df.shape)
        Conn().insert_many(self.list_df)
    


if __name__ == "__main__":
    Scrap_esty().bracelets()



 

