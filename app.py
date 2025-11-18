import streamlit as st
import base64
import os

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(page_title="Job Architecture", layout="wide")

# ==========================================================
# FUNÇÃO PARA CARREGAR PNG INLINE
# ==========================================================
def load_icon_png(path: str) -> str:
    """
    Lê um arquivo PNG e retorna seu conteúdo em base64 para uso inline em HTML.
    Se o arquivo não existir, retorna string vazia.
    """
    if not os.path.exists(path):
        st.error(f"Ícone não encontrado no caminho: {path}")
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ==========================================================
# HEADER / TELA INICIAL (CENTRALIZADA)
# ==========================================================
icon_path = "assets/icons/governance.png"
icon_b64 = load_icon_png(icon_path)

html_header = f"""
<div style="
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 0;
">
    <img src="data:image/png;base64,{icon_b64}"
         alt="Job Architecture Icon"
         style="
            width: 180px;
            height: 180px;
            margin-bottom: 24px;
         ">
    <h1 style="
        font-size: 40px;
        font-weight: 700;
        margin: 0;
        padding: 0;
        text-align: center;
    ">
        Job Architecture
    </h1>
</div>
"""

st.markdown(html_header, unsafe_allow_html=True)

# ==========================================================
# Aqui você pode adicionar o restante da lógica da página,
# menus laterais, widgets, etc., conforme o seu app exige.
# ==========================================================
