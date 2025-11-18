import streamlit as st
import base64
import os

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(page_title="Job Architecture", layout="wide")

# ==========================================================
# FUNÇÃO PARA CARREGAR PNG INLINE (Verificação de caminho)
# ==========================================================
def load_icon_png(path):
    # ATENÇÃO: Verifique se o caminho 'assets/icons/governance.png' é 
    # relativo ao seu arquivo 'app.py' E se ele foi commitado no Git.
    if not os.path.exists(path):
        # Para debug no Streamlit Cloud, você pode adicionar um log:
        # st.error(f"Arquivo não encontrado: {path}. Verifique o caminho e o Git.")
        return ""
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        # st.error(f"Erro ao ler o arquivo: {e}")
        return ""

# ==========================================================
# ICON PATH
# ==========================================================
icon_path = "assets/icons/governance.png"
icon_b64 = load_icon_png(icon_path)

# ==========================================================
# HTML DA TELA INICIAL (Reordenado para Título -> Logo -> Subtítulo)
# ==========================================================
html = f"""
<style>
/* ... suas definições de @font-face ... */

@font-face {{
    font-family: 'SIGFlowBold';
    src: url('assets/css/fonts/PPSIGFlow-Bold.otf') format('opentype');
    font-weight: bold;
}}

@font-face {{
    font-family: 'SIGFlowRegular';
    src: url('assets/css/fonts/PPSIGFlow-Regular.otf') format('opentype');
    font-weight: normal;
}}

h1.sig-title {{
    font-family: 'SIGFlowBold', sans-serif;
    /* Extra grande - 64px */
    font-size: 64px; 
    margin: 0px;
    padding: 0px;
    text-align: center;
}}

p.sig-subtitle {{
    font-family: 'SIGFlowRegular', sans-serif;
    /* Subtítulo regular - 20px */
    font-size: 20px; 
    margin-top: 20px; /* Ajuste o espaçamento superior se necessário */
    color: #555;
    text-align: center;
    max-width: 800px;
}}
/* Novo estilo para o container do logo */
.governance-logo {{
    margin-top: 28px; /* Espaço extra abaixo do Título/Logo */
    text-align: center;
}}
</style>

<div style="
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:flex-start;
    height:100vh;
    padding-top:40px;
">

    <h1 class="sig-title">Job Architecture</h1>
    
    <div class="governance-logo">
        <img src="data:image/png;base64,{icon_b64}"
             style="width:260px;"> 
    </div>

    <p class="sig-subtitle">
        A global job framework designed to standardize governance and harmonize roles across the organization.
    </p>
    

</div>
"""

st.markdown(html, unsafe_allow_html=True)
