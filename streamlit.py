import streamlit as st
import numpy as np
import plotly.express as px
import pandas as  pd 
from connect_mongodb import Conn
import re
from scrap import Scrap_esty




class Design():

    @staticmethod
    def get_df():
        df = Conn().get_data()
        df.price = pd.to_numeric(df.price)
        return df

    @staticmethod
    def create_df_stat(df):
        l = []
        for y in df.date.unique():
            d = {}
            d["date"] = y
            for i in df["produit"].unique():
                d[i+"_mean"] = df[df["produit"] == i].price.mean()
                d[i+"_max"] = df[df["produit"] == i].price.max()
                d[i+"_min"] = df[df["produit"] == i].price.min()
                d[i+"_median"] = df[df["produit"] == i].price.median()
            l.append(d)
        df = pd.json_normalize(l)
        return df 
        
    



    def main(self):

        df = self.get_df()
        menu = ["Bracelets","Colier"]
        choice = st.sidebar.selectbox("Menu",menu)

        if (pd.to_datetime(df.date.max())- pd.to_datetime('today')).days >= 14:
            Scrap_esty().bracelets()
        
        if choice == "Bracelets":
            df = df[df.jewel == "bracelets"]
            df_stat = self.create_df_stat(df)
            st.text(f'Dernière Update {df.date.max()}')


            categorie = np.unique([i.split("_")[:-1] for i in df_stat.columns.drop("date")]).tolist()
            cat_selected = st.multiselect('Select countries', categorie)
            if not not cat_selected:
                columns_selected = []
                for y in cat_selected:
                    columns_selected.extend([i for i in df_stat.columns if len(re.findall(y, i)) != 0])
                fig_line = px.line(df_stat, x="date", y=columns_selected)
                fig_scatter = px.scatter( df[ df["produit"].isin(cat_selected)], x="price", color="produit")
            else:
                fig_line = px.line(df_stat, x="date", y=df_stat.columns)
                fig_scatter = px.scatter( df, x="price", y='produit', color="produit")

            st.plotly_chart(fig_line)
            st.plotly_chart(fig_scatter)


        if choice == "Colier":
            df = df[df.jewel == "necklaces"]
            df_stat = self.create_df_stat(df)
            st.text(f'Dernière Update {df.date.max()}')


            categorie = np.unique([i.split("_")[:-1] for i in df_stat.columns.drop("date")]).tolist()
            cat_selected = st.multiselect('Select countries', categorie)
            if not not cat_selected:
                columns_selected = []
                for y in cat_selected:
                    columns_selected.extend([i for i in df_stat.columns if len(re.findall(y, i)) != 0])
                fig_line = px.line(df_stat, x="date", y=columns_selected)
                fig_scatter = px.scatter( df[ df["produit"].isin(cat_selected)], x="price", color="produit")
            else:
                fig_line = px.line(df_stat, x="date", y=df_stat.columns)
                fig_scatter = px.scatter( df, x="price", y='produit', color="produit")

            st.plotly_chart(fig_line)
            st.plotly_chart(fig_scatter)

if __name__ == "__main__":
    Design().main()