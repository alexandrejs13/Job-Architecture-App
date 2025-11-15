import streamlit as st
import base64

st.set_page_config(
    page_title="Job Architecture App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CSS GLOBAL ==========
css = """
<style>

@font-face {
    font-family:'SIGFlow';
    src: url(data:font/otf;base64,{{REG}}) format('opentype');
    font-weight:400;
}
@font-face {
    font-family:'SIGFlow';
    src: url(data:font/otf;base64,{{SEMI}}) format('opentype');
    font-weight:600;
}
@font-face {
    font-family:'SIGFlow';
    src: url(data:font/otf;base64,{{BOLD}}) format('opentype');
    font-weight:700;
}

html, body, p, div, span {
    font-family:'SIGFlow', sans-serif !important;
    color:#555 !important;
    font-size:18px !important;
    line-height:1.5 !important;
}

[data-testid="stSidebar"] {
    background:#f2efeb !important; 
}

[data-testid="stSidebarNav"] li:nth-of-type(1) {
    display:none !important;
}

[data-testid="stSidebarNav"] a[data-selected="true"] {
    background:#145efc !important;
    color:white !important;
    border-radius:8px !important;
    font-weight:600 !important;
}

[data-testid="stSidebarNav"] a:hover {
    background:#e5e3de !important;
}

</style>
"""

# ========== FONTES BASE64 ==========
import os
def load_font(path):
    return base64.b64encode(open(path,"rb").read()).decode()

reg = load_font("assets/fonts/PPSIGFlow-Regular.otf")
semi = load_font("assets/fonts/PPSIGFlow-SemiBold.otf")
bold = load_font("assets/fonts/PPSIGFlow-Bold.otf")

css = css.replace("{{REG}}", reg).replace("{{SEMI}}", semi).replace("{{BOLD}}", bold)

st.markdown(css, unsafe_allow_html=True)

# ========== SIDEBAR LOGO CORRETO ==========
st.sidebar.markdown("<div style='text-align:center; margin-top:20px;'>", unsafe_allow_html=True)
st.sidebar.image("assets/icons/logo_sig.svg", width=120)
st.sidebar.markdown("</div>", unsafe_allow_html=True)

# ========== HOME ==========
st.markdown("<h1>Home</h1>", unsafe_allow_html=True)
st.write("Bem-vindo.")
