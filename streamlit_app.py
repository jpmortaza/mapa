import streamlit as st
import pandas as pd

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

# Filtros interativos
st.sidebar.header("Filtros")
if 'Cidade' in df1.columns:
    cidades = df1['Cidade'].unique()
    cidade_selecionada = st.sidebar.multiselect("Selecione a cidade:", cidades, default=cidades[:3])
    df1 = df1[df1['Cidade'].isin(cidade_selecionada)]
    st.sidebar.write(f"Dados filtrados para {len(df1)} registros.")

# Mapa removido pois Streamlit está sendo utilizado online
else:
    st.warning("Dados de Latitude e Longitude não encontrados.")

# Download dos dados
st.sidebar.subheader("Download dos Dados")
st.sidebar.download_button(label="Baixar Dados Filtrados", data=df1.to_csv(index=False), file_name="dados_filtrados.csv", mime='text/csv')

st.write("### Fonte: Dados fornecidos pelo usuário.")
