import streamlit as st
import base64
import os
import pandas as pd

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(page_title="Job Families", layout="wide")

# ==========================================================
# FUNÇÃO PNG
# ==========================================================
def load_icon_png(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ==========================================================
# HEADER SIG
# ==========================================================
icon_path = "assets/icons/people_employees.png"
icon_b64 = load_icon_png(icon_path)

st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; margin-top:12px;">
    <img src="data:image/png;base64,{icon_b64}" style="width:56px; height:56px;">
    <h1 style="font-size:36px; font-weight:700; margin:0; padding:0;">
        Job Families
    </h1>
</div>

<hr style="margin-top:14px; margin-bottom:26px;">
""", unsafe_allow_html=True)

# ==========================================================
# GLOBAL LAYOUT — limita largura e impede esticar infinito
# ==========================================================
st.markdown("""
<style>

    .main > div {
        max-width: 1400px;
        margin-left: auto;
        margin-right: auto;
        padding-left: 20px;
        padding-right: 20px;
    }

    .stDataFrame {
        max-width: 1400px;
        margin-left: auto;
        margin-right: auto;
    }

    .block-container, .stColumn {
        max-width: 1400px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

</style>
""", unsafe_allow_html=True)


# ==========================================================
# CARREGAR ARQUIVO
# ==========================================================
file_path = "data/Job Family.xlsx"

if not os.path.exists(file_path):
    st.error("Arquivo **'Job Family.xlsx'** não encontrado na pasta `data/`.")
    st.stop()

df = pd.read_excel(file_path)
df.columns = [str(c).strip() for c in df.columns]

# remove a primeira coluna (sequencial)
df = df.iloc[:, 1:]

required_cols = {"Job Family", "Sub Job Family"}
if not required_cols.issubset(df.columns):
    st.error("Arquivo precisa conter colunas: Job Family e Sub Job Family.")
    st.stop()


# ==========================================================
# CONTEÚDO
# ==========================================================
st.markdown("""
### What Job Families Represent in a Job Architecture

**Job Families** group roles based on similar nature of work, capabilities, and functional purpose.  
They establish structure, clarity, and transparency inside the organization.

A robust Job Family framework:

- organizes work into meaningful capability clusters  
- supports fair and consistent leveling decisions  
- clarifies career path options  
- ensures functional comparability across the business  
- strengthens compensation alignment  

---

### Families, Subfamilies, Profiles and Description

- **Job Family** → broad discipline  
- **Sub Job Family** → specialization within the discipline  
- **Profile** → defined role inside a subfamily  
- **Description** → purpose, scope, influence, and functional expectations  

---
""")

# ==========================================================
# PICKLIST
# ==========================================================
st.markdown("### Explore Job Families and Subfamilies")

families = sorted(df["Job Family"].dropna().unique())
selected_family = st.selectbox("Select a Job Family:", families)

subfamilies = sorted(
    df[df["Job Family"] == selected_family]["Sub Job Family"]
    .dropna()
    .unique()
)

selected_subfamily = st.selectbox("Select a Sub Job Family:", subfamilies)

df_filtered = df[
    (df["Job Family"] == selected_family) &
    (df["Sub Job Family"] == selected_subfamily)
]

st.markdown("---")

# ==========================================================
# TABELA PREMIUM SIG
# ==========================================================
st.markdown("### Job Family & Subfamily Detail")

table_html = df_filtered.to_html(
    index=False,
    classes="sig-premium-table",
    escape=False
)

st.markdown("""
<style>

.sig-premium-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 15px;
    line-height: 1.45;
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
}

.sig-premium-table th {
    background: #f2f4f7;
    font-weight: 700;
    padding: 14px 16px;
    text-align: left;
    color: #333;
    white-space: normal;
    border-bottom: 1px solid #e5e7eb;
}

.sig-premium-table td {
    padding: 12px 16px;
    border-bottom: 1px solid #eee;
    vertical-align: top;
    white-space: normal;
    max-width: 420px;
    word-wrap: break-word;
}

.sig-premium-table tr:nth-child(even) td {
    background: #fafafa;
}

.sig-premium-table tr:hover td {
    background: #eef3ff;
    transition: background 0.25s ease;
}

.sig-premium-table thead tr:first-child th:first-child {
    border-top-left-radius: 12px;
}
.sig-premium-table thead tr:first-child th:last-child {
    border-top-right-radius: 12px;
}
.sig-premium-table tbody tr:last-child td:first-child {
    border-bottom-left-radius: 12px;
}
.sig-premium-table tbody tr:last-child td:last-child {
    border-bottom-right-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

st.markdown(table_html, unsafe_allow_html=True)

# ==========================================================
# RODAPÉ
# ==========================================================
st.caption("Navigate to Job Profiles, Structure Levels and Job Match.")
