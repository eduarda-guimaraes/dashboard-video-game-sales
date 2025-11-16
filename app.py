import streamlit as st

st.set_page_config(
    page_title="Dashboard de Vendas de Games",
    page_icon="🎮",
    layout="wide"
)

st.title("🎮 Dashboard de Vendas de Video Games")

st.markdown("""
Bem-vindo ao **Dashboard de Vendas de Video Games**!

Use o menu lateral para navegar entre as páginas.

Este dashboard analisa um dataset com **mais de 16.000 registros** de jogos,
incluindo:

- Vendas globais  
- Gêneros  
- Plataformas  
- Evolução das vendas ao longo dos anos  

Cada integrante da equipe é responsável por uma página de análise dentro do projeto.
""")