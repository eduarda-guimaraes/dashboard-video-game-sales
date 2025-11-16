import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from pathlib import Path

# Define o caminho do arquivo CSV já limpo
CLEAN_PATH = Path("data/vgsales_clean.csv")

st.set_page_config(
    page_title="Dashboard de Vendas de Games",
    page_icon="🎮",
    layout="wide"
)

@st.cache_data
def load_data():
    """
    Carrega o dataset de vendas a partir do arquivo CSV.
    O cache evita recarregar o dataset a cada refresh da página.
    """
    df = pd.read_csv(CLEAN_PATH)
    return df


def apply_filters(df):
    """
    Cria e aplica os filtros da barra lateral:
    - Gênero
    - Plataforma
    - Intervalo de anos
    Retorna um DataFrame já filtrado.
    """

    st.sidebar.title("Filtros")
    st.sidebar.markdown("Ajuste os filtros abaixo para atualizar os gráficos em tempo real.")

    # Filtro de gênero
    st.sidebar.subheader("Gênero")
    genres = sorted(df["Genre"].unique())
    selected_genres = st.sidebar.multiselect(
        "Selecione os gêneros:",
        options=genres,
        default=genres,  # Começa com todos selecionados
    )

    # Filtro de plataforma
    st.sidebar.subheader("Plataforma")
    platforms = sorted(df["Platform"].unique())
    selected_platforms = st.sidebar.multiselect(
        "Selecione as plataformas:",
        options=platforms,
        default=platforms,
    )

    # Filtro por intervalo de anos
    st.sidebar.subheader("Ano de lançamento")
    year_min = int(df["Year"].min())  # menor ano disponível
    year_max = int(df["Year"].max())  # maior ano disponível

    selected_years = st.sidebar.slider(
        "Intervalo de anos:",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max),  # valor inicial = tudo
    )

    # Cria uma cópia para não alterar o df original
    df_filtered = df.copy()
    # Aplica filtros de gênero, plataforma e ano
    df_filtered = df_filtered[df_filtered["Genre"].isin(selected_genres)]
    df_filtered = df_filtered[df_filtered["Platform"].isin(selected_platforms)]
    df_filtered = df_filtered[df_filtered["Year"].between(selected_years[0], selected_years[1])]

    return df_filtered


def kpi_section(df):
    """
    Exibe 3 indicadores principais (KPIs) com base no DataFrame filtrado:
    - Quantidade de jogos
    - Soma das vendas globais
    - Número de gêneros únicos
    """
    col1, col2, col3 = st.columns(3)

    total_games = len(df)
    total_sales = df["Total_Sales"].sum()
    unique_genres = df["Genre"].nunique()

    # Exibição da métrica 1
    with col1:
        st.metric(
            label="🎮 Jogos no filtro",
            value=f"{total_games:,}".replace(",", "."),
            help="Quantidade de registros (jogos) após os filtros."
        )

    # Exibição da métrica 2
    with col2:
        st.metric(
            label="💰 Vendas globais (mi)",
            value=f"{total_sales:.1f}",
            help="Soma das vendas globais em milhões (NA, EU, JP e outros)."
        )

    # Exibição da métrica 3
    with col3:
        st.metric(
            label="📂 Gêneros únicos",
            value=str(unique_genres),
            help="Número de gêneros diferentes presentes no filtro atual."
        )


def static_chart(df):
    """
    Gráfico estático (Matplotlib) mostrando o Top 5 gêneros por vendas globais.
    """
    st.markdown("### 🎮 Top 5 gêneros por vendas globais (gráfico estático)")

    # Agrupa por gênero, soma vendas e pega top 5
    top_genres = (
        df.groupby("Genre")["Total_Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    # Cria o gráfico de barras com Matplotlib
    fig, ax = plt.subplots()
    top_genres.plot(kind="bar", ax=ax, color="skyblue")

    ax.set_title("Top 5 gêneros com maiores vendas globais")
    ax.set_xlabel("Gênero")
    ax.set_ylabel("Vendas globais (milhões)")

    st.pyplot(fig)


def interactive_chart(df):
    """
    Gráfico interativo (Plotly)
    Mostra a evolução das vendas globais ao longo dos anos.
    """

    st.markdown("### 📈 Evolução das vendas globais ao longo dos anos (gráfico interativo)")

    # Agrupamento por ano
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


def interactive_chart_genres(df):
    """
    Gráfico interativo de barras mostrando a soma de vendas por gênero.
    """

    st.markdown("### 🎯 Distribuição de vendas por gênero (gráfico interativo)")

    # Soma das vendas por gênero
    genre_sales = (
        df.groupby("Genre")["Total_Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    # Cria o gráfico de barras com Plotly
    fig = px.bar(
        genre_sales,
        x="Genre",
        y="Total_Sales",
        labels={
            "Genre": "Gênero",
            "Total_Sales": "Vendas globais (milhões)"
        },
        title="Vendas totais por gênero",
        color="Total_Sales",
        color_continuous_scale="viridis"
    )

    # Inclina os rótulos no eixo X para melhor leitura
    fig.update_xaxes(tickangle=45)  # Deixa os nomes inclinados para não sobrepor
    fig.update_layout(showlegend=False)

    st.plotly_chart(fig, use_container_width=True)


def static_chart_platforms(df):
    """
    Gráfico estático (Matplotlib) mostrando o Top 10 de plataformas em vendas.
    """

    st.markdown("### 🎮 Top 10 plataformas por vendas (gráfico estático)")

    top_platforms = (
        df.groupby("Platform")["Total_Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    top_platforms.plot(kind="barh", ax=ax, color="coral")
    
    ax.set_title("Top 10 plataformas com maiores vendas globais", fontsize=14, fontweight="bold")
    ax.set_xlabel("Vendas globais (milhões)", fontsize=12)
    ax.set_ylabel("Plataforma", fontsize=12)
    ax.invert_yaxis()  # Maior valor fica no topo
    
    plt.tight_layout()
    st.pyplot(fig)


def documentation():
    """
    Aba explicativa da página.
    Mostra como interpretar os gráficos e usar os filtros.
    """

    st.markdown("### 📝 Como usar esta página")

    st.markdown(
        """
        **Objetivo da página**
        Esta página apresenta uma análise inicial das vendas de video games, respondendo:

        - Quais são os gêneros mais vendidos?
        - Como as vendas evoluíram ao longo do tempo?
        - Como os filtros afetam os resultados?

        **Como navegar**
        - Use a barra lateral para filtrar os dados.
        - Veja os KPIs no topo.
        - Navegue pelas abas para gráficos e explicação.
        """
    )


def main():
    """
    Função principal da página.
    Monta toda a interface da Análise Inicial.
    """

    st.title("🎮 Análise Inicial — Vendas de Video Games")
    st.caption("Exploração geral do dataset de vendas globais de jogos, com filtros interativos.")

    # Carrega dados e aplica filtros
    df = load_data()
    df_filtered = apply_filters(df)

    # Mostra quantidade de registros filtrados
    st.markdown(f"**Total de registros após filtros:** {len(df_filtered)}")

    # Exibe KPIs
    kpi_section(df_filtered)

    st.markdown("---")

    # Abas da página
    tab1, tab2 = st.tabs(["📊 Gráficos", "📘 Explicação"])

    with tab1:
        # Primeira linha: gráficos interativos
        st.markdown("#### Gráficos Interativos")
        col1, col2 = st.columns(2)

        with col1:
            interactive_chart(df_filtered)
        with col2:
            interactive_chart_genres(df_filtered)

        st.markdown("---")

        # Segunda linha: gráficos estáticos
        st.markdown("#### Gráficos Estáticos")
        col3, col4 = st.columns(2)

        with col3:
            static_chart(df_filtered)
        with col4:
            static_chart_platforms(df_filtered)

    with tab2:
        documentation()


# Execução direta do arquivo
if __name__ == "__main__":
    main()
