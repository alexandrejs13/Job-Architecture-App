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
def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ==========================================================
# HEADER — versão centralizada (home)
# ==========================================================
icon_path = "assets/icons/governance.png"
icon_b64 = load_icon_png(icon_path)

st.markdown(f"""
<div style="
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    margin-top:60px;
    margin-bottom:20px;
">
    <img src="data:image/png;base64,{icon_b64}"
         style="width:200px; height:200px; margin-bottom:26px;">
    
    <h1 style="
        font-size:48px;
        font-weight:700;
        margin:0;
        padding:0;
        text-align:center;
    ">
        Job Architecture
    </h1>
</div>
""", unsafe_allow_html=True)

# ==========================================================
# CONTEÚDO OPCIONAL DA HOMEPAGE
# (mantive vazio — a tela vira um splash screen elegante)
# ==========================================================
