import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
    col1, col2, col3, col4 = st.columns(4)

    na_sales = df["NA_Sales"].sum()
    eu_sales = df["EU_Sales"].sum()
    jp_sales = df["JP_Sales"].sum()
    other_sales = df["Other_Sales"].sum()

    with col1:
        st.metric(
            label="🇺🇸 Vendas NA (mi)",
            value=f"{na_sales:.1f}",
            help="Vendas na América do Norte em milhões."
        )

    with col2:
        st.metric(
            label="🇪🇺 Vendas EU (mi)",
            value=f"{eu_sales:.1f}",
            help="Vendas na Europa em milhões."
        )

    with col3:
        st.metric(
            label="🇯🇵 Vendas JP (mi)",
            value=f"{jp_sales:.1f}",
            help="Vendas no Japão em milhões."
        )

    with col4:
        st.metric(
            label="🌍 Outras Regiões (mi)",
            value=f"{other_sales:.1f}",
            help="Vendas em outras regiões em milhões."
        )


def regional_comparison_chart(df):
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
        labels={"Vendas (milhões)": "Vendas (milhões)"},
        title="Comparação de vendas por região geográfica"
    )
    
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    st.caption(
        "Este gráfico compara as vendas totais entre as diferentes regiões geográficas. "
        "Passe o mouse sobre as barras para ver valores detalhados."
    )


def regional_evolution_chart(df):
    st.markdown("### 📈 Evolução das vendas por região ao longo dos anos (gráfico interativo)")
    
    df_yearly = df.groupby("Year").agg({
        "NA_Sales": "sum",
        "EU_Sales": "sum",
        "JP_Sales": "sum",
        "Other_Sales": "sum"
    }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_yearly["Year"],
        y=df_yearly["NA_Sales"],
        mode="lines+markers",
        name="América do Norte",
        line=dict(color="#1f77b4", width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=df_yearly["Year"],
        y=df_yearly["EU_Sales"],
        mode="lines+markers",
        name="Europa",
        line=dict(color="#ff7f0e", width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=df_yearly["Year"],
        y=df_yearly["JP_Sales"],
        mode="lines+markers",
        name="Japão",
        line=dict(color="#2ca02c", width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=df_yearly["Year"],
        y=df_yearly["Other_Sales"],
        mode="lines+markers",
        name="Outras Regiões",
        line=dict(color="#d62728", width=3)
    ))
    
    fig.update_layout(
        title="Evolução das vendas por região ao longo dos anos",
        xaxis_title="Ano",
        yaxis_title="Vendas (milhões)",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.caption(
        "Este gráfico mostra como as vendas evoluíram em cada região ao longo do tempo. "
        "Use a legenda para mostrar/ocultar regiões específicas."
    )


def regional_pie_chart(df):
    st.markdown("### 🥧 Distribuição percentual de vendas por região (gráfico interativo)")
    
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
        title="Distribuição percentual de vendas por região",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Vendas: %{value:.2f} milhões<br>Percentual: %{percent}<extra></extra>"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.caption(
        "Este gráfico de pizza mostra a proporção de vendas de cada região em relação ao total. "
        "Clique nas fatias da legenda para destacar regiões específicas."
    )


def documentation():
    st.markdown("### 📝 Como usar esta página")
    
    st.markdown("""
**Objetivo da página**

Esta página apresenta uma **análise regional** das vendas de video games, permitindo comparar o desempenho
de vendas entre diferentes regiões geográficas:

- **América do Norte (NA)**: Estados Unidos e Canadá
- **Europa (EU)**: Países europeus
- **Japão (JP)**: Mercado japonês
- **Outras Regiões**: Resto do mundo

**Gráficos disponíveis**

1. **Comparação de vendas por região** - Gráfico de barras mostrando vendas totais de cada região
2. **Evolução temporal por região** - Linha do tempo mostrando como cada região evoluiu ao longo dos anos
3. **Distribuição percentual** - Gráfico de pizza mostrando a proporção de cada região

**Como os filtros influenciam**

- **Gênero**: Compare quais gêneros são mais populares em cada região
- **Plataforma**: Veja como diferentes consoles performam em cada mercado
- **Ano**: Analise tendências temporais e mudanças nas preferências regionais

**Insights possíveis**

- Identifique qual região é o maior mercado para determinado gênero ou plataforma
- Observe mudanças nas preferências regionais ao longo do tempo
- Compare a evolução de cada mercado (crescimento, declínio, estabilidade)
    """)


def main():
    st.title("🌍 Análise Regional — Vendas de Video Games")
    st.caption("Comparação de vendas entre diferentes regiões geográficas com visualizações interativas.")
    
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

