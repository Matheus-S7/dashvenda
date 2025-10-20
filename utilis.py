from dataset import df
import pandas as pd
import streamlit as st
import time 

def formatar_numeros(valor, prefix = ""):
    for unit in ['', 'mil']:
        if valor < 1000:
            return f'{prefix} {valor:.2f} {unit}'
        valor /= 1000
    return f'{prefix} {valor:2f} milhões'    

# Dataframe Receita Estado
df_rec_estado = df.groupby('Local da compra')[['Preço']].sum()
df_rec_estado = df.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']].merge(df_rec_estado,
left_on='Local da compra', right_index=True).sort_values('Preço', ascending=False)

# Receita Mensal
df_rec_mensal = (
    df.set_index('Data da Compra')
      .groupby(pd.Grouper(freq='M'))['Preço']
      .sum()
      .reset_index()
)

df_rec_mensal['Ano'] = df_rec_mensal['Data da Compra'].dt.year
df_rec_mensal['Mes'] = df_rec_mensal['Data da Compra'].dt.month_name()
# print(df_rec_mensal)

# Dataframe Receita por Categoria
df_rec_categoria = df.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço',ascending=False)
# print(df_rec_categoria)

# Dataframe Vendedores
df_vendedores = pd.DataFrame(df.groupby('Vendedor')['Preço'].agg(['sum', 'count']))
#print(df_vendedores)

@st.cache_data
def convert_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def mensagem_sucesso():
    sucess = st.success(
        'Arquivo Baixado com sucesso',
        icon='✅')
    time.sleep(3)
    sucess.empty()