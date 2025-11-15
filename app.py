import streamlit as st
import importlib
from pathlib import Path
import base64

# ---------------------------------------------------------
# CONFIGURAÇÃO GLOBAL DO APP
# ---------------------------------------------------------

st.set_page_config(
    page_title="Job Architecture App",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CSS PERSONALIZADO (LÊ ARQUIVO DA PASTA ASSETS)
# ---------------------------------------------------------
css_path = Path("assets/custom.css")
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)
else:
    st.error("Arquivo assets/custom.css não encontrado. Verifique o diretório.")


# ---------------------------------------------------------
# MENU CUSTOMIZADO COM PNGs
# ---------------------------------------------------------

MENU = {
    "Job Architecture": {
        "module": "pages.job_architecture",
        "icon": "assets/icons/governance.png"
    },
    "Job Families": {
        "module": "pages.job_families",
        "icon": "assets/icons/people_employees.png"
    },
    "Job Profile Description": {
        "module": "pages.job_profile_description",
        "icon": "assets/icons/business_review_clipboard.png"
    },
    "Job Maps": {
        "module": "pages.job_maps",
        "icon": "assets/icons/globe_trade.png"
    },
    "Job Match": {
        "module": "pages.job_match",
        "icon": "assets/icons/checkmark_success.png"
    },
    "Structure Level": {
        "module": "pages.structure_level",
        "icon": "assets/icons/process.png"
    },
    "Dashboard": {
        "module": "pages.dashboard",
        "icon": "assets/icons/data_2_perfromance.png"
    },
}


# ---------------------------------------------------------
# FUNÇÃO PARA MOSTRAR IMAGEM PNG NO MENU
# ---------------------------------------------------------
def icon_image(path, width=22):
    try:
        with open(path, "rb") as file:
            data = base64.b64encode(file.read()).decode()
        return f"<img src='data:image/png;base64,{data}' width='{width}'>"
    except:
        return ""


# ---------------------------------------------------------
# BARRA LATERAL CUSTOMIZADA
# ---------------------------------------------------------
with st.sidebar:
    st.image("assets/SIG_Logo_RGB_Black.png", width=180)
    st.markdown("<div class='menu-title'>Menu</div>", unsafe_allow_html=True)

    selected = None
    for label, info in MENU.items():
        icon_html = icon_image(info["icon"], width=26)
        button_label = f"{icon_html} <span class='menu-item'>{label}</span>"

        if st.button(button_label, use_container_width=True):
            selected = label

    # Caso nenhum botão tenha sido clicado ainda
    if selected is None:
        selected = list(MENU.keys())[0]


# ---------------------------------------------------------
# IMPORTAÇÃO DINÂMICA DA PÁGINA SELECIONADA
# ---------------------------------------------------------
page_module = importlib.import_module(MENU[selected]["module"])

# Executa o método run() da página
page_module.run()
