import streamlit as st
import pandas as pd # <-- Adicionado para garantir o uso de to_datetime e outras funções
from dataset import df
from utilis import convert_csv, mensagem_sucesso

# --- CORREÇÃO DE PRÉ-PROCESSAMENTO (GARANTIR FORMATO DE DATA) ---
# É crucial que a coluna de data seja do tipo datetime antes de filtrar
if not pd.api.types.is_datetime64_any_dtype(df['Data da Compra']):
    df['Data da Compra'] = pd.to_datetime(df['Data da Compra'])


st.title('Dataset de Vendas')
with st.expander('Colunas'):
    colunas= st.multiselect(
        'Selecione as Colunas',
        list(df.columns),
        list(df.columns)        
    )
st.sidebar.title('Filtros')
with st.sidebar.expander('Categoria do Produto'):
    categorias = st.multiselect(
        'Selecione as Categorias',
        df['Categoria do Produto'].unique(),
        df['Categoria do Produto'].unique()
    )

with st.sidebar.expander('Preço do Produto'):
    # Variável renomeada para 'preco' (sem cedilha) para evitar UndefinedVariableError
    preco = st.slider( 
        'Selecione o Preco',
        0, 5000,
        (0, 5000)
    )

with st.sidebar.expander('Data da Compra'):
    data_compra = st.date_input(
        'Selecione a data',
        # Inicializa com o intervalo completo
        (df['Data da Compra'].min(),
         df['Data da Compra'].max()),
        min_value=df['Data da Compra'].min(), # Adicionado para melhor UX
        max_value=df['Data da Compra'].max()  # Adicionado para melhor UX
    )

# --- CORREÇÃO DA QUERY ---

# 1. Converte a tupla de data em strings formatadas (ISO YYYY-MM-DD)
# Isso resolve o erro de 'UndefinedVariableError' para a data
data_inicio_str = data_compra[0].strftime('%Y-%m-%d')
data_fim_str = data_compra[1].strftime('%Y-%m-%d')

# 2. Usa uma f-string para incorporar as variáveis de forma segura
# Note: preco está sem o cedilha (consistente com o slider)
# Note: As strings de data estão entre aspas simples: '{data_inicio_str}'
query = f"""
    `Categoria do Produto` in @categorias and \
    @preco[0] <= Preço <= @preco[1] and \
    '{data_inicio_str}' <= `Data da Compra` <= '{data_fim_str}' 
"""

filtro_dados = df.query(query)
filtro_dados = filtro_dados[colunas]

st.markdown(f"A tabela possui: blue[{filtro_dados.shape[0]}] linha e :blue[{filtro_dados.shape[1]}] colunas")


st.dataframe(filtro_dados)

st.markdown('Escreva o nome do arquivo')

coluna1, coluna2 = st.columns(2)
with coluna1:
    nome_arquivo = st.text_input("",
 label_visibility='collapsed')
    nome_arquivo += '.csv'
with coluna2:
    st.download_button(
        'Baixar arquivo',
        data=convert_csv(filtro_dados),
        file_name=nome_arquivo,
        on_click=mensagem_sucesso
        
    )    
