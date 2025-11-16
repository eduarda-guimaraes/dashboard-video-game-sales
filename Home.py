import streamlit as st
import pandas as pd
from pathlib import Path

# Configurações da aplicação
st.set_page_config(
    page_title="Dashboard de Vendas de Games",
    page_icon="🎮",
    layout="wide"
)

# Caminho do dataset
CLEAN_PATH = Path("data/vgsales_clean.csv")

@st.cache_data
def load_data():
    """Carrega o dataset com cache para performance."""
    return pd.read_csv(CLEAN_PATH)

st.title("🎮 Dashboard de Vendas de Video Games")
st.markdown("---")

# Carrega os dados para usar nas estatísticas gerais da Home
df = load_data()

# Objetivo
st.header("🎯 Objetivo do Dashboard")
st.markdown("""
Este dashboard interativo foi criado para **explorar e visualizar o mercado global de video games**,
permitindo identificar:
- Tendências ao longo dos anos  
- Diferenças regionais de mercado  
- Publishers e plataformas mais relevantes  
- Destaques por gênero e tipo de jogo  

Ele transforma dados brutos em **informações claras, visuais e fáceis de interpretar**.
""")

st.markdown("---")

# Navegação
st.header("🧭 Como Navegar entre as Seções")
st.markdown("""
Use o **menu lateral** no canto esquerdo para acessar cada parte da análise:

### **📌 Seções disponíveis**
- **🏠 Home** — Você está aqui. Uma visão geral e explicação do dashboard.  
- **📈 Análise Inicial** — KPIs, evolução temporal e gêneros mais vendidos.  
- **🌍 Análise Regional** — Comparação de vendas entre NA, EU, JP e Outras regiões.  
- **🏢 Análise de Mercado** — Ranking de publishers e performance por console.  

Cada seção aprofunda um aspecto diferente do mercado.
""")

st.markdown("---")

# Filtros
st.header("🔍 Como os Filtros Influenciam os Dados")
st.markdown("""
As páginas internas possuem filtros na barra lateral que **atualizam os gráficos automaticamente**.

### **Filtros disponíveis**
- 🎮 **Plataforma** (PS4, Xbox One, Wii, etc.)  
- 🎯 **Gênero** (Action, Sports, RPG, etc.)  
- 🏢 **Publisher** (Nintendo, EA, Ubisoft…)  
- 📅 **Ano de lançamento** (slider por período)

### **Como funcionam**
- Os filtros funcionam **em conjunto** (combinação lógica AND).  
- Cada gráfico exibe apenas os jogos que atendem *todos* os filtros selecionados.  
- Os KPIs de cada página também são recalculados automaticamente.

Isso permite uma análise **totalmente personalizada**.
""")

st.markdown("---")

# Estatísticas gerais
st.header("📊 Estatísticas Gerais do Dataset")
# Cria 4 colunas lado a lado para mostrar métricas
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Número total de registros (jogos) no dataset completo
    st.metric("Total de Jogos", f"{len(df):,}".replace(",", "."))

with col2:
    # Soma total das vendas globais (Total_Sales)
    st.metric("Total de Vendas (mi)", f"{df['Total_Sales'].sum():.1f}")

with col3:
    # Quantidade de gêneros diferentes
    st.metric("Gêneros Únicos", df['Genre'].nunique())

with col4:
    # Quantidade de plataformas diferentes
    st.metric("Plataformas Únicas", df['Platform'].nunique())

st.markdown("---")

# Dica final
st.info("💡 **Dica:** Comece pela aba *Análise Inicial* para ter uma visão geral antes de explorar as demais seções.")
