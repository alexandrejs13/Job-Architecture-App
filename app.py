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
# ICON PATH
# ==========================================================
icon_path = "assets/icons/governance.png"
icon_b64 = load_icon_png(icon_path)

# ==========================================================
# HTML
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
    font-size: 64px;
    margin: 0;
    padding: 0;
    text-align: center;
}}

p.sig-subtitle {{
    font-family: 'SIGFlowRegular', sans-serif;
    font-size: 20px;
    margin-top: 12px;
    color: #555;
    text-align: center;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
}}
</style>

<div style="text-align:center; padding-top:40px;">

    <h1 class="sig-title">Job Architecture</h1>

    <p class="sig-subtitle">
        A global job framework designed to standardize governance and harmonize roles across the organization.
    </p>

    <img src="data:image/png;base64,{icon_b64}"
         style="width:260px; margin-top:26px;">
</div>
"""

st.markdown(html, unsafe_allow_html=True)
