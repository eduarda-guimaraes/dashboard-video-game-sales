import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Caminho do arquivo CSV já limpo
CLEAN_PATH = Path("data/vgsales_clean.csv")

st.set_page_config(
    page_title="Dashboard de Vendas de Games",
    page_icon="🎮",
    layout="wide"
)

@st.cache_data
def load_data():
    """
    Carrega o dataset de vendas.
    O uso de cache evita recarregar o arquivo toda vez que atualizamos a página.
    """
    df = pd.read_csv(CLEAN_PATH)
    return df


def apply_filters(df):
    """
    Cria os filtros da barra lateral e aplica ao dataframe:
    - Gênero
    - Plataforma
    - Ano de lançamento
    """

    st.sidebar.title("Filtros")
    st.sidebar.markdown("Ajuste os filtros abaixo para atualizar os gráficos em tempo real.")

    # Filtro por gênero
    st.sidebar.subheader("Gênero")
    genres = sorted(df["Genre"].unique())
    selected_genres = st.sidebar.multiselect(
        "Selecione os gêneros:",
        options=genres,
        default=genres,
    )

    # Filtro por plataforma
    st.sidebar.subheader("Plataforma")
    platforms = sorted(df["Platform"].unique())
    selected_platforms = st.sidebar.multiselect(
        "Selecione as plataformas:",
        options=platforms,
        default=platforms,
    )

    # Filtro por ano (slider)
    st.sidebar.subheader("Ano de lançamento")
    year_min = int(df["Year"].min())
    year_max = int(df["Year"].max())

    selected_years = st.sidebar.slider(
        "Intervalo de anos:",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max),
    )

    # Aplica filtros ao dataframe
    df_filtered = df.copy()
    df_filtered = df_filtered[df_filtered["Genre"].isin(selected_genres)]
    df_filtered = df_filtered[df_filtered["Platform"].isin(selected_platforms)]
    df_filtered = df_filtered[df_filtered["Year"].between(selected_years[0], selected_years[1])]

    return df_filtered


def kpi_section(df):
    """
    Mostra indicadores principais (KPIs):
    - Vendas em NA
    - Vendas em EU
    - Vendas em JP
    - Outras regiões
    """
    col1, col2, col3, col4 = st.columns(4)

    na_sales = df["NA_Sales"].sum()
    eu_sales = df["EU_Sales"].sum()
    jp_sales = df["JP_Sales"].sum()
    other_sales = df["Other_Sales"].sum()

    # Métricas em colunas
    with col1:
        st.metric("🇺🇸 Vendas NA (mi)", f"{na_sales:.1f}")

    with col2:
        st.metric("🇪🇺 Vendas EU (mi)", f"{eu_sales:.1f}")

    with col3:
        st.metric("🇯🇵 Vendas JP (mi)", f"{jp_sales:.1f}")

    with col4:
        st.metric("🌍 Outras Regiões (mi)", f"{other_sales:.1f}")


def regional_comparison_chart(df):
    """
    Gráfico de barras comparando total de vendas por região.
    """

    st.markdown("### 🌍 Comparação de vendas por região (gráfico interativo)")

    regional_data = {
        "Região": ["América do Norte", "Europa", "Japão", "Outras Regiões"],
        "Vendas (milhões)": [
            df["NA_Sales"].sum(),
            df["EU_Sales"].sum(),
            df["JP_Sales"].sum(),
            df["Other_Sales"].sum()
        ]
    }

    df_regional = pd.DataFrame(regional_data)

    fig = px.bar(
        df_regional,
        x="Região",
        y="Vendas (milhões)",
        color="Vendas (milhões)",
        color_continuous_scale="blues",
        title="Comparação de vendas por região geográfica"
    )

    st.plotly_chart(fig, use_container_width=True)


def regional_evolution_chart(df):
    """
    Gráfico de linha mostrando evolução das vendas por região ao longo dos anos.
    """

    st.markdown("### 📈 Evolução das vendas por região ao longo dos anos")

    df_yearly = df.groupby("Year").agg({
        "NA_Sales": "sum",
        "EU_Sales": "sum",
        "JP_Sales": "sum",
        "Other_Sales": "sum"
    }).reset_index()

    fig = go.Figure()

    # Uma linha para cada região
    fig.add_trace(go.Scatter(
        x=df_yearly["Year"],
        y=df_yearly["NA_Sales"],
        mode="lines+markers",
        name="América do Norte"
    ))

    fig.add_trace(go.Scatter(
        x=df_yearly["Year"],
        y=df_yearly["EU_Sales"],
        mode="lines+markers",
        name="Europa"
    ))

    fig.add_trace(go.Scatter(
        x=df_yearly["Year"],
        y=df_yearly["JP_Sales"],
        mode="lines+markers",
        name="Japão"
    ))

    fig.add_trace(go.Scatter(
        x=df_yearly["Year"],
        y=df_yearly["Other_Sales"],
        mode="lines+markers",
        name="Outras Regiões"
    ))

    fig.update_layout(
        title="Evolução das vendas por região ao longo dos anos",
        xaxis_title="Ano",
        yaxis_title="Vendas (milhões)",
        hovermode="x unified"
    )

    st.plotly_chart(fig, use_container_width=True)


def regional_pie_chart(df):
    """
    Gráfico de pizza mostrando porcentagem de cada região no total de vendas.
    """

    st.markdown("### 🥧 Distribuição percentual de vendas por região")

    regional_data = {
        "Região": ["América do Norte", "Europa", "Japão", "Outras Regiões"],
        "Vendas": [
            df["NA_Sales"].sum(),
            df["EU_Sales"].sum(),
            df["JP_Sales"].sum(),
            df["Other_Sales"].sum()
        ]
    }

    df_regional = pd.DataFrame(regional_data)

    fig = px.pie(
        df_regional,
        values="Vendas",
        names="Região",
        title="Distribuição percentual de vendas por região"
    )

    st.plotly_chart(fig, use_container_width=True)


def documentation():
    """
    Aba explicativa com o propósito da página e instruções.
    """

    st.markdown("### 📝 Como usar esta página")
    st.markdown("""
        Esta página compara mercados geográficos diferentes
        para entender onde os jogos vendem mais.
    """)


def main():
    """
    Função principal da página.
    Monta toda a interface e chama as funções auxiliares.
    """

    st.title("🌍 Análise Regional — Vendas de Video Games")
    st.caption("Comparação entre regiões do mundo usando visualizações interativas.")

    df = load_data()
    df_filtered = apply_filters(df)

    st.markdown(f"**Total de registros após filtros:** {len(df_filtered)}")

    kpi_section(df_filtered)

    st.markdown("---")

    tab1, tab2 = st.tabs(["📊 Gráficos", "📘 Explicação"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            regional_comparison_chart(df_filtered)

        with col2:
            regional_pie_chart(df_filtered)

        st.markdown("---")

        regional_evolution_chart(df_filtered)

    with tab2:
        documentation()


if __name__ == "__main__":
    main()
