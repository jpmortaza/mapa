import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static

# Configuração do layout
st.set_page_config(page_title="Dashboard de Dados de Estupro", layout="wide")

# Carregar os dados
@st.cache_data
def load_data():
    df1 = pd.read_excel("Estupro de Vunerável - 2024.xlsx")
    df2 = pd.read_excel("Estupro.xlsx")
    return df1, df2

df1, df2 = load_data()

# Título do dashboard
st.title("Dashboard de Análise de Dados de Estupro")

# Exibir tabelas
st.subheader("Visualização dos Dados")

tab1, tab2 = st.tabs(["Estupro de Vulnerável - 2024", "Estupro"])

with tab1:
    st.dataframe(df1)

with tab2:
    st.dataframe(df2)

# Criar gráficos interativos
st.subheader("Análise Visual")

col1, col2 = st.columns(2)

# Gráfico 1 - Contagem por categoria
with col1:
    categoria_counts = df1.iloc[:, 0].value_counts()
    fig1 = px.bar(categoria_counts, x=categoria_counts.index, y=categoria_counts.values,
                  labels={'x': 'Categoria', 'y': 'Frequência'}, title="Distribuição por Categoria")
    st.plotly_chart(fig1)

# Gráfico 2 - Análise de Tendência Temporal
with col2:
    if 'Data' in df1.columns:
        df1['Data'] = pd.to_datetime(df1['Data'])
        df1.sort_values('Data', inplace=True)
        trend = df1.groupby(df1['Data'].dt.to_period("M")).size()
        fig2 = px.line(trend, x=trend.index.astype(str), y=trend.values,
                       labels={'x': 'Data', 'y': 'Ocorrências'}, title="Tendência de Ocorrências ao Longo do Tempo")
        st.plotly_chart(fig2)

# Filtros interativos
st.sidebar.header("Filtros")
if 'Cidade' in df1.columns:
    cidades = df1['Cidade'].unique()
    cidade_selecionada = st.sidebar.multiselect("Selecione a cidade:", cidades, default=cidades[:3])
    df1 = df1[df1['Cidade'].isin(cidade_selecionada)]
    st.sidebar.write(f"Dados filtrados para {len(df1)} registros.")

# Mapa Interativo
st.subheader("Mapa Interativo de Ocorrências")
if 'Latitude' in df1.columns and 'Longitude' in df1.columns:
    mapa = folium.Map(location=[df1['Latitude'].mean(), df1['Longitude'].mean()], zoom_start=5)
    for _, row in df1.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=row.get('Cidade', 'Localização'),
            tooltip=row.get('Categoria', 'Ocorrência')
        ).add_to(mapa)
    folium_static(mapa)
else:
    st.warning("Dados de Latitude e Longitude não encontrados.")

# Download dos dados
st.sidebar.subheader("Download dos Dados")
st.sidebar.download_button(label="Baixar Dados Filtrados", data=df1.to_csv(index=False), file_name="dados_filtrados.csv", mime='text/csv')

st.write("### Fonte: Dados fornecidos pelo usuário.")
