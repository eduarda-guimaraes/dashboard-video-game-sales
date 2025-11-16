import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Dashboard de Vendas de Games",
    page_icon="🎮",
    layout="wide"
)

CLEAN_PATH = Path("data/vgsales_clean.csv")

@st.cache_data
def load_data():
    df = pd.read_csv(CLEAN_PATH)
    return df

st.title("🎮 Dashboard de Vendas de Video Games")
st.markdown("---")

# Carregar dados para estatísticas
df = load_data()

# Seção de Objetivo
st.header("📋 Objetivo do Dashboard")
st.markdown("""
Este dashboard interativo foi desenvolvido para explorar visualmente um conjunto de dados de **vendas de video games**,
facilitando a descoberta de padrões, tendências e relações no mercado de jogos eletrônicos.

**Dataset:**
- **Fonte:** Kaggle - Video Game Sales Dataset
- **Registros:** Mais de **16.000 jogos** analisados
- **Período:** 1980 a 2025
- **Regiões:** América do Norte (NA), Europa (EU), Japão (JP) e Outras regiões

**Funcionalidades principais:**
- 📊 **Análise inicial** - Visão geral com KPIs e tendências temporais
- 🌍 **Análise regional** - Comparação de vendas entre diferentes regiões
- 🏢 **Análise de Publishers e Plataformas** - Top publishers e performance por plataforma
""")

st.markdown("---")

# Seção de Navegação
st.header("🧭 Como Navegar entre as Seções")
st.markdown("""
Use o **menu lateral** (ícone ☰ no canto superior esquerdo) para navegar entre as diferentes páginas de análise:

1. **🏠 Home** (página atual) - Documentação e visão geral
2. **📈 Análise Inicial** - KPIs, evolução temporal e top gêneros
3. **🌍 Análise Regional** - Comparação de vendas por região geográfica
4. **🏢 Publishers e Plataformas** - Análise de publishers e performance por plataforma

Cada página possui **filtros interativos** na barra lateral que permitem refinar os dados analisados.
""")

st.markdown("---")

# Seção de Filtros
st.header("🔍 Como os Filtros Influenciam os Dados")
st.markdown("""
Todas as páginas de análise possuem **filtros funcionais** na barra lateral que atualizam os gráficos e métricas em tempo real:

### Filtros Disponíveis:

**1. Gênero** 🎯
- Selecione um ou mais gêneros (ex: Action, Sports, RPG)
- Os gráficos mostrarão apenas jogos dos gêneros selecionados
- Útil para comparar performance entre diferentes tipos de jogos

**2. Plataforma** 🎮
- Escolha uma ou mais plataformas (ex: PS4, Xbox, Nintendo Switch)
- Permite analisar tendências específicas de cada console
- Ideal para identificar qual plataforma domina cada gênero

**3. Ano de Lançamento** 📅
- Use o slider para definir um intervalo de anos
- Analise tendências temporais e evolução do mercado
- Identifique períodos de crescimento ou declínio

**4. Publisher** 🏢 (em algumas páginas)
- Filtre por editoras específicas
- Compare performance entre diferentes empresas
- Identifique líderes de mercado

### Como Funciona:
- Os filtros são **combinados** (AND lógico) - todos os critérios devem ser atendidos
- Os gráficos e métricas são **atualizados automaticamente** quando você altera qualquer filtro
- Os KPIs no topo de cada página refletem os dados **após a aplicação dos filtros**
- Você pode **limpar seleções** para voltar a ver todos os dados
""")

st.markdown("---")

# Estatísticas Gerais
st.header("📊 Estatísticas Gerais do Dataset")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Jogos", f"{len(df):,}".replace(",", "."))

with col2:
    st.metric("Total de Vendas (mi)", f"{df['Total_Sales'].sum():.1f}")

with col3:
    st.metric("Gêneros Únicos", df['Genre'].nunique())

with col4:
    st.metric("Plataformas Únicas", df['Platform'].nunique())

st.markdown("---")

# Informações sobre Gráficos
st.header("📈 Sobre os Gráficos")
st.markdown("""
Este dashboard contém **mais de 6 gráficos interativos e estáticos**, incluindo:

- ✅ **Gráficos Interativos com Plotly** - Zoom, pan, hover para detalhes
- ✅ **Gráficos Estáticos com Matplotlib** - Visualizações rápidas e limpas
- ✅ **Visualizações por Região** - Comparação geográfica de vendas
- ✅ **Análises Temporais** - Evolução ao longo dos anos
- ✅ **Rankings e Top Lists** - Melhores performers em diferentes categorias
- ✅ **Distribuições e Comparações** - Padrões e relações entre variáveis

**Dica:** Passe o mouse sobre os gráficos interativos para ver informações detalhadas de cada ponto!
""")

st.markdown("---")
st.info("💡 **Dica:** Comece pela página 'Análise Inicial' para ter uma visão geral dos dados antes de explorar análises mais específicas.")