import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from pathlib import Path

CLEAN_PATH = Path("data/vgsales_clean.csv")


@st.cache_data
def load_data():
    df = pd.read_csv(CLEAN_PATH)
    return df


def apply_filters(df):
    st.sidebar.title("Filtros")

    st.sidebar.markdown("Ajuste os filtros abaixo para atualizar os gráficos em tempo real.")

    st.sidebar.subheader("Gênero")
    genres = sorted(df["Genre"].unique())
    selected_genres = st.sidebar.multiselect(
        "Selecione os gêneros:",
        options=genres,
        default=genres,
    )

    st.sidebar.subheader("Plataforma")
    platforms = sorted(df["Platform"].unique())
    selected_platforms = st.sidebar.multiselect(
        "Selecione as plataformas:",
        options=platforms,
        default=platforms,
    )

    st.sidebar.subheader("Ano de lançamento")
    year_min = int(df["Year"].min())
    year_max = int(df["Year"].max())

    selected_years = st.sidebar.slider(
        "Intervalo de anos:",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max),
    )

    df_filtered = df.copy()
    df_filtered = df_filtered[df_filtered["Genre"].isin(selected_genres)]
    df_filtered = df_filtered[df_filtered["Platform"].isin(selected_platforms)]
    df_filtered = df_filtered[df_filtered["Year"].between(selected_years[0], selected_years[1])]

    return df_filtered


def kpi_section(df):
    col1, col2, col3 = st.columns(3)

    total_games = len(df)
    total_sales = df["Total_Sales"].sum()
    unique_genres = df["Genre"].nunique()

    with col1:
        st.metric(
            label="🎮 Jogos no filtro",
            value=f"{total_games:,}".replace(",", "."),
            help="Quantidade de registros (jogos) após os filtros."
        )

    with col2:
        st.metric(
            label="💰 Vendas globais (mi)",
            value=f"{total_sales:.1f}",
            help="Soma das vendas globais em milhões (NA, EU, JP e outros)."
        )

    with col3:
        st.metric(
            label="📂 Gêneros únicos",
            value=str(unique_genres),
            help="Número de gêneros diferentes presentes no filtro atual."
        )


def static_chart(df):
    st.markdown("### 🎮 Top 5 gêneros por vendas globais (gráfico estático)")

    top_genres = (
        df.groupby("Genre")["Total_Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    fig, ax = plt.subplots()
    top_genres.plot(kind="bar", ax=ax, color="skyblue")

    ax.set_title("Top 5 gêneros com maiores vendas globais")
    ax.set_xlabel("Gênero")
    ax.set_ylabel("Vendas globais (milhões)")

    st.pyplot(fig)

    st.caption(
        "Este gráfico mostra os cinco gêneros mais vendidos considerando os filtros atuais. "
        "As barras representam a soma das vendas globais em milhões de unidades."
    )


def interactive_chart(df):
    st.markdown("### 📈 Evolução das vendas globais ao longo dos anos (gráfico interativo)")

    df_group = (
        df.groupby("Year")["Total_Sales"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        df_group,
        x="Year",
        y="Total_Sales",
        markers=True,
        labels={
            "Year": "Ano",
            "Total_Sales": "Vendas globais (milhões)"
        },
        title="Vendas globais ao longo dos anos"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Este gráfico mostra como as vendas globais de video games evoluíram no tempo, "
        "de acordo com o intervalo de anos e demais filtros escolhidos."
    )


def documentation():
    st.markdown("### 📝 Como usar esta página")

    st.markdown(
        """
**Objetivo da página**

Esta página apresenta uma **análise inicial** das vendas de video games, ajudando a responder perguntas como:

- Quais são os gêneros mais vendidos?
- Como as vendas evoluíram ao longo dos anos?
- Como filtros de **gênero**, **plataforma** e **ano de lançamento** influenciam os resultados?

**Como navegar pelos elementos**

1. Use os **filtros na barra lateral** para selecionar:
   - Um ou mais gêneros
   - Uma ou mais plataformas
   - Um intervalo de anos específico

2. Observe os **indicadores no topo** (quantidade de jogos, total de vendas e número de gêneros).

3. Use as **abas** para alternar entre:
   - Visão geral dos gráficos
   - Explicação e interpretação dos dados

Experimente diferentes combinações de filtros para descobrir padrões e tendências no mercado de games. 🎮
        """
    )


def main():
    st.title("🎮 Análise Inicial — Vendas de Video Games")
    st.caption("Exploração geral do dataset de vendas globais de jogos, com filtros interativos.")

    df = load_data()
    df_filtered = apply_filters(df)

    st.markdown(f"**Total de registros após filtros:** {len(df_filtered)}")

    kpi_section(df_filtered)

    st.markdown("---")

    tab1, tab2 = st.tabs(["📊 Gráficos", "📘 Explicação"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            static_chart(df_filtered)
        with col2:
            interactive_chart(df_filtered)

    with tab2:
        documentation()


if __name__ == "__main__":
    main()
