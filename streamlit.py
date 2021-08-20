import streamlit as st
import numpy as np
import plotly.express as px
import pandas as  pd 
from connect_mongodb import Conn
#import pdfminer
import re


#st.write(pdfminer.__version__) 



class Design():

    @staticmethod
    def create_df():
        d={'date': [],
        'beaded-bracelets_max': [],
        'beaded-bracelets_min': [],
        'beaded-bracelets_mean': [],
        'charm-bracelets_max': [],
        'charm-bracelets_min': [],
        'charm-bracelets_mean': [],
        'woven-and-braided-bracelets_max': [],
        'woven-and-braided-bracelets_min': [],
        'woven-and-braided-bracelets_mean': [],
        'bangles_max': [],
        'bangles_min': [],
        'bangles_mean': [],
        'cuff-bracelets_max': [],
        'cuff-bracelets_min': [],
        'cuff-bracelets_mean': [],
        'chain-and-link-bracelets_max': [],
        'chain-and-link-bracelets_min': [],
        'chain-and-link-bracelets_mean': []}

        df = Conn().get_data()
        df.price = pd.to_numeric(df.price)

        for y in df.date.unique():
            d["date"].append(y)
            for i in df["produit"].unique():
                d[i+"_mean"].append(df[df["produit"] == i].price.mean())
                d[i+"_max"].append(df[df["produit"] == i].price.max())
                d[i+"_min"].append(df[df["produit"] == i].price.min())
        df_graph = pd.DataFrame(d)
        return df, df_graph





    def main(self):

        df ,df_graph = self.create_df()
        menu = ["Graphique"]
        choice = st.sidebar.selectbox("Menu",menu)
        if choice == "Graphique":
            st.text('This is some text.')


            categorie = np.unique([i.split("_")[:-1] for i in df_graph.columns.drop("date")]).tolist()
            print(categorie)
            cat_selected = st.multiselect('Select countries', categorie)
            if not not cat_selected:
                columns_selected = []
                for y in cat_selected:
                    columns_selected.extend([i for i in df_graph.columns if len(re.findall(y, i)) != 0])
                fig_line = px.line(df_graph, x="date", y=columns_selected)
                fig_scatter = px.scatter(df[df["produit"].isin(cat_selected)], x="price", color="produit")
            else:
                fig_line = px.line(df_graph, x="date", y=df_graph.columns)
                fig_scatter = px.scatter(df, x="price", color="produit")

            st.plotly_chart(fig_line)
            st.plotly_chart(fig_scatter)

if __name__ == "__main__":
    Design().main()