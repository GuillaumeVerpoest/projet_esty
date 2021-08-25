from pymongo import MongoClient
import pandas as pd 
#import streamlit as st


class Conn:

    def __init__(self) -> None:
        #self.client = MongoClient(st.secrets["mongodb_key"])
        self.client = MongoClient("mongodb+srv://Guillaume:Guillaume@cluster0.bk25f.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

    def insert_many(self,liste_data):
        mydb = self.client["esty"]
        mycol = mydb["esty"]
        mycol.insert_many(liste_data)


    def get_data(self):
        mydb = self.client["esty"]
        mycol = mydb["esty"]
        x = mycol.find()
        return pd.DataFrame(x)

# df = Conn().get_data()
# df.to_csv("test.csv")
