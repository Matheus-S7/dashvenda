import streamlit as st
import plotly.express as px
from dataset import df
from utilis import formatar_numeros
from graficos import grafico_estado, grafico_mensal, grafico_estado_rec, grafico_categoria, grafico_vendedores, grafico_vendedores_vendas

# Layout Página
st.set_page_config(layout='wide')

st.title('Dashbord de Vendas:')

st.sidebar.title('Filtro Vendores')

filtro_vendedor = st.sidebar.multiselect(
    'Vendedores',
    df['Vendedor'].unique()
)

if filtro_vendedor:
    df = df[df['Vendedor'].isin(filtro_vendedor)]


ab1, ab2, ab3 = st.tabs(['Dataset', 'Receita', 'Vendedores'])
with ab1: 
    st.dataframe(df)
with ab2:
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric('Receita Total', formatar_numeros(df['Preço'].sum(), 'R$'))
        st.plotly_chart(grafico_estado, use_container_width=True)
        st.plotly_chart(grafico_estado_rec, use_container_width=True)
    with coluna2:
        st.metric('Quantidade de Vendas',formatar_numeros(df.shape[0]))
        st.plotly_chart(grafico_mensal, use_container_width=True)
        st.plotly_chart(grafico_categoria, use_container_width=True)
with ab3:
    coluna1, coluna1 = st.columns(2)
    with coluna1:
        st.plotly_chart(grafico_vendedores)
        st.plotly_chart(grafico_vendedores_vendas)