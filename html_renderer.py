# html_renderer.py
import html
import os
from typing import Dict
import pandas as pd


# ---------------------------------------------------------
# Carrega SVGs igual à Job Profile Description
# ---------------------------------------------------------
def load_svg(svg_name: str) -> str:
    """
    Lê os SVGs a partir de assets/icons/sig/<nome>.svg
    """
    path = os.path.join("assets", "icons", "sig", svg_name)
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        svg = f.read()
        # remove header XML se existir
        svg = svg.replace('<?xml version="1.0" encoding="utf-8"?>', "")
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


def render_job_description(best_match_row: pd.Series, score_pct: float) -> str:
    """
    Mesmo layout da Job Profile Description (uma coluna),
    fundo branco, sem barra de rolagem interna.
    """

    job_profile = html.escape(str(best_match_row.get("Job Profile", "")))
    gg = html.escape(str(best_match_row.get("Global Grade", "")))
    jf = html.escape(str(best_match_row.get("Job Family", "")))
    sf = html.escape(str(best_match_row.get("Sub Job Family", "")))
    cp = html.escape(str(best_match_row.get("Career Path", "")))
    fc = html.escape(str(best_match_row.get("Full Job Code", "")))

    score_txt = f"{score_pct}%"

    out = []

    out.append(f"""
<html>
<head>
<meta charset="UTF-8">
<style>
html, body {{
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', sans-serif;
    background: #ffffff; /* fundo branco */
}}

.job-match-wrapper {{
    padding: 0;
    margin-top: 18px;
    margin-bottom: 30px;
}}

/* Card superior */
.job-match-card {{
    background: #f5f3ee;
    border-radius: 16px;
    padding: 22px 24px;
    border: 1px solid #e3e1dd;
    margin-bottom: 24px;
}}

.job-title {{
    font-size: 20px;
    font-weight: 700;
    line-height: 1.25;
    margin-bottom: 4px;
}}

.job-gg {{
    color: #145efc;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 10px;
}}

/* Linha com família / sub família / career / code */
.job-meta {{
    background: #ffffff;
    padding: 14px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    font-size: 14px;
    line-height: 1.4;
}}

.job-meta-main {{
    margin-bottom: 4px;
}}

.job-meta-score {{
    font-weight: 600;
    color: #145efc;
}}

/* Seções */
.job-sections {{
    display: flex;
    flex-direction: column;
    gap: 24px;
}}

.section-box {{
    padding-bottom: 4px;
}}

.section-title {{
    font-size: 16px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 6px;
}}

.section-icon {{
    width: 20px;
    height: 20px;
    display: inline-block;
}}

.section-line {{
    height: 1px;
    background: #e8e6e1;
    width: 100%;
    margin: 8px 0 12px 0;
}}

.section-text {{
    font-size: 14px;
    line-height: 1.45;
    white-space: pre-wrap;
}}
</style>
</head>
<body>
<div class="job-match-wrapper">

    <div class="job-match-card">
        <div class="job-title">{job_profile}</div>
        <div class="job-gg">GG {gg} • Job Match</div>

        <div class="job-meta">
            <div class="job-meta-main">
                Job Family: {jf} / Sub Job Family: {sf} / Career Path: {cp} / Full Job Code: {fc}
            </div>
            <div class="job-meta-score">
                Match Score: {score_txt}
            </div>
        </div>
    </div>

    <div class="job-sections">
""")

    # Seções na mesma ordem do Job Profile Description
    for sec in SECTIONS_ORDER:
        raw_val = best_match_row.get(sec, "")
        if pd.isna(raw_val) or str(raw_val).strip() == "":
            continue

        text_val = html.escape(str(raw_val))
        icon_svg = ICONS_SVG.get(sec, "")

        out.append(f"""
        <div class="section-box">
            <div class="section-title">
                <span class="section-icon">{icon_svg}</span>
                {html.escape(sec)}
            </div>
            <div class="section-line"></div>
            <div class="section-text">{text_val}</div>
        </div>
        """)

    out.append("""
    </div> <!-- job-sections -->
</div> <!-- job-match-wrapper -->
</body>
</html>
""")

    return "\n".join(out)
