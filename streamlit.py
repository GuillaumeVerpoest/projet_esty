import streamlit as st
from streamlit_metrics import metric, metric_row
import plotly.express as px
import pandas as  pd 
from connect_mongodb import Conn
from scrap import Scrap_esty
import plotly.graph_objects as go
from random import randrange




class Design():

    @staticmethod
    def get_df():
        df = Conn().get_data()
        df.price = pd.to_numeric(df.price)
        df.to_csv("test.csv")
        return df

    @staticmethod
    def create_data_timeseries(df_origin):
        df_origin["date"] = pd.to_datetime(df_origin["date"])
        df_origin = df_origin.set_index(["date"])

        df2 = df_origin.copy()
        for _ in range(14):
            df2.price =df2.price * randrange(1,5)
            df2.index = df2.index + pd.DateOffset(14)
            df_origin = pd.concat([df2,df_origin])

        m = df_origin["price"].resample('2W').agg(["mean","min","max"])
        return m

    @staticmethod
    def fig_timeseries(m):


        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=m.index,
            y=m["min"]+m["max"],
            fill='tozeroy',
            fillcolor='rgba(0,100,80,0.2)',
            line_color='rgba(255,255,255,0)',
            showlegend=False,
        ))
        fig.add_trace(go.Scatter(
            x=m.index, y=m["mean"],
            line_color='rgb(0,100,80)',
            name='mean',
        ))
        fig.update_layout(title_text="Statistique Global (Valeur non réel)")
        return fig


    def template_board_main(self, df_origin):

        st.text(f'Dernière Update {df_origin.date.max()}')


        cat_selected = st.multiselect('Select countries', df_origin.produit.unique())

        if cat_selected:
            df_origin = df_origin[df_origin["produit"].isin(cat_selected)]

        m = self.create_data_timeseries(df_origin)

        st.metric(label="Streamlit version", value=0.87, delta=0.01)
        metric_row(
            {
                "Total de Données selectioné": df_origin.shape[0],
                "Tendance":m.iloc[-2]["mean"] - m.iloc[-1]["mean"],
            }
        )
        
        cpt = st.slider('Slope', min_value=1, max_value=50, step=1)
        df_board = df_origin[['produit','price','profil']]
        st.dataframe(df_board.sort_values(by=["price"], ascending=False).head(cpt),1000,1000)

        fig_timeseries = self.fig_timeseries(m)
        fig_scatter = px.scatter(df_origin, x="price", y='produit', color="produit")
        st.plotly_chart(fig_timeseries)
        st.plotly_chart(fig_scatter)


        
    def main(self):

        df_origin = self.get_df()
        df_origin = df_origin[df_origin["date"]==df_origin["date"].max()]

        menu = ["Bracelets","Colier"]
        choice = st.sidebar.selectbox("Menu",menu)

        if (pd.to_datetime(df_origin.date.max())- pd.to_datetime('today')).days >= 14:
            Scrap_esty().bracelets()
        
        if choice == "Bracelets":

            df_origin = df_origin[df_origin.jewel == "bracelets"]
            self.template_board_main(df_origin)
        

        if choice == "Colier":
            df_origin = df_origin[df_origin.jewel == "necklaces"]
            self.template_board_main(df_origin)

if __name__ == "__main__":
    Design().main()
