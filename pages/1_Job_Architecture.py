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
# HEADER — padrão SIG (igual todas as páginas)
# ==========================================================
icon_path = "assets/icons/governance.png"
icon_b64 = load_icon_png(icon_path)

st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:12px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">
        Job Architecture
    </h1>
</div>

<hr style="margin-top:14px; margin-bottom:26px;">
""", unsafe_allow_html=True)

# ==========================================================
# CSS E BLOCO CENTRAL
# ==========================================================
html = f"""
<style>
@font-face {{
    font-family: 'SIGFlowBold';
    src: url('assets/css/fonts/PPSIGFlow-Bold.otf') format('opentype');
}}

@font-face {{
    font-family: 'SIGFlowRegular';
    src: url('assets/css/fonts/PPSIGFlow-Regular.otf') format('opentype');
}}

h1.sig-title {{
    font-family: 'SIGFlowBold', sans-serif;
    font-size: 52px;
    text-align: center;
    margin: 0;
}}

p.sig-subtitle {{
    font-family: 'SIGFlowRegular', sans-serif;
    font-size: 20px;
    color: #555;
    text-align: center;
    max-width: 900px;
    margin: 14px auto 0 auto;
    line-height: 1.45;
}}
</style>

<div style="text-align:center; padding-top:20px;">

    <h1 class="sig-title">O que é Job Architecture?</h1>

    <p class="sig-subtitle">
        Job Architecture é a estrutura que organiza todos os cargos da empresa de forma clara, lógica e comparável. 
        Ela define famílias, níveis, escopos e critérios objetivos que diferenciam cada papel, permitindo consistência 
        global na classificação e avaliação das funções. Essa organização cria um padrão único para entender senioridade, 
        complexidade e responsabilidade, fortalecendo governança, equidade interna e decisões transparentes de 
        remuneração e carreira. Com uma arquitetura bem desenhada, a empresa consegue alinhar expectativas, facilitar 
        mobilidade interna e garantir que posições semelhantes sejam tratadas com a mesma lógica em todas as áreas 
        e geografias.
    </p>

</div>
"""

st.components.v1.html(html, height=700)
