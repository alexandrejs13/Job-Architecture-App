import streamlit as st
from PIL import Image
import os

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)

# carregar e aplicar CSS
with open("assets/css/theme.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ========== HOME LAYOUT ==========
st.markdown('<div class="home-center">', unsafe_allow_html=True)

# LOGO GRANDE
logo = Image.open("assets/icons/SIG_Logo_RGB_Black.png")
st.image(logo, width=240)

# ÍCONE + TÍTULO INLINE
icon = Image.open("assets/icons/governance.png")
col1, col2 = st.columns([1, 4])
with col1:
    st.image(icon, width=70)
with col2:
    st.markdown("<h1 style='margin-top: 15px;'>Job Architecture</h1>", unsafe_allow_html=True)

# SUBTÍTULO
st.markdown("""
<div class="home-subtitle">
Base de Dados de Descrições de Cargos Genéricas para Classificação e Harmonização Global
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# ========== ÍCONES DO MENU (clicáveis) ==========
import streamlit as st

st.markdown("---")
st.markdown("### Acessar Módulos")

# páginas e ícones
links = {
    "Job Architecture": ("governance.png", "1_Job_Architecture"),
    "Job Families": ("people_employees.png", "2_Job_Families"),
    "Job Profile Description": ("business_review_clipboard.png", "3_Job_Profile_Description"),
    "Job Maps": ("globe_trade.png", "4_Job_Maps"),
    "Job Match": ("checkmark_success.png", "5_Job_Match"),
    "Structure Level": ("process.png", "6_Structure_Level"),
    "Dashboard": ("data_2_performance.png", "7_Dashboard")
}

st.markdown('<div class="icon-grid">', unsafe_allow_html=True)

for label, (icon_file, page_file) in links.items():
    path = f"assets/icons/{icon_file}"
    st.markdown(
        f"""
        <div class="icon-item" onclick="window.location.href='/{page_file}'">
            <img src="{path}">
            <div class="icon-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)
