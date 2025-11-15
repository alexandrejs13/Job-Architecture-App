import streamlit as st

st.set_page_config(
    page_title="Home | SIG Job Architecture",
    layout="wide"
)

# ---- CSS ----
st.markdown("""
<style>
.home-container {
    text-align: center;
    margin-top: 40px;
}

.title-row {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 25px;
    margin-top: 25px;
}

.title-icon {
    width: 90px;
}

.home-icons-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 50px;
    margin-top: 60px;
    padding-left: 10%;
    padding-right: 10%;
}

.home-icons-grid img {
    width: 110px;
    height: auto;
    transition: 0.2s;
}

.home-icons-grid img:hover {
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# ---- HEADER ----
st.markdown('<div class="home-container">', unsafe_allow_html=True)

# Logo SIG
st.image("assets/icons/SIG_Logo_RGB_Black.png", width=200)

# Ícone + Título
st.markdown('<div class="title-row">', unsafe_allow_html=True)
st.image("assets/icons/governance.png", width=90)
st.markdown("<h1 style='margin:0;'>Job Architecture</h1>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Subtítulo
st.markdown("""
### Base de Dados de Descrições de Cargos Genéricas  
para Classificação e Harmonização Global
""")

st.markdown('</div>', unsafe_allow_html=True)

# ---- ÍCONES DA GRADE ----
st.markdown('<div class="home-icons-grid">', unsafe_allow_html=True)

# Lista: ícone → label → destino
items = [
    ("assets/icons/governance.png", "Job Architecture", "pages/1_Job_Architecture.py"),
    ("assets/icons/people_employees.png", "Job Families", "pages/2_Job_Families.py"),
    ("assets/icons/business_review_clipboard.png", "Job Profile Description", "pages/3_Job_Profile_Description.py"),
    ("assets/icons/data_2_perfromance.png", "Job Maps", "pages/4_Job_Maps.py"),
    ("assets/icons/checkmark_success.png", "Job Match", "pages/5_Job_Match.py"),
    ("assets/icons/globe_trade.png", "Structure Level", "pages/6_Structure_Level.py"),
    ("assets/icons/process.png", "Dashboard", "pages/7_Dashboard.py"),
]

# Renderização dos ícones com navegação nativa
for icon, label, target in items:
    st.page_link(target, label=label, icon=icon)

st.markdown('</div>', unsafe_allow_html=True)
