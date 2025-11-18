# Home - Job Architecture App

import streamlit as st
import base64
import os

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(
    page_title="Job Architecture",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================================
# FUNÇÃO PARA CARREGAR PNG/JPG INLINE (BASE64)
# ==========================================================
def load_image_b64(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# ==========================================================
# CSS GLOBAL SIG
# ==========================================================
css_path = "assets/css/sig_style.css"
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==========================================================
# FONTES PP SIG FLOW
# (caso você tenha utils/font.py, senão posso gerar)
# ==========================================================
try:
    from utils.fonts import load_pp_fonts
    load_pp_fonts()
except:
    pass


# ==========================================================
# IMAGEM DE CAPA — SEM TÍTULO, SEM ÍCONE
# ==========================================================
home_img_path = "assets/home/home_card.jpg"
home_img_b64 = load_image_b64(home_img_path)

st.markdown(
    f"""
    <div class="sig-container" style="margin-top: 12px;">
        <img 
            src="data:image/jpeg;base64,{home_img_b64}" 
            style="width: 100%; max-width: 1400px; display: block; margin: 0 auto; border-radius: 12px;"
        >
    </div>
    """,
    unsafe_allow_html=True,
)
