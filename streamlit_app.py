import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard de Dados de Estupro",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon=":bar_chart:"
)

# Carregar os dados
@st.cache_data
def load_data():
    df1 = pd.read_csv("Estupro de Vunerável - 2024.csv", encoding="utf-8", sep=None, engine="python")
    df2 = pd.read_csv("Estupro.csv", encoding="utf-8", sep=None, engine="python")
    return df1, df2

df1, df2 = load_data()

# Título do dashboard
st.title("Dashboard de Análise de Dados de Estupro")

# Criar filtros interativos
categorias = df1.columns.tolist()
with st.sidebar:
    st.header("Filtros")
    filtro_coluna = st.selectbox("Selecione a coluna para filtrar:", categorias)
    valores_unicos = df1[filtro_coluna].unique().tolist()
    valores_unicos.insert(0, "Todos")
    filtro_valor = st.selectbox(f"Selecione um valor de {filtro_coluna}:", valores_unicos)

# Aplicar filtro
if filtro_valor != "Todos":
    df1 = df1[df1[filtro_coluna] == filtro_valor]

# Campo de pesquisa
search_term = st.text_input("Pesquisar nos dados:")

if search_term:
    df1 = df1[df1.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)]

# Exibir dados
st.subheader("Visualização dos Dados")
st.dataframe(df1)

st.subheader("Mapa Interativo de Ocorrências")
if 'Latitude' in df1.columns and 'Longitude' in df1.columns:
    st.map(df1[['Latitude', 'Longitude']])
else:
    st.warning("Dados de Latitude e Longitude não encontrados.")

# Download dos dados
st.sidebar.subheader("Download dos Dados")
st.sidebar.download_button(label="Baixar Dados Filtrados", data=df1.to_csv(index=False), file_name="dados_filtrados.csv", mime='text/csv')

st.caption("### Fonte: Dados fornecidos pelo usuário.")
