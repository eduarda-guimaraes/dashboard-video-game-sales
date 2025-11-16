import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from pathlib import Path

# Caminho do CSV
CLEAN_PATH = Path("data/vgsales_clean.csv")

st.set_page_config(
    page_title="Dashboard de Vendas de Games",
    page_icon="🎮",
    layout="wide"
)

@st.cache_data
def load_data():
    """
    Carrega o dataset usando cache para otimizar desempenho.
    """
    return pd.read_csv(CLEAN_PATH)


def apply_filters(df):
    """
    Cria os filtros específicos desta página:
    - Gênero
    - Plataforma
    - Publisher
    - Ano de lançamento
    """

    st.sidebar.title("Filtros")

    # Filtro por gênero
    st.sidebar.subheader("Gênero")
    genres = sorted(df["Genre"].unique())
    selected_genres = st.sidebar.multiselect("Selecione os gêneros:", genres, genres)

    # Filtro por plataforma
    st.sidebar.subheader("Plataforma")
    platforms = sorted(df["Platform"].unique())
    selected_platforms = st.sidebar.multiselect("Selecione as plataformas:", platforms, platforms)

    # Filtro por publisher
    st.sidebar.subheader("Publisher")
    publishers = sorted(df["Publisher"].unique())
    selected_publishers = st.sidebar.multiselect("Selecione os publishers:", publishers, publishers)

    # Filtro por anos
    st.sidebar.subheader("Ano de lançamento")
    selected_years = st.sidebar.slider(
        "Intervalo de anos:",
        min_value=int(df["Year"].min()),
        max_value=int(df["Year"].max()),
        value=(int(df["Year"].min()), int(df["Year"].max()))
    )

    # Aplicação dos filtros
    df_filtered = df.copy()
    df_filtered = df_filtered[df_filtered["Genre"].isin(selected_genres)]
    df_filtered = df_filtered[df_filtered["Platform"].isin(selected_platforms)]
    df_filtered = df_filtered[df_filtered["Publisher"].isin(selected_publishers)]
    df_filtered = df_filtered[df_filtered["Year"].between(selected_years[0], selected_years[1])]

    return df_filtered


def kpi_section(df):
    """
    Exibe indicadores:
    - Top publisher por vendas
    - Top plataforma
    - Número de publishers únicos
    """

    col1, col2, col3 = st.columns(3)

    # Descobre o publisher com maior soma de vendas
    top_publisher = df.groupby("Publisher")["Total_Sales"].sum().idxmax()
    top_publisher_sales = df.groupby("Publisher")["Total_Sales"].sum().max()

    # Descobre plataforma com maior soma de vendas
    top_platform = df.groupby("Platform")["Total_Sales"].sum().idxmax()
    top_platform_sales = df.groupby("Platform")["Total_Sales"].sum().max()

    unique_publishers = df["Publisher"].nunique()

    with col1:
        st.metric("🏆 Top Publisher", top_publisher, f"{top_publisher_sales:.1f} mi")

    with col2:
        st.metric("🎮 Top Plataforma", top_platform, f"{top_platform_sales:.1f} mi")

    with col3:
        st.metric("🏢 Publishers únicos", unique_publishers)


def top_publishers_chart(df):
    """
    Ranking dos 15 maiores publishers em vendas.
    """

    st.markdown("### 🏢 Top 15 Publishers por vendas globais")

    top_publishers = (
        df.groupby("Publisher")["Total_Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    fig = px.bar(
        top_publishers,
        x="Total_Sales",
        y="Publisher",
        orientation="h",
        title="Top 15 Publishers com maiores vendas",
        color="Total_Sales",
        color_continuous_scale="plasma"
    )

    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def platform_performance_chart(df):
    """
    Mostra a relação entre número de jogos de cada plataforma e vendas totais.
    """

    st.markdown("### 📊 Performance de vendas por plataforma")

    platform_data = df.groupby("Platform").agg({
        "Total_Sales": "sum",
        "Name": "count"
    }).reset_index()

    platform_data.columns = ["Platform", "Total_Sales", "Num_Games"]

    fig = px.scatter(
        platform_data,
        x="Num_Games",
        y="Total_Sales",
        size="Total_Sales",
        color="Total_Sales",
        hover_name="Platform",
        title="Relação entre número de jogos e vendas totais por plataforma"
    )

    st.plotly_chart(fig, use_container_width=True)


def publisher_platform_heatmap(df):
    """
    Gera um heatmap mostrando quais publishers vendem mais em quais plataformas.
    """

    st.markdown("### 🔥 Top Publishers por Plataforma (Heatmap)")

    # Top 10 publishers e plataformas
    top_publishers = df.groupby("Publisher")["Total_Sales"].sum().nlargest(10).index
    top_platforms = df.groupby("Platform")["Total_Sales"].sum().nlargest(10).index

    df_filtered = df[df["Publisher"].isin(top_publishers) & df["Platform"].isin(top_platforms)]

    heatmap_data = df_filtered.groupby(["Publisher", "Platform"])["Total_Sales"] \
                              .sum().reset_index() \
                              .pivot(index="Publisher", columns="Platform", values="Total_Sales") \
                              .fillna(0)

    fig, ax = plt.subplots(figsize=(12, 8))
    im = ax.imshow(heatmap_data.values, cmap="YlOrRd", aspect="auto")

    ax.set_xticks(range(len(heatmap_data.columns)))
    ax.set_yticks(range(len(heatmap_data.index)))
    ax.set_xticklabels(heatmap_data.columns, rotation=45)
    ax.set_yticklabels(heatmap_data.index)

    plt.colorbar(im, ax=ax, label="Vendas (milhões)")
    st.pyplot(fig)


def documentation():
    """
    Aba de documentação explicando como interpretar os gráficos.
    """

    st.markdown("### 📝 Como usar esta página")
    st.markdown("""
        Aqui analisamos os maiores publishers e plataformas do mercado:
        - Quem mais vende
        - Quais plataformas têm mais jogos
        - Heatmap mostrando combinação publisher/plataforma
    """)


def main():
    st.title("🏢 Publishers e Plataformas — Análise de Mercado")

    df = load_data()
    df_filtered = apply_filters(df)

    st.markdown(f"**Total de registros após filtros:** {len(df_filtered)}")

    kpi_section(df_filtered)

    st.markdown("---")

    tab1, tab2 = st.tabs(["📊 Gráficos", "📘 Explicação"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            top_publishers_chart(df_filtered)
        with col2:
            platform_performance_chart(df_filtered)

        st.markdown("---")

        publisher_platform_heatmap(df_filtered)

    with tab2:
        documentation()


if __name__ == "__main__":
    main()
