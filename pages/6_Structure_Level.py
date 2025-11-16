# pages/6_Structure_Level.py

import streamlit as st
import pandas as pd
from utils.data_loader import load_excel_data

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================
st.set_page_config(page_title="Structure Level", layout="wide")


# ==========================================================
# HEADER PADRÃO DO APP NOVO
# ==========================================================
def header(icon_path: str, title: str) -> None:
    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        st.image(icon_path, width=48)
    with col2:
        st.markdown(
            f"""
            <h1 style="margin:0; padding:0; font-size:36px; font-weight:700;">
                {title}
            </h1>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("<hr style='margin-top:5px;'>", unsafe_allow_html=True)


header("assets/icons/process.png", "Structure Level")


# ==========================================================
# SEÇÃO DE TEXTO — IDENTIDADE NOVA + SEU TEXTO
# ==========================================================
st.markdown("""
### What “Structure Level” Means in an Organizational Career Architecture

A **Structure Level** is the standardized layer that organizes all roles in the company into a clear, comparable hierarchy.  
Instead of relying on job titles — which can vary across teams and countries — the Structure Level defines the *real substance* of a role:  
its scope, decision-making responsibility, complexity, and expected contribution to the organization.

It acts as a backbone for the entire career framework, ensuring that every job connects coherently to:

- the global grade  
- the career path  
- the career band  
- the career level  

---

### How It Works in Practice

The Structure Level translates each role into a consistent **organizational slot**.

Using your table as reference:

- **Grades 21–17 → Executive Leadership**  
  Strategic direction, broad impact, enterprise-level accountability.

- **Grades 16–12 → People Managers**  
  Leading teams, performance management, driving execution.

- **Grades 16–10 → Professional Path**  
  Deep functional or technical expertise with significant autonomy and influence.

- **Grades 9–5 → Specialists & Analysts**  
  Core functional delivery, increasing independence and technical depth.

- **Project Roles**  
  Follow the same progression (Coordinator → Manager → Program Manager), mapped to the same structural backbone.

Each level builds logically on the previous one, showing a progression of capability, scope, and contribution.

---

### Why Structure Levels Matter

#### **Consistency Across the Organization**
Every job — whether in Management, Professional, or Projects — is mapped to the same hierarchy, making comparisons fair and transparent.

#### **Clear Career Paths**
Employees understand how to progress not only by title but by capability and responsibility.

#### **Compensation Alignment**
Each Structure Level reflects a degree of complexity and impact, simplifying governance of compensation philosophy.

#### **Eliminates Title Inflation**
Anchors the *real* size of the role, regardless of naming differences across regions or functions.

#### **Enables Mobility & Workforce Planning**
With all roles aligned to the same structure, mobility and comparisons across teams, countries and functions become easier and more precise.

---

### How the Levels Reflect Real Organizational Progression

**Management Path**
- 21–17 → Enterprise leadership  
- 16–12 → People managers

**Professional Path**
- 16–14 → Lead Experts / Senior Experts  
- 13–11 → Experts  
- 10–7 → Specialists / Senior Specialists  
- 6–5  → Assistants / Analysts  

**Projects Path**
- Same structural backbone, mapped to scope and responsibility of project leadership.

---

The **Structure Level** unifies all these paths into a single, coherent organizational map.
""")


# ==========================================================
# CARREGAMENTO DO ARQUIVO (MANTIDO DO JEITO CERTO)
# ==========================================================
data = load_excel_data()
df = data.get("level_structure", pd.DataFrame())

if df.empty:
    st.error(
        "Arquivo **'Level Structure.xlsx'** não encontrado na pasta `data/` "
        "ou o arquivo está vazio."
    )
    st.stop()


# ==========================================================
# TABELA — MANTER COMO ESTÁ NO APP NOVO
# ==========================================================
st.markdown("### Structure Level Table")

st.dataframe(df, use_container_width=True)


# ==========================================================
# RODAPÉ
# ==========================================================
st.caption("Continue navegando para acessar Job Maps e Job Match.")
