# html_renderer.py
import html
import os
import pandas as pd
from typing import Dict

# ---------------------------------------------------------
# Carrega SVG
# ---------------------------------------------------------
def load_svg(svg_name: str) -> str:
    path = os.path.join("assets", "icons", "sig", svg_name)
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        svg = f.read()
        svg = svg.replace('<?xml version="1.0" encoding="utf-8"?>', '')
        return svg

ICONS_SVG: Dict[str, str] = {
    "Sub Job Family Description": load_svg("Hierarchy.svg"),
    "Job Profile Description": load_svg("Content_Book_Phone.svg"),
    "Career Band Description": load_svg("File_Clipboard_Text.svg"),
    "Role Description": load_svg("Shopping_Business_Target.svg"),
    "Grade Differentiator": load_svg("User_Add.svg"),
    "Qualifications": load_svg("Edit_Pencil.svg"),
    "Specific parameters / KPIs": load_svg("Graph_Bar.svg"),
    "Competencies 1": load_svg("Setting_Cog.svg"),
    "Competencies 2": load_svg("Setting_Cog.svg"),
    "Competencies 3": load_svg("Setting_Cog.svg"),
}

SECTIONS_ORDER = [
    "Sub Job Family Description",
    "Job Profile Description",
    "Career Band Description",
    "Role Description",
    "Grade Differentiator",
    "Qualifications",
    "Specific parameters / KPIs",
    "Competencies 1",
    "Competencies 2",
    "Competencies 3",
]


# =====================================================================
# FUNÇÃO PRINCIPAL
# =====================================================================
def render_job_description(best_match_row: pd.Series, final_score: float) -> str:

    def safe_get(col):
        try:
            val = best_match_row.get(col, "")
            if pd.isna(val):
                return ""
            return str(val)
        except:
            return ""

    job_title = html.escape(safe_get("Job Profile"))
    gg = html.escape(safe_get("Global Grade"))
    jf = html.escape(safe_get("Job Family"))
    sf = html.escape(safe_get("Sub Job Family"))
    cp = html.escape(safe_get("Career Path"))
    fc = html.escape(safe_get("Full Job Code"))

    out = []

    out.append("""
<style>
body {
    background: #ffffff !important;
    margin: 0;
    font-family: "Segoe UI", sans-serif;
}

/* libera scroll total */
html, body {
    overflow-y: visible !important;
}

/* CARD PRINCIPAL */
.job-card {
    background: #f5f3ee;
    border-radius: 16px;
    padding: 26px 30px;
    border: 1px solid #e3e1dd;
    margin-bottom: 32px;
}

/* Título */
.job-title {
    font-size: 26px;
    font-weight: 700;
}

/* Subtítulo + pílula */
.job-subtitle {
    font-size: 18px;
    font-weight: 700;
    color: #145efc;
    margin-top: 4px;
    display: flex;
    align-items: center;
    gap: 12px;
}

/* Pílula do score */
.pill {
    background: #145efc;
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
}

/* Meta-card */
.meta-card {
    background: white;
    padding: 14px 18px;
    margin-top: 18px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    font-size: 15px;
    line-height: 1.55;
}

/* Seções */
.section-box {
    margin-bottom: 28px;
}

.section-title {
    font-size: 18px;
    font-weight: 700;
    display: flex;
    gap: 8px;
    align-items: center;
}

.section-title svg {
    width: 22px;
    height: 22px;
}

.section-line {
    height: 1px;
    background: #e8e6e1;
    margin: 8px 0 12px 0;
}

.section-text {
    font-size: 15px;
    line-height: 1.55;
    white-space: pre-wrap;
}

</style>
""")

    # topo
    out.append("<div class='job-card'>")

    out.append(f"""
        <div class="job-title">{job_title}</div>

        <div class="job-subtitle">
            GG {gg} • Job Match
            <span class="pill">{final_score}%</span>
        </div>

        <div class="meta-card">
            <b>Job Family:</b> {jf}<br>
            <b>Sub Job Family:</b> {sf}<br>
            <b>Career Path:</b> {cp}<br>
            <b>Full Job Code:</b> {fc}
        </div>
    """)

    out.append("</div>")

    # seções completas (mesmo se vazias!)
    for sec in SECTIONS_ORDER:
        raw_text = safe_get(sec)
        icon_svg = ICONS_SVG.get(sec, "")

        out.append(f"""
            <div class="section-box">
                <div class="section-title">
                    {icon_svg} {html.escape(sec)}
                </div>
                <div class="section-line"></div>
                <div class="section-text">{html.escape(raw_text)}</div>
            </div>
        """)

    return "\n".join(out)
