import streamlit as st

# Configuração da página para o menu lateral (usando ícone Lucide)
st.set_page_config(
    page_title="Job Architecture", 
    layout="wide",
    # Usando o ícone Lucide/Streamlit para o menu lateral
    # O Streamlit não suporta PNGs diretamente no menu lateral
    icon="briefcase" 
)

# Ícone PNG no título da página (usando HTML/Markdown para controle de tamanho)
# O ícone PNG deve estar no diretório 'icons/'
st.markdown(
    """
    <style>
    .page-title-container {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .page-title-icon {
        height: 1.2em; /* Ajusta o tamanho do ícone para a proporção da fonte */
        width: auto;
        vertical-align: middle;
    }
    </style>
    <div class="page-title-container">
        <img src="icons/governance.png" class="page-title-icon">
        <h1>Job Architecture</h1>
    </div>
    """, 
    unsafe_allow_html=True
)

st.write("Page: Job Architecture")
