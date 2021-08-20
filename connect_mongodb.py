from pymongo import MongoClient
import pandas as pd 
import streamlit as st


class Conn:

    def __init__(self) -> None:
        self.client = MongoClient(st.secrets["mongodb_key"])

    @classmethod
    def insert_many(cls,liste_data):
        mydb = cls.client["esty"]
        mycol = mydb["esty"]
        mycol.insert_many(liste_data)


    @classmethod
    def get_data(cls):
        mydb = cls.client["esty"]
        mycol = mydb["esty"]
        x = mycol.find()
        return pd.DataFrame(x)
