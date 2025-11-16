# pages/4_Job_Maps.py
# FINAL — Versão Perfeita + Filtros + Fullscreen Azul SIG + Coluna GG Ajustada

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from utils.data_loader import load_excel_data

# ==========================================================
# CONFIG DA PÁGINA
# ==========================================================
st.set_page_config(page_title="Job Maps", layout="wide")

# ==========================================================
# HEADER CLEAN — PADRÃO DO APP
# ==========================================================
def header(icon_path: str, title: str):
    col1, col2 = st.columns([0.08, 0.92])
    with col1:
        st.image(icon_path, width=48)
    with col2:
        st.markdown(
            f"<h1 style='margin:0; padding:0; font-size:36px; font-weight:700;'>{title}</h1>",
            unsafe_allow_html=True
        )
    st.markdown("<hr style='margin-top:5px;'>", unsafe_allow_html=True)

header("assets/icons/globe_trade.png", "Job Maps")

# ==========================================================
# CSS — VISUAL PERFEITO + ACABAMENTOS FINAIS
# ==========================================================
css = """
<style>

:root {
    --border: #d9d9d9;
    --gg-bg: #000000;
    --family-bg: #4F5D75;
    --subfamily-bg: #E9EDF2;
    --sig-blue: #145efc;
}

/* WRAPPER */
.map-wrapper {
    height: 75vh;
    overflow: auto;
    border-radius: 10px;
    border: 0.5px solid var(--border);
    background: white;
}

/* GRID */
.jobmap-grid {
    display: grid;
    width: max-content;
    font-size: 0.88rem;
    border-collapse: collapse;
}

/* ====================================== */
/* HEADER FAMÍLIA — ALTURA 55px PERFEITA */
/* ====================================== */
.header-family {
    background: var(--family-bg);
    color: white;
    height: 55px !important;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    position: sticky;
    top: 0;
    z-index: 10;
    border-right: 1px solid white;
}

/* ======================================= */
/* HEADER SUBFAMÍLIA — ALTURA 44px SLIM    */
/* ======================================= */
.header-subfamily {
    background: var(--subfamily-bg);
    color: #222;
    height: 44px !important;
    display: flex;
    align-items: center;
    justify-content: center;
    position: sticky;
    top: 55px;
    z-index: 9;
    border-right: 1px solid var(--border);
}

/* =============================== */
/* COLUNA GG — 140px + BORDAS      */
/* =============================== */
.gg-header {
    background: var(--gg-bg);
    color: white;
    width: 140px !important;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;

    /* STICKY */
    position: sticky;
    left: 0;
    top: 0;
    z-index: 30;

    /* Borda branca entre título e GG21 */
    border-bottom: 1px solid var(--border);
}

.gg-cell {
    background: var(--gg-bg);
    color: white;
    width: 140px !important;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;

    /* STICKY lateral */
    position: sticky;
    left: 0;
    z-index: 25;

    /* Mesmo estilo de borda entre GG20/GG19 */
    border-bottom: 1px solid var(--border);
}

/* CÉLULAS */
.cell {
    border-right: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    padding: 6px;
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    align-items: center;
}

/* CARDS */
.job-card {
    background: white;
    border: 1px solid var(--border);
    border-left-width: 4px !important;
    border-radius: 6px;
    padding: 6px 8px;
    width: 135px;
    height: 75px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.job-card b {
    font-size: 0.78rem;
    margin-bottom: 3px;
}

.job-card span {
    font-size: 0.70rem;
    color: #555;
}

/* FULLSCREEN BUTTONS — SIG BLUE */
.fullscreen-btn, .exit-btn {
    position: fixed;
    bottom: 28px;
    right: 28px;
    z-index: 999999;
    background: var(--sig-blue) !important;
    color: white !important;
    border-radius: 28px !important;
    padding: 12px 28px !important;
    border: none !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.35) !important;
}

</style>
"""

st.markdown(css, unsafe_allow_html=True)

# ==========================================================
# CARREGAR DADOS
# ==========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

if df.empty:
    st.error("Job Profile não encontrado.")
    st.stop()

df = df.copy()
df["Job Family"] = df["Job Family"].astype(str).str.strip()
df["Sub Job Family"] = df["Sub Job Family"].astype(str).str.strip().replace(['nan', 'None', '<NA>'], '-')
df["Career Path"] = df["Career Path"].astype(str).str.strip()
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True)

# ==========================================================
# FILTROS — AGORA ABAIXO DO HEADER
# ==========================================================
colA, colB = st.columns(2)

families = ["Todas"] + sorted(df["Job Family"].unique())
paths = ["Todas"] + sorted(df["Career Path"].unique())

fam_filter = colA.selectbox("Job Family", families)
path_filter = colB.selectbox("Career Path", paths)

df_flt = df.copy()
if fam_filter != "Todas":
    df_flt = df_flt[df_flt["Job Family"] == fam_filter]
if path_filter != "Todas":
    df_flt = df_flt[df_flt["Career Path"] == path_filter]

# ==========================================================
# CORES SIG PARA CARREIRA
# ==========================================================
def get_path_color(p):
    p = str(p).lower()
    if "manage" in p or "executive" in p: return "#00493b"
    if "professional" in p: return "#73706d"
    if "tech" in p or "support" in p: return "#a09b05"
    return "#145efc"

# ==========================================================
# GERAR MAPA
# ==========================================================
@st.cache_data(ttl=600)
def generate_map(df):

    grades = sorted(df["Global Grade"].unique(), key=lambda x: int(x), reverse=True)
    families_order = sorted(df["Job Family"].unique())

    submap = {}
    col_index = 2
    for fam in families_order:
        subs = sorted(df[df["Job Family"] == fam]["Sub Job Family"].unique())
        for s in subs:
            submap[(fam, s)] = col_index
            col_index += 1

    grouped = df.groupby(["Job Family", "Sub Job Family", "Global Grade"])
    cards = {k: v.to_dict("records") for k, v in grouped}

    html = []
    html.append("<div class='map-wrapper'><div class='jobmap-grid'>")

    # HEADER GG
    html.append("<div class='gg-header' style='grid-column:1; grid-row:1 / span 2;'>GG</div>")

    # FAMÍLIA
    col = 2
    for fam in families_order:
        subs = sorted(df[df["Job Family"] == fam]["Sub Job Family"].unique())
        span = len(subs)
        html.append(f"<div class='header-family' style='grid-column:{col} / span {span};'>{fam}</div>")
        col += span

    # SUBFAMÍLIA
    for (fam, sub), c in submap.items():
        html.append(f"<div class='header-subfamily' style='grid-column:{c};'>{sub}</div>")

    # LINHAS
    row = 3
    for g in grades:
        html.append(f"<div class='gg-cell' style='grid-row:{row};'>GG {g}</div>")

        for (fam, sub), c_idx in submap.items():
            recs = cards.get((fam, sub, g), [])
            cell_html = ""

            for r in recs:
                color = get_path_color(r["Career Path"])
                cell_html += (
                    f"<div class='job-card' style='border-left-color:{color};'>"
                    f"<b>{r['Job Profile']}</b>"
                    f"<span>{r['Career Path']} — GG {g}</span>"
                    "</div>"
                )

            html.append(
                f"<div class='cell' style='grid-column:{c_idx}; grid-row:{row};'>{cell_html}</div>"
            )

        row += 1

    html.append("</div></div>")
    return "".join(html)

# ==========================================================
# RENDER MAP
# ==========================================================
st.markdown(generate_map(df_flt), unsafe_allow_html=True)

# ==========================================================
# FULLSCREEN MODE
# ==========================================================
if "fs" not in st.session_state:
    st.session_state.fs = False

if not st.session_state.fs:
    if st.button("⛶ Tela Cheia", key="fs_on"):
        st.session_state.fs = True
        st.rerun()

if st.session_state.fs:

    st.markdown(
        """<button class="exit-btn" onclick="window.parent.location.reload()">Sair</button>""",
        unsafe_allow_html=True
    )

    components.html("""
        <script>
        document.addEventListener('keydown', (e)=>{
            if(e.key === "Escape"){
                const btn = window.parent.document.querySelector('.exit-btn');
                if(btn){ btn.click(); }
            }
        });
        </script>
    """, height=0, width=0)
