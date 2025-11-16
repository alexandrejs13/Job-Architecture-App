# -*- coding: utf-8 -*-
# pages/4_Job_Maps.py — versão completa final (SIG brand)

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from pathlib import Path

from utils.data_loader import load_excel_data


# ==========================================================
# 1. CONFIGURAR PÁGINA
# ==========================================================
st.set_page_config(page_title="Job Maps", layout="wide")


# ==========================================================
# 2. HEADER PADRÃO (idêntico às outras páginas)
# ==========================================================
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

# Carregar CSS global (header.css)
css_path = Path(__file__).parents[1] / "assets" / "header.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)


# ==========================================================
# 3. CSS DO MAPA (CLEAN + SIG BRAND)
# ==========================================================
st.markdown(
    """
<style>

:root {
    --gray-line: #e5e5e5;
    --dark-gray: #2f2f2f;

    /* Cores SIG — ajustadas para contraste */
    --mgmt: #73706d;     /* Management */
    --prof: #7e7873;     /* Professional */
    --tech: #a3a09b;     /* Technical */
    --proj: #8a837d;     /* Project */
}

/* MAP WRAPPER */
.map-wrapper {
    height: 75vh;
    overflow: auto;
    background: white;
    border: 1px solid var(--gray-line);
    border-radius: 10px;
}

/* GRID */
.jobmap-grid {
    display: grid;
    width: max-content;
    background: white;
    grid-auto-rows: 115px;
    font-size: 0.86rem;
}

/* CÉLULAS */
.cell {
    background: white;
    border-right: 1px solid var(--gray-line);
    border-bottom: 1px solid var(--gray-line);
    padding: 8px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}


/* GG HEADER — STICKY TOTAL */
.gg-header {
    background: var(--dark-gray);
    color: white;
    font-weight: 800;
    display: flex;
    justify-content: center;
    align-items: center;
    position: sticky;
    left: 0;
    top: 0;
    z-index: 50;
    border-right: 2px solid white;
}

/* COLUNA GG — STICKY VERTICAL + HORIZONTAL */
.gg-cell {
    background: var(--dark-gray);
    color: white;
    font-weight: 700;
    position: sticky;
    left: 0;
    z-index: 40;
    display: flex;
    justify-content: center;
    align-items: center;
    border-right: 2px solid white;
}

/* FAMÍLIAS — STICKY */
.header-family {
    background: #dcdcdc;
    color: #222;
    font-weight: 700;
    text-align: center;
    padding: 5px;
    position: sticky;
    top: 0;
    z-index: 30;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* SUBFAMÍLIAS — STICKY */
.header-subfamily {
    background: #f3f3f3;
    color: #222;
    font-weight: 600;
    text-align: center;
    padding: 5px;
    position: sticky;
    top: 52px;
    z-index: 25;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* CARDS (SIG brand) */
.job-card {
    background: white;
    border: 1px solid #e0e0e0;
    border-left-width: 5px !important;
    border-radius: 6px;
    padding: 6px 8px;
    width: 150px;
    height: 78px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.job-card b {
    font-size: 0.78rem;
    margin-bottom: 3px;
}

/* FULLSCREEN */
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
    padding: 12px 28px !important;
    border-radius: 40px !important;
    font-weight: 700 !important;
    border: none !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.35) !important;
}
#exit-fs button:hover { background: #000 !important; }

</style>
""",
    unsafe_allow_html=True
)


# ==========================================================
# 4. CARREGAR DADOS
# ==========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

if df.empty:
    st.error("Erro ao carregar Job Profile.xlsx")
    st.stop()

df = df.copy()
df["Job Family"] = df["Job Family"].astype(str).str.strip()
df["Sub Job Family"] = df["Sub Job Family"].astype(str).str.strip()
df["Sub Job Family"] = df["Sub Job Family"].replace(["", "nan", "None", "<NA>"], "-")
df["Career Path"] = df["Career Path"].astype(str).str.strip()
df["Global Grade"] = (
    df["Global Grade"]
    .astype(str)
    .str.replace(r"\\.0$", "", regex=True)
)

# ==========================================================
# 5. CORES SIG POR CARREIRA
# ==========================================================
def get_path_color(path):
    p = str(path).lower()
    if "manage" in p or "executive" in p: return "var(--mgmt)"
    if "professional" in p: return "var(--prof)"
    if "tech" in p: return "var(--tech)"
    return "var(--proj)"


# ==========================================================
# 6. FILTROS
# ==========================================================
colA, colB = st.columns(2)
fam_filter = colA.selectbox("Job Family", ["Todas"] + sorted(df["Job Family"].unique()))
path_filter = colB.selectbox("Career Path", ["Todas"] + sorted(df["Career Path"].unique()))

df_filtered = df.copy()
if fam_filter != "Todas":
    df_filtered = df_filtered[df_filtered["Job Family"] == fam_filter]

if path_filter != "Todas":
    df_filtered = df_filtered[df_filtered["Career Path"] == path_filter]


# ==========================================================
# 7. FUNÇÃO DO MAPA (MERGE + STICKY + SIG)
# ==========================================================
@st.cache_data(ttl=600, show_spinner="Gerando Job Map…")
def generate_map_html(df):

    families = sorted(df["Job Family"].unique())
    grades = sorted(df["Global Grade"].unique(), key=lambda x: int(x), reverse=True)

    # Subfamílias → colunas
    submap = {}
    col_i = 2
    fam_span = {}

    for f in families:
        subs = sorted(df[df["Job Family"] == f]["Sub Job Family"].unique())
        fam_span[f] = len(subs)
        for sf in subs:
            submap[(f, sf)] = col_i
            col_i += 1

    # Agrupar cards
    grouped = df.groupby(["Job Family", "Sub Job Family", "Global Grade"])
    cards = {k: v.to_dict("records") for k, v in grouped}

    # Merge vertical
    content = {}
    span = {}
    skip = set()

    for g in grades:
        for (f, sf), idx in submap.items():
            rec = cards.get((f, sf, g), [])
            content[(g, idx)] = "|".join(sorted(r["Job Profile"] for r in rec)) if rec else None

    for (f, sf), idx in submap.items():
        for i, g in enumerate(grades):
            if (g, idx) in skip:
                continue

            cur = content[(g, idx)]
            if cur is None:
                span[(g, idx)] = 1
                continue

            s = 1
            for g2 in grades[i + 1:]:
                if content[(g2, idx)] == cur:
                    s += 1
                    skip.add((g2, idx))
                else:
                    break
            span[(g, idx)] = s

    # HTML final
    html = [
        "<div class='map-wrapper'><div class='jobmap-grid' style='grid-template-columns:160px repeat("
        + str(len(submap))
        + ", 200px);'>"
    ]

    # Header GG
    html.append("<div class='gg-header' style='grid-column:1; grid-row:1 / span 2;'>GG</div>")

    # Header Família
    col = 2
    for f in families:
        html.append(
            f"<div class='header-family' style='grid-column:{col} / span {fam_span[f]};'>{f}</div>"
        )
        col += fam_span[f]

    # Header Subfamília
    for (f, sf), idx in submap.items():
        html.append(f"<div class='header-subfamily' style='grid-column:{idx};'>{sf}</div>")

    # Linhas
    r = 3
    for g in grades:
        html.append(f"<div class='gg-cell' style='grid-row:{r}; grid-column:1;'>GG {g}</div>")

        for (f, sf), idx in submap.items():

            if (g, idx) in skip:
                continue

            sp = span.get((g, idx), 1)
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

            html.append(f"<div class='cell' style='grid-column:{idx}; {rspan}'>{cell}</div>")

        r += 1

    html.append("</div></div>")
    return "".join(html)


# ==========================================================
# 8. TELA CHEIA
# ==========================================================
if "fs" not in st.session_state:
    st.session_state.fs = False

colFS = st.columns([6, 1])[1]
if not st.session_state.fs:
    if colFS.button("⛶ Tela cheia"):
        st.session_state.fs = True
        st.rerun()

if st.session_state.fs:
    st.markdown("<div class='fullscreen-wrapper'>", unsafe_allow_html=True)

    st.markdown("<div id='exit-fs'>", unsafe_allow_html=True)
    if st.button("Sair"):
        st.session_state.fs = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    components.html(
        """
        <script>
        document.addEventListener("keydown", (e)=>{
            if(e.key==="Escape"){
                const btn = window.parent.document.querySelector("#exit-fs button");
                if(btn){ btn.click(); }
            }
        });
        </script>
        """,
        height=0,
        width=0,
    )


# ==========================================================
# 9. RENDERIZAR MAPA
# ==========================================================
st.markdown(generate_map_html(df_filtered), unsafe_allow_html=True)
