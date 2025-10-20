import plotly.express as px
from utilis import df_rec_estado, df_rec_mensal, df_rec_categoria, df_vendedores

grafico_estado = px.scatter_geo(    

    df_rec_estado,
    lat='lat',
    lon='lon',
    scope='south america',
    size= 'Preço',
    template= 'seaborn',
    hover_name= 'Local da compra',
    hover_data= {'lat': False, 'lon': False},
    title='Receita por Estado'
    
)

grafico_mensal = px.line(
    df_rec_mensal,
    x = 'Mes',
    y = 'Preço',
    markers= True,
    range_y = (0, df_rec_mensal.max()),
    color = 'Ano',
    line_dash= 'Ano',
    title = 'Receita Mensal'
)

grafico_mensal.update_layout(yaxis_title = 'Receita')

grafico_estado_rec = px.bar(
    df_rec_estado.head(10),
    x = 'Local da compra',
    y = 'Preço',
    text_auto = True,
    title= 'Top Receita por Estados'
)

grafico_categoria = px.bar(
    df_rec_categoria.head(10),
    text_auto = True,
    title= 'Receita Categoria Top 10'
)

grafico_vendedores = px.bar(
    df_vendedores[['sum']].sort_values('sum', ascending=False).head(7),
    x = 'sum',
    y = df_vendedores[['sum']].sort_values('sum', ascending=False).head(7).index,
    text_auto=True,
    title= 'Top 10 Vendedores por Receita'
)

grafico_vendedores_vendas = px.bar(
      df_vendedores[['count']].sort_values('count', ascending=False).head(7),
    x = 'count',
    y = df_vendedores[['count']].sort_values('count', ascending=False).head(7).index,
    text_auto=True,
    title='Top 7 Vendedores Vendas'
)