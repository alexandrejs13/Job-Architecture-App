# pages/4_Job_Maps.py
# Job Maps – layout clean com merges, coluna GG ajustada e fullscreen

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from utils.data_loader import load_excel_data

# ==========================================================
# 1. CONFIGURAÇÃO DE PÁGINA + HEADER PADRÃO
# ==========================================================
st.set_page_config(page_title="Job Maps", layout="wide")


def header(icon_path: str, title: str):
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


header("assets/icons/globe_trade.png", "Job Maps")

# ==========================================================
# 2. CSS – BASE, COLUNA GG E FULLSCREEN
# ==========================================================
clean_css = """
<style>
:root {
    --border: #d9d9d9;
    --subtle-bg: #f7f7f7;
    --header-bg: #eaeaea;
    --text-gray: #444;
    --gg-bg: #000000;
}

/* WRAPPER DA TABELA */
.map-wrapper {
    height: 75vh;
    overflow: auto;
    border-radius: 10px;
    border: 0.5px solid var(--border);
    background: #ffffff;
}

/* GRID PRINCIPAL */
.jobmap-grid {
    display: grid;
    width: max-content;
    border-collapse: collapse;
    font-size: 0.88rem;
    grid-auto-rows: 110px;          /* mesma altura para todas as linhas */
}

/* HEADER FAMÍLIA (linha 1) */
.header-family {
    background: #4f5d75;            /* fundo forte */
    color: #ffffff;
    border-right: 0.5px solid #ffffff;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    position: sticky;
    top: 0;
    z-index: 20;
    padding: 0 6px;
}

/* HEADER SUBFAMÍLIA (linha 2) */
.header-subfamily {
    background: #e9edf2;            /* mesmo tom mais claro */
    color: #111111;
    border-right: 0.5px solid var(--border);
    font-weight: 600;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    position: sticky;
    top: 50px;                      /* logo abaixo da família */
    z-index: 19;
    padding: 0 6px;
}

/* COLUNA GG – HEADER */
.gg-header {
    background: var(--gg-bg);
    color: #ffffff;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    position: sticky;
    left: 0;
    top: 0;
    z-index: 30;
    border-right: 2px solid #ffffff;
    border-bottom: 1px solid #ffffff;
    align-self: stretch;
}

/* COLUNA GG – CÉLULAS */
.gg-cell {
    background: var(--gg-bg);
    color: #ffffff;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    position: sticky;
    left: 0;
    z-index: 25;
    padding: 0 8px;
    border-right: 2px solid #ffffff;   /* linha branca vertical */
    border-bottom: 1px solid #ffffff;  /* linha branca horizontal */
    align-self: stretch;               /* ocupa toda a altura da linha */
}

/* CÉLULAS NORMAIS */
.cell {
    border-bottom: 0.5px solid var(--border);
    border-right: 0.5px solid var(--border);
    padding: 6px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;     /* centraliza cards verticalmente dentro da célula */
}

/* JOB CARD – TAMANHO FIXO */
.job-card {
    background: #ffffff;
    border: 0.5px solid var(--border);
    border-left-width: 4px !important;
    border-radius: 6px;
    padding: 6px 8px;
    width: 135px;
    height: 75px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    transition: 0.20s ease;
}

.job-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}

.job-card b {
    font-size: 0.78rem;
    margin-bottom: 3px;
    color: #333333;
}

.job-card span {
    font-size: 0.7rem;
    color: #666666;
}

/* FULLSCREEN – WRAPPER + BOTÃO PRETO FOSCO */
.fullscreen-wrapper {
    position: fixed !important;
    top: 0;
    left: 0;
    height: 100vh !important;
    width: 100vw !important;
    background: #ffffff;
    z-index: 9998 !important;
    padding: 12px 16px !important;
    box-sizing: border-box;
}

#exit-fullscreen-btn {
    position: fixed;
    bottom: 28px;
    right: 28px;
    z-index: 999999 !important;
    background: #000000 !important;
    color: #ffffff !important;
    border-radius: 28px !important;
    padding: 12px 28px !important;
    border: none !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    box-shadow: 0px 4px 16px rgba(0,0,0,0.35) !important;
    cursor: pointer;
}
#exit-fullscreen-btn:hover {
    transform: scale(1.06);
}
</style>
"""
st.markdown(clean_css, unsafe_allow_html=True)

# ==========================================================
# 3. CARREGAMENTO E PREPARAÇÃO DO DATAFRAME
# ==========================================================
data = load_excel_data()
df = data.get("job_profile", pd.DataFrame())

if df.empty:
    st.error("Arquivo Job Profile não encontrado ou vazio.")
    st.stop()

df = df.copy()
df["Job Family"] = df["Job Family"].astype(str).str.strip()
df["Sub Job Family"] = df["Sub Job Family"].astype(str).str.strip().replace(
    ["nan", "None", "<NA>"], "-"
)
df["Career Path"] = df["Career Path"].astype(str).str.strip()
df["Global Grade"] = df["Global Grade"].astype(str).str.replace(
    r"\.0$", "", regex=True
)

df = df[
    (df["Job Family"] != "")
    & (df["Job Profile"] != "")
    & (df["Global Grade"] != "")
]

# ==========================================================
# 4. CORES DISCRETAS POR CARREIRA (SIG-INSPIRED)
# ==========================================================
def get_path_color(path_name: str) -> str:
    p = str(path_name).lower()
    if "manage" in p or "executive" in p:
        return "#00493b"  # Management – SIG Forest 3
    if "professional" in p:
        return "#73706d"  # Professional – SIG Sand 4
    if "tech" in p or "support" in p:
        return "#a09b05"  # Technical – SIG Moss 3
    return "#145efc"      # Project/Default – SIG Sky


# ==========================================================
# 5. FILTROS MINIMALISTAS
# ==========================================================
families = ["Todas"] + sorted(df["Job Family"].unique())
paths = ["Todas"] + sorted(df["Career Path"].unique())

colA, colB = st.columns(2)
fam_filter = colA.selectbox("Job Family", families)
path_filter = colB.selectbox("Career Path", paths)

df_flt = df.copy()
if fam_filter != "Todas":
    df_flt = df_flt[df_flt["Job Family"] == fam_filter]
if path_filter != "Todas":
    df_flt = df_flt[df_flt["Career Path"] == path_filter]

if df_flt.empty:
    st.info("Sem registros para os filtros selecionados.")
    st.stop()

# ==========================================================
# 6. GERAÇÃO DO MAPA COM MERGE VERTICAL
# ==========================================================
@st.cache_data(ttl=600, show_spinner="Gerando mapa…")
def generate_map_html(df: pd.DataFrame) -> str:
    families_order = sorted(df["Job Family"].unique())
    grades = sorted(
        df["Global Grade"].unique(),
        key=lambda x: int(x) if str(x).isdigit() else 999,
        reverse=True,
    )

    # --- MAPA DE SUBFAMÍLIAS (COLUNAS) ---
    submap = {}
    header_spans = {}
    col_index = 2  # coluna 1 é GG

    for fam in families_order:
        subs = sorted(df[df["Job Family"] == fam]["Sub Job Family"].unique())
        header_spans[fam] = len(subs)
        for s in subs:
            submap[(fam, s)] = col_index
            col_index += 1

    # --- AGRUPAMENTO DOS CARDS POR CÉLULA ---
    grouped = df.groupby(["Job Family", "Sub Job Family", "Global Grade"])
    cards = {k: v.to_dict("records") for k, v in grouped}

    # --- MERGE VERTICAL (mesma combinação conteúdo / coluna) ---
    content_map = {}
    span_map = {}
    skip_set = set()

    for g in grades:
        for (fam, sf), c_idx in submap.items():
            rec = cards.get((fam, sf, g), [])
            if rec:
                content_map[(g, c_idx)] = "|".join(
                    sorted(
                        f"{r['Job Profile']}|{r['Career Path']}"
                        for r in rec
                    )
                )
            else:
                content_map[(g, c_idx)] = None

    for (fam, sf), c_idx in submap.items():
        for i, g in enumerate(grades):
            if (g, c_idx) in skip_set:
                continue
            current = content_map[(g, c_idx)]
            if current is None:
                span_map[(g, c_idx)] = 1
                continue

            span = 1
            for next_g in grades[i + 1 :]:
                if content_map[(next_g, c_idx)] == current:
                    span += 1
                    skip_set.add((next_g, c_idx))
                else:
                    break
            span_map[(g, c_idx)] = span

    # --- CONSTRUÇÃO DO HTML ---
    num_subcols = len(submap)
    grid_style = (
        "grid-template-columns: 140px "
        + " ".join(["auto"] * num_subcols)
        + ";"
    )

    html = [
        "<div class='map-wrapper'><div class='jobmap-grid' style='"
        + grid_style
        + "'>"
    ]

    # HEADER GG (coluna 1, linhas 1–2)
    html.append(
        "<div class='gg-header' style='grid-column:1; grid-row:1 / span 2;'>GG</div>"
    )

    # HEADER FAMÍLIAS (linha 1)
    col = 2
    for fam in families_order:
        span = header_spans[fam]
        html.append(
            f"<div class='header-family' style='grid-row:1; grid-column:{col} / span {span};'>{fam}</div>"
        )
        col += span

    # HEADER SUBFAMÍLIAS (linha 2)
    for (fam, sf), c_idx in submap.items():
        html.append(
            f"<div class='header-subfamily' style='grid-row:2; grid-column:{c_idx};'>{sf}</div>"
        )

    # LINHAS PRINCIPAIS (a partir da linha 3)
    row_idx = 3
    for g in grades:
        # célula GG
        html.append(
            f"<div class='gg-cell' style='grid-row:{row_idx}; grid-column:1;'>GG {g}</div>"
        )

        # demais colunas
        for (fam, sf), c_idx in submap.items():
            if (g, c_idx) in skip_set:
                continue

            span = span_map.get((g, c_idx), 1)
            row_span = (
                f"grid-row:{row_idx} / span {span};"
                if span > 1
                else f"grid-row:{row_idx};"
            )

            recs = cards.get((fam, sf, g), [])
            cell_html = ""

            for rec in recs:
                color = get_path_color(rec["Career Path"])
                label = f"{rec['Career Path']} – GG {g}"
                cell_html += (
                    f"<div class='job-card' "
                    f"style='border-left-color:{color};'>"
                    f"<b>{rec['Job Profile']}</b>"
                    f"<span>{label}</span>"
                    "</div>"
                )

            html.append(
                f"<div class='cell' style='grid-column:{c_idx}; {row_span}'>{cell_html}</div>"
            )

        row_idx += 1

    html.append("</div></div>")
    return "".join(html)


map_html = generate_map_html(df_flt)

# ==========================================================
# 7. FULLSCREEN (BOTÃO PRETO FOSCO)
# ==========================================================
if "fullscreen" not in st.session_state:
    st.session_state.fullscreen = False

if not st.session_state.fullscreen:
    # modo normal: mostra mapa + botão para entrar em tela cheia
    st.markdown(map_html, unsafe_allow_html=True)

    col_fs = st.columns([6, 1])[1]
    if col_fs.button("⛶ Tela Cheia"):
        st.session_state.fullscreen = True
        st.experimental_rerun()
else:
    # modo tela cheia: wrapper fixo + botão sair
    st.markdown(
        "<div class='fullscreen-wrapper'>", unsafe_allow_html=True
    )
    st.markdown(map_html, unsafe_allow_html=True)

    # botão sair (preto fosco)
    st.markdown(
        "<button id='exit-fullscreen-btn'>❌ Sair</button>",
        unsafe_allow_html=True,
    )

    # ESC fecha tela cheia
    components.html(
        """
        <script>
        const btn = window.parent.document.getElementById('exit-fullscreen-btn');
        if (btn) {
            btn.onclick = function() {
                fetch(window.location.href, {method: 'POST'}).then(()=>{});
                window.parent.location.reload();
            };
        }
        document.addEventListener('keydown', (e)=>{
            if(e.key === "Escape" && btn){
                btn.click();
            }
        });
        </script>
        """,
        height=0,
        width=0,
    )
