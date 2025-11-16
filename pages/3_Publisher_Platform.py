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

    st.sidebar.subheader("Publisher")
    publishers = sorted(df["Publisher"].unique())
    selected_publishers = st.sidebar.multiselect(
        "Selecione os publishers:",
        options=publishers,
        default=publishers,
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
    df_filtered = df_filtered[df_filtered["Publisher"].isin(selected_publishers)]
    df_filtered = df_filtered[df_filtered["Year"].between(selected_years[0], selected_years[1])]

    return df_filtered


def kpi_section(df):
    col1, col2, col3 = st.columns(3)

    top_publisher = df.groupby("Publisher")["Total_Sales"].sum().idxmax()
    top_publisher_sales = df.groupby("Publisher")["Total_Sales"].sum().max()
    
    top_platform = df.groupby("Platform")["Total_Sales"].sum().idxmax()
    top_platform_sales = df.groupby("Platform")["Total_Sales"].sum().max()
    
    unique_publishers = df["Publisher"].nunique()

    with col1:
        st.metric(
            label="🏆 Top Publisher",
            value=top_publisher[:20] + "..." if len(top_publisher) > 20 else top_publisher,
            delta=f"{top_publisher_sales:.1f} mi",
            help="Publisher com maior volume de vendas."
        )

    with col2:
        st.metric(
            label="🎮 Top Plataforma",
            value=top_platform,
            delta=f"{top_platform_sales:.1f} mi",
            help="Plataforma com maior volume de vendas."
        )

    with col3:
        st.metric(
            label="🏢 Publishers únicos",
            value=str(unique_publishers),
            help="Número de publishers diferentes presentes no filtro atual."
        )


def top_publishers_chart(df):
    st.markdown("### 🏢 Top 15 Publishers por vendas globais (gráfico interativo)")
    
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
        color="Total_Sales",
        color_continuous_scale="plasma",
        labels={
            "Total_Sales": "Vendas globais (milhões)",
            "Publisher": "Publisher"
        },
        title="Top 15 Publishers com maiores vendas"
    )
    
    fig.update_layout(
        showlegend=False,
        yaxis={"categoryorder": "total ascending"}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.caption(
        "Este gráfico mostra os 15 publishers com maiores vendas globais. "
        "Passe o mouse sobre as barras para ver valores detalhados."
    )


def platform_performance_chart(df):
    st.markdown("### 📊 Performance de vendas por plataforma (gráfico interativo)")
    
    platform_data = (
        df.groupby("Platform")
        .agg({
            "Total_Sales": "sum",
            "Name": "count"
        })
        .reset_index()
    )
    platform_data.columns = ["Platform", "Total_Sales", "Num_Games"]
    
    fig = px.scatter(
        platform_data,
        x="Num_Games",
        y="Total_Sales",
        size="Total_Sales",
        color="Total_Sales",
        hover_name="Platform",
        color_continuous_scale="viridis",
        labels={
            "Num_Games": "Número de Jogos",
            "Total_Sales": "Vendas Globais (milhões)",
            "Platform": "Plataforma"
        },
        title="Relação entre número de jogos e vendas totais por plataforma",
        size_max=50
    )
    
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>" +
                      "Jogos: %{x}<br>" +
                      "Vendas: %{y:.2f} milhões<extra></extra>"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.caption(
        "Este gráfico de dispersão mostra a relação entre o número de jogos lançados e as vendas totais. "
        "O tamanho das bolhas representa o volume de vendas. Passe o mouse para ver detalhes."
    )


def publisher_platform_heatmap(df):
    st.markdown("### 🔥 Top Publishers por Plataforma (gráfico estático)")
    
    # Pegar top 10 publishers e top 10 plataformas
    top_publishers = df.groupby("Publisher")["Total_Sales"].sum().nlargest(10).index.tolist()
    top_platforms = df.groupby("Platform")["Total_Sales"].sum().nlargest(10).index.tolist()
    
    df_filtered = df[df["Publisher"].isin(top_publishers) & df["Platform"].isin(top_platforms)]
    
    heatmap_data = (
        df_filtered.groupby(["Publisher", "Platform"])["Total_Sales"]
        .sum()
        .reset_index()
        .pivot(index="Publisher", columns="Platform", values="Total_Sales")
        .fillna(0)
    )
    
    fig, ax = plt.subplots(figsize=(12, 8))
    im = ax.imshow(heatmap_data.values, cmap="YlOrRd", aspect="auto")
    
    ax.set_xticks(range(len(heatmap_data.columns)))
    ax.set_yticks(range(len(heatmap_data.index)))
    ax.set_xticklabels(heatmap_data.columns, rotation=45, ha="right")
    ax.set_yticklabels(heatmap_data.index)
    
    ax.set_title("Heatmap: Vendas por Publisher e Plataforma", fontsize=14, fontweight="bold", pad=20)
    ax.set_xlabel("Plataforma", fontsize=12)
    ax.set_ylabel("Publisher", fontsize=12)
    
    # Adicionar valores no heatmap
    for i in range(len(heatmap_data.index)):
        for j in range(len(heatmap_data.columns)):
            text = ax.text(j, i, f"{heatmap_data.iloc[i, j]:.1f}",
                          ha="center", va="center", color="black", fontsize=8)
    
    plt.colorbar(im, ax=ax, label="Vendas (milhões)")
    plt.tight_layout()
    st.pyplot(fig)
    
    st.caption(
        "Este heatmap mostra as vendas combinadas dos top 10 publishers nas top 10 plataformas. "
        "Cores mais escuras indicam maiores volumes de vendas."
    )


def documentation():
    st.markdown("### 📝 Como usar esta página")
    
    st.markdown("""
**Objetivo da página**

Esta página apresenta uma **análise de Publishers e Plataformas**, explorando:

- Quais publishers dominam o mercado de video games
- Como diferentes plataformas performam em termos de vendas
- A relação entre número de jogos lançados e vendas totais
- Quais publishers são mais fortes em cada plataforma

**Gráficos disponíveis**

1. **Top 15 Publishers** - Ranking dos maiores publishers por vendas globais
2. **Performance por Plataforma** - Gráfico de dispersão mostrando relação entre número de jogos e vendas
3. **Heatmap Publisher x Plataforma** - Matriz de calor mostrando vendas combinadas

**Como os filtros influenciam**

- **Gênero**: Veja quais publishers/plataformas dominam cada gênero
- **Plataforma**: Analise publishers específicos em plataformas selecionadas
- **Publisher**: Compare performance de publishers específicos
- **Ano**: Observe mudanças no mercado ao longo do tempo

**Insights possíveis**

- Identifique publishers dominantes e suas estratégias de mercado
- Compare eficiência de vendas (muitos jogos vs. poucos jogos com alta venda)
- Descubra sinergias entre publishers e plataformas específicas
- Analise concentração de mercado e competição
    """)


def main():
    st.title("🏢 Publishers e Plataformas — Análise de Mercado")
    st.caption("Análise detalhada de publishers e plataformas com visualizações interativas e estáticas.")
    
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

