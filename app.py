import streamlit as st
import base64
import os
from pathlib import Path

# ==========================================================
# CONFIG GERAL
# ==========================================================
st.set_page_config(
    page_title="Job Architecture",
    layout="wide",
)

BASE_DIR = Path(__file__).parent

# ==========================================================
# CSS GLOBAL SIG (MESMO DAS OUTRAS PÁGINAS)
# ==========================================================
css_path = BASE_DIR / "assets" / "css" / "layout_global.css"

if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# ==========================================================
# FUNÇÃO PARA CARREGAR IMAGEM EM BASE64
# ==========================================================
def load_image_base64(path: Path) -> str:
    if not path.exists():
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ==========================================================
# HERO IMAGE – MESMA LARGURA DO CONTEÚDO
# ==========================================================
hero_path = BASE_DIR / "assets" / "home" / "home_card.jpg"
hero_b64 = load_image_base64(hero_path)

if hero_b64:
    st.markdown(
        f"""
        <div style="
            max-width: 1100px;
            margin: 32px auto 0 auto;
        ">
            <img 
                src="data:image/jpeg;base64,{hero_b64}" 
                alt="Job Architecture" 
