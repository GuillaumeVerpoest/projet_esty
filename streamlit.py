import streamlit as st
import numpy as np
import plotly.express as px
import pandas as  pd 
from connect_mongodb import Conn
import re




class Design():

    def create_df_calculed(self):
        l = []
        df = Conn().get_data()
        df.to_csv("test.csv")
        df.price = pd.to_numeric(df.price)

        for y in df.date.unique():
            d = {}
            d["date"] = y
            for i in df["produit"].unique():
                d[i+"_mean"] = df[df["produit"] == i].price.mean()
                d[i+"_max"] = df[df["produit"] == i].price.max()
                d[i+"_min"] = df[df["produit"] == i].price.min()
                d[i+"_median"] = df[df["produit"] == i].price.median()
            l.append(d)
        df_calculed = pd.json_normalize(l)
        return df, df_calculed
        
    



    def main(self):

        df_origin ,df_graph = self.create_df_calculed()
        df_origin = df_origin[df_origin.date == df_origin.date.max()]
        print(df_origin.shape)
        #df.sort_values(by=['col1'])
        menu = ["Graphique"]
        choice = st.sidebar.selectbox("Menu",menu)
        if choice == "Graphique":
            st.text('This is some text.')


            categorie = np.unique([i.split("_")[:-1] for i in df_graph.columns.drop("date")]).tolist()
            cat_selected = st.multiselect('Select countries', categorie)
            if not not cat_selected:
                columns_selected = []
                for y in cat_selected:
                    columns_selected.extend([i for i in df_graph.columns if len(re.findall(y, i)) != 0])
                fig_line = px.line(df_graph, x="date", y=columns_selected)
                fig_scatter = px.scatter( df_origin[ df_origin["produit"].isin(cat_selected)], x="price", color="produit")
            else:
                fig_line = px.line(df_graph, x="date", y=df_graph.columns)
                fig_scatter = px.scatter( df_origin, x="price", y='produit', color="produit")

            st.plotly_chart(fig_line)
            st.plotly_chart(fig_scatter)

if __name__ == "__main__":
    Design().main()