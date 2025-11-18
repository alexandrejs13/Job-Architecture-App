import streamlit as st
import base64
import os

# ==========================================================
# CONFIG GERAL — mesmo padrão das demais páginas
# ==========================================================
st.set_page_config(
    page_title="Job Architecture",
    layout="wide",
)

# ==========================================================
# APLICA CSS GLOBAL (layout_global.css) — fonte PPSIGFlow + sidebar
# ==========================================================
def load_global_css(path: str):
    """Carrega o CSS global para aplicar fonte PPSIGFlow e layout padrão."""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# caminho relativo dentro do projeto
css_path = os.path.join("assets", "css", "layout_global.css")
load_global_css(css_path)

# ==========================================================
# FUNÇÃO PARA CARREGAR IMAGEM INLINE (hero)
# ==========================================================
def load_image_b64(path: str) -> str:
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ==========================================================
# HERO IMAGE — primeira coisa da página (sem título/ícone antes)
# ==========================================================
hero_path = os.path.join("assets", "home", "home_card.jpg")
hero_b64 = load_image_b64(hero_path)

if hero_b64:
    st.markdown(
        f"""
        <div style="
            display: flex;
            justify-content: center;
            margin-top: 10px;
            margin-bottom: 30px;
        ">
            <img 
                src="data:image/jpg;base64,{hero_b64}" 
                style="
                    width: 100%;
                    max-width: 1100px;
                    border-radius: 28px;  /* cantos mais arredondados */
                    display: block;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
                "
            >
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    # fallback simples caso a imagem não seja encontrada
    st.warning("Imagem de capa não encontrada em 'assets/home/home_card.jpg'.")

# ==========================================================
# TÍTULO + TEXTO — usando fonte PPSIGFlow (já registrada no CSS)
# ==========================================================
st.markdown(
    """
    <h1 style="
        font-family: 'PPSIGFlow';
        font-size: 40px;
        font-weight: 600;
        margin-bottom: 10px;
        color: #000;
    ">
        Job Architecture
    </h1>

    <p style="
        font-family: 'PPSIGFlow';
        font-size: 18px;
        font-weight: 400;
        line-height: 1.6;
        max-width: 900px;
        color: #000;
    ">
        Bem-vindo ao portal de Job Architecture. Aqui você encontra as estruturas organizadas 
        de famílias de cargos, perfis de posição, níveis, responsabilidades e competências 
        essenciais para garantir consistência, governança e alinhamento global.
        <br><br>
        Explore as seções ao lado para navegar por famílias, perfis, comparações, dashboards 
        e muito mais — tudo com a identidade visual SIG e uma experiência totalmente integrada.
    </p>
    """,
    unsafe_allow_html=True,
)
