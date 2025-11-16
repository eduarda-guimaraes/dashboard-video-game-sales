# 🎮 Dashboard de Vendas de Video Games

Dashboard interativo desenvolvido com Streamlit para explorar visualmente um conjunto de dados de vendas de video games, facilitando a descoberta de padrões, tendências e relações no mercado de jogos eletrônicos.

## 📊 Dataset

- **Fonte:** Kaggle - Video Game Sales Dataset
- **Registros:** Mais de 16.000 jogos
- **Período:** 1980 a 2025
- **Regiões:** América do Norte (NA), Europa (EU), Japão (JP) e Outras regiões

## 🚀 Instruções de Execução

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd dashboard-video-game-sales
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o script de limpeza de dados (se necessário):
```bash
python clean_data.py
```

5. Execute o dashboard:
```bash
streamlit run app.py
```

O dashboard será aberto automaticamente no seu navegador em `http://localhost:8501`

## 📁 Estrutura do Projeto

```
dashboard-video-game-sales/
├── app.py                      # Página principal (Home)
├── clean_data.py              # Script de limpeza de dados
├── requirements.txt           # Dependências do projeto
├── README.md                  # Este arquivo
├── data/
│   ├── vgsales_raw.csv        # Dados brutos
│   └── vgsales_clean.csv      # Dados limpos
└── pages/
    ├── 1_Initial_Analysis.py   # Análise inicial
    ├── 2_Regional_Analysis.py  # Análise regional
    └── 3_Publisher_Platform.py # Análise de publishers e plataformas
```

## 🌐 Publicação no Streamlit Cloud

### Passo a passo:

1. **Crie uma conta no Streamlit Cloud:**
   - Acesse [share.streamlit.io](https://share.streamlit.io)
   - Faça login com sua conta GitHub

2. **Conecte seu repositório:**
   - Clique em "New app"
   - Selecione o repositório do GitHub
   - Escolha o branch (geralmente `main` ou `master`)

3. **Configure o app:**
   - **Main file path:** `app.py`
   - **Python version:** 3.8 ou superior
   - O Streamlit Cloud detectará automaticamente o `requirements.txt`

4. **Deploy:**
   - Clique em "Deploy"
   - Aguarde o processo de build e deploy
   - Seu dashboard estará disponível em uma URL pública

### Arquivos necessários no repositório:

- ✅ `app.py` (arquivo principal)
- ✅ `requirements.txt` (dependências)
- ✅ `data/vgsales_clean.csv` (dados)
- ✅ Pasta `pages/` com as páginas de análise

## 📈 Funcionalidades

### Páginas Disponíveis:

1. **🏠 Home** - Documentação completa, objetivo do dashboard e instruções de uso
2. **📊 Análise Inicial** - KPIs, evolução temporal, top gêneros e plataformas (4 gráficos)
3. **🌍 Análise Regional** - Comparação de vendas entre regiões (3 gráficos interativos)
4. **🏢 Publishers e Plataformas** - Análise de mercado e performance (3 gráficos)

### Gráficos:

- ✅ **6+ gráficos** no total
- ✅ **2+ gráficos interativos** com Plotly (zoom, pan, hover)
- ✅ **Gráficos estáticos** com Matplotlib
- ✅ **Filtros funcionais** que atualizam todos os gráficos em tempo real

### Filtros Disponíveis:

- 🎯 **Gênero** - Selecione um ou mais gêneros
- 🎮 **Plataforma** - Escolha uma ou mais plataformas
- 📅 **Ano de Lançamento** - Intervalo de anos com slider
- 🏢 **Publisher** - Filtre por editoras (em algumas páginas)

## 🛠️ Tecnologias Utilizadas

- **Streamlit** - Framework para criação de dashboards interativos
- **Pandas** - Manipulação e análise de dados
- **Plotly** - Gráficos interativos
- **Matplotlib** - Gráficos estáticos

## 📝 Licença

Este projeto é de uso educacional e acadêmico.

## 👥 Autores

Desenvolvido como projeto de dashboard interativo para análise de dados.

