from pymongo import MongoClient
import pandas as pd 
import streamlit as st


class Conn:

    def __init__(self) -> None:
        self.client = MongoClient(st.secrets["mongodb_key"])
      

    def insert_many(self,liste_data):
        mydb = self.client["esty"]
        mycol = mydb["esty"]
        mycol.insert_many(liste_data)


    def get_data(self):
        mydb = self.client["esty"]
        mycol = mydb["esty"]
        x = mycol.find()
        return pd.DataFrame(x)

