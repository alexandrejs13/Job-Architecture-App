# -*- coding: utf-8 -*-
# pages/4_Job_Maps.py — versão final, completa e funcional

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from pathlib import Path

from utils.data_loader import load_excel_data
from utils.ui import setup_sidebar
from utils.ui_components import lock_sidebar


# ==========================================================
# 1. CONFIGURAÇÃO DE PÁGINA + HEADER PADRÃO
# ==========================================================
st.set_page_config(
    page_title="Job Maps",
    layout="wide"
)

setup_sidebar()
lock_sidebar()


def header(icon_path, title):
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
            unsafe_allow_html=True
        )
    st.markdown("<hr style='margin-top:5px;'>", unsafe_allow_html=True)


header("assets/icons/globe_trade.png", "Job Maps")


# ==========================================================
# 2. CSS NOVO — CLEAN, STICKY, MODERNO
# ==========================================================
st.markdown("""
<style>

:root {
    --blue: #145efc;
    --gray-line: #e5e5e5;
    --dark-gray: #2f2f2f;
}

/* MAP WRAPPER */
.map-wrapper {
    height: 74vh;
    overflow: auto;
    background: white;
    border-radius: 10px;
    border: 2px solid var(--gray-line);
    position: relative;
}

/* GRID */
.jobmap-grid {
    display: grid;
    width: max-content;
    background: white;
    grid-auto-rows: 115px;
    font-size: 0.86rem;
}

/* CELLS */
.cell {
    background: white;
    border-right: 1px solid var(--gray-line);
    border-bottom: 1px solid var(--gray-line);
    padding: 8px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

/* GG HEADER */
.gg-header {
    background: var(--dark-gray);
    color: white;
    font-weight: 800;
    position: sticky;
    left: 0;
    top: 0;
    z-index: 40;
    display: flex;
    justify-content: center;
    align-items: center;
    border-right: 2px solid white;
}

/* GG CELLS */
.gg-cell {
    background: var(--dark-gray);
    color: white;
    font-weight: 700;
    position: sticky;
    left: 0;
    z-index: 30;
    display: flex;
    justify-content: center;
    align-items: center;
    border-right: 2px solid white;
}

/* FAMÍLIAS */
.header-family {
    background: #4F5D75;
    color: white;
    font-weight: 700;
    padding: 6px;
    text-align: center;
    position: sticky;
    top: 0;
    height: 50px;
    z-index: 25;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* SUBFAMÍLIAS */
.header-subfamily {
    background: #E9EDF2;
    color: #222;
    font-weight: 600;
    padding: 6px;
    text-align: center;
    position: sticky;
    top: 50px;
    height: 45px;
    z-index: 24;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* JOB CARD */
.job-card {
    background: white;
    border: 1px solid var(--gray-line);
    border-left-width: 4px !important;
    border-radius: 6px;
    padding: 5px 7px;
    width: 135px;
    height: 75px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.job-card b {
    font-size: 0.76rem;
    margin-bottom: 3px;
}

/* FULLSCREEN WRAPPER */
.fullscreen-wrapper {
    position: fixed !important;
    top: 0; left: 0;
    height: 100vh !important;
    width: 100vw !important;
    background: white;
    z-index: 9999 !important;
    padding: 0 !important;
    margin: 0 !important;
}

/* BOTÃO PRETO FOSCO */
#exit-fs button {
    background: #111 !important;
    color: white !important;
    border-radius: 40px !important;
    padding: 14px 32px !important;
    font-weight: 700 !important;
    border: none !important;
    box-shadow: 0 4px 18px rgba(0,0,0,0.35) !important;
}
#exit-fs button:hover {
    background: black !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# 3. LOAD DATA
# ==========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

if df.empty:
    st.error("Erro: Não foi possível carregar Job Profile.")
    st.stop()

df = df.copy()
df["Job Family"] = df["Job Family"].astype(str).str.strip()
df["Sub Job Family"] = df["Sub Job Family"].astype(str).str.strip().replace(['nan', 'None', '<NA>', ''], '-')
df["Career Path"] = df["Career Path"].astype(str).str.strip()
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(r"\.0$", "", regex=True)


# ==========================================================
# 4. CORES DISCRETAS POR TRILHA
# ==========================================================
def get_path_color(path):
    p = str(path).lower()
    if "manage" in p or "executive" in p: return "#4F5D75"
    if "professional" in p: return "#2F2F2F"
    if "tech" in p: return "#7C7C7C"
    return "#5F6C7A"   # default (project)


# ==========================================================
# 5. FILTROS
# ==========================================================
colA, colB = st.columns(2)
fam = colA.selectbox("Job Family", ["Todas"] + sorted(df["Job Family"].unique()))
path = colB.selectbox("Career Path", ["Todas"] + sorted(df["Career Path"].unique()))

df_filtered = df.copy()
if fam != "Todas":
    df_filtered = df_filtered[df_filtered["Job Family"] == fam]
if path != "Todas":
    df_filtered = df_filtered[df_filtered["Career Path"] == path]


# ==========================================================
# 6. GERADOR DE MAPA (MERGE + STICKY)
# ==========================================================
@st.cache_data(ttl=600, show_spinner="Gerando mapa…")
def generate_map_html(df):

    families = sorted(df["Job Family"].unique())
    grades = sorted(df["Global Grade"].unique(), key=lambda x: int(x), reverse=True)

    submap = {}
    fam_span = {}
    col_i = 2

    for f in families:
        subs = sorted(df[df["Job Family"] == f]["Sub Job Family"].unique())
        fam_span[f] = len(subs)
        for sf in subs:
            submap[(f, sf)] = col_i
            col_i += 1

    grouped = df.groupby(["Job Family", "Sub Job Family", "Global Grade"])
    cards = {k: v.to_dict("records") for k, v in grouped}

    content = {}
    span = {}
    skip = set()

    for g in grades:
        for (f, sf), cidx in submap.items():
            rec = cards.get((f, sf, g), [])
            content[(g, cidx)] = "|".join(r["Job Profile"] for r in rec) if rec else None

    for (f, sf), cidx in submap.items():
        for i, g in enumerate(grades):

            if (g, cidx) in skip:
                continue

            cur = content[(g, cidx)]
            if cur is None:
                span[(g, cidx)] = 1
                continue

            s = 1
            for g2 in grades[i+1:]:
                if content[(g2, cidx)] == cur:
                    s += 1
                    skip.add((g2, cidx))
                else:
                    break
            span[(g, cidx)] = s

    html = ["<div class='map-wrapper'>"]
    html.append(f"<div class='jobmap-grid' style='grid-template-columns:160px repeat({len(submap)}, 200px);'>")

    # GG HEADER
    html.append("<div class='gg-header' style='grid-column:1; grid-row:1 / span 2;'>GG</div>")

    # FAMÍLIAS
    col = 2
    for f in families:
        html.append(f"<div class='header-family' style='grid-column:{col} / span {fam_span[f]};'>{f}</div>")
        col += fam_span[f]

    # SUBFAMÍLIAS
    for (f, sf), cidx in submap.items():
        html.append(f"<div class='header-subfamily' style='grid-column:{cidx};'>{sf}</div>")

    # LINHAS
    r = 3
    for g in grades:

        html.append(f"<div class='gg-cell' style='grid-row:{r}; grid-column:1;'>GG {g}</div>")

        for (f, sf), cidx in submap.items():

            if (g, cidx) in skip:
                continue

            sp = span.get((g, cidx), 1)
            rspan = f"grid-row:{r} / span {sp};"

            recs = cards.get((f, sf, g), [])
            cell = ""

            for rc in recs:
                color = get_path_color(rc["Career Path"])
                cell += (
                    f"<div class='job-card' style='border-left-color:{color};'>"
                    f"<b>{rc['Job Profile']}</b>"
                    f"<span>{rc['Career Path']}</span>"
                    "</div>"
                )

            html.append(f"<div class='cell' style='grid-column:{cidx}; {rspan}'>{cell}</div>")

        r += 1

    html.append("</div></div>")
    return "".join(html)


# ==========================================================
# 7. FULLSCREEN BUTTON
# ==========================================================
if "fs" not in st.session_state:
    st.session_state.fs = False

# Botão fullscreen no canto DIREITO
colFS = st.columns([6,1])[1]
if not st.session_state.fs:
    if colFS.button("⛶ Tela Cheia"):
        st.session_state.fs = True
        st.rerun()

if st.session_state.fs:
    st.markdown("<div class='fullscreen-wrapper'>", unsafe_allow_html=True)

    # BOTÃO SAIR
    st.markdown("<div id='exit-fs' style='position:fixed; bottom:30px; right:30px; z-index:99999;'>", unsafe_allow_html=True)
    if st.button("Sair"):
        st.session_state.fs = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ESC
    components.html("""
        <script>
        document.addEventListener('keydown', (e)=>{
            if(e.key==='Escape'){
                const btn = window.parent.document.querySelector('#exit-fs button');
                if(btn){ btn.click(); }
            }
        });
        </script>
    """, height=0, width=0)


# ==========================================================
# 8. MAPA FINAL
# ==========================================================
st.markdown(generate_map_html(df_filtered), unsafe_allow_html=True)
