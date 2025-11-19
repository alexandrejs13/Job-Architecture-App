# html_renderer.py
import html
import os
import pandas as pd

# ---------------------------------------------------------
# Carrega SVGs da pasta /assets/icons/sig/
# ---------------------------------------------------------
def load_svg(svg_name: str) -> str:
    path = os.path.join("assets", "icons", "sig", svg_name)
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        svg = f.read()
        svg = svg.replace('<?xml version="1.0" encoding="utf-8"?>', '')
        return svg

ICONS = {
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

SECTIONS_ORDER = list(ICONS.keys())

# ---------------------------------------------------------
# HTML FINAL — IDÊNTICO AO JOB PROFILE DESCRIPTION
# ---------------------------------------------------------
def render_job_description(row: pd.Series, score_pct: int) -> str:

    job_title = html.escape(row.get("Job Profile", ""))
    gg = html.escape(str(row.get("Global Grade", "")))

    jf = html.escape(row.get("Job Family", ""))
    sf = html.escape(row.get("Sub Job Family", ""))
    cp = html.escape(row.get("Career Path", ""))
    fc = html.escape(row.get("Full Job Code", ""))

    # -----------------------------------------------------
    # HTML completo
    # -----------------------------------------------------
    return f"""
<html>
<head>
<meta charset="UTF-8">
<style>

html, body {{
    margin: 0;
    padding: 0;
    background: #ffffff;
    font-family: 'Segoe UI', sans-serif;
}}

.container {{
    width: 100%;
    margin-top: 10px;
}}

.card-top {{
    background: #f5f3ee;
    border-radius: 16px;
    padding: 26px 28px;
    border: 1px solid #e3e1dd;
    margin-bottom: 28px;
}}

.title {{
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 6px;
}}

.gg {{
    color: #145efc;
    font-size: 18px;
    font-weight: 700;
    margin-top: 2px;
}}

.match-pill {{
    display: inline-block;
    background: #145efc;
    color: white;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 14px;
    font-weight: 600;
    margin-left: 8px;
}}

.meta {{
    background: #ffffff;
    padding: 16px;
    margin-top: 18px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    font-size: 15px;
    line-height: 1.5;
}}

.section {{
    margin-bottom: 34px;
}}

.section-title {{
    font-size: 18px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 6px;
}}

.section-title svg {{
    width: 22px;
    height: 22px;
}}

.section-line {{
    width: 100%;
    height: 1px;
    background: #e8e6e1;
    margin: 10px 0 14px 0;
}}

.section-text {{
    font-size: 15px;
    line-height: 1.55;
    white-space: pre-wrap;
}}

</style>
</head>

<body>

<div class="container">

    <div class="card-top">
        <div class="title">{job_title}</div>

        <div class="gg">
            GG {gg}
            <span class="match-pill">{score_pct}% Match</span>
        </div>

        <div class="meta">
            <b>Job Family:</b> {jf}<br>
            <b>Sub Job Family:</b> {sf}<br>
            <b>Career Path:</b> {cp}<br>
            <b>Full Job Code:</b> {fc}
        </div>
    </div>

    <!-- SEÇÕES -->
    <div class="sections">
"""

    + "\n".join([
        f"""
        <div class="section">
            <div class="section-title">{ICONS.get(sec, '')} {html.escape(sec)}</div>
            <div class="section-line"></div>
            <div class="section-text">{html.escape(str(row.get(sec, '')))}</div>
        </div>
        """
        for sec in SECTIONS_ORDER
    ]) + """

    </div>
</div>

</body>
</html>
"""

