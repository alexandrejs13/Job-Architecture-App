import streamlit as st
import pandas as pd
import html
import streamlit.components.v1 as components

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Job Profile Description", layout="wide")

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown("""
<h1 style="font-size:36px; font-weight:700; margin-bottom:4px;">
    Job Profile Description
</h1>
<hr style="margin-top:0;">
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_profiles():
    return pd.read_excel("data/Job Profile.xlsx")

df = load_profiles()

# ---------------------------------------------------------
# FILTERS
# ---------------------------------------------------------
st.subheader("🔍 Job Profile Description Explorer")

c1, c2, c3 = st.columns(3)

with c1:
    job_family = st.selectbox("Job Family",
        ["All"] + sorted(df["Job Family"].dropna().unique()))

with c2:
    subfam_list = (
        df[df["Job Family"] == job_family]["Sub Job Family"].dropna().unique()
        if job_family != "All"
        else df["Sub Job Family"].dropna().unique()
    )
    sub_family = st.selectbox("Sub Job Family",
        ["All"] + sorted(subfam_list))

with c3:
    path_list = (
        df[df["Sub Job Family"] == sub_family]["Career Path"].dropna().unique()
        if sub_family != "All"
        else df["Career Path"].dropna().unique()
    )
    career_path = st.selectbox("Career Path",
        ["All"] + sorted(path_list))

flt = df.copy()

if job_family != "All":
    flt = flt[flt["Job Family"] == job_family]
if sub_family != "All":
    flt = flt[flt["Sub Job Family"] == sub_family]
if career_path != "All":
    flt = flt[flt["Career Path"] == career_path]

flt["label"] = flt["Global Grade"].astype(str) + " • " + flt["Job Profile"]

selected = st.multiselect("Select up to 3 profiles:",
    flt["label"].tolist(), max_selections=3)

if not selected:
    st.stop()

profiles = [flt[flt["label"] == s].iloc[0].to_dict() for s in selected]

# ---------------------------------------------------------
# SECTIONS
# ---------------------------------------------------------
sections = [
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

icons = {
    "Sub Job Family Description": "Hierarchy.svg",
    "Job Profile Description": "File_Clipboard_Text.svg",
    "Career Band Description": "Hierarchy.svg",
    "Role Description": "Shopping_Business_Suitcase.svg",
    "Grade Differentiator": "Edit_Pencil.svg",
    "Qualifications": "Content_Book_Phone.svg",
    "Specific parameters / KPIs": "Graph_Bar.svg",
    "Competencies 1": "Setting_Cog.svg",
    "Competencies 2": "Setting_Cog.svg",
    "Competencies 3": "Setting_Cog.svg",
}

# ---------------------------------------------------------
# HTML — versão topo minimalista
# ---------------------------------------------------------
def build_html(profiles):

    n = len(profiles)

    html_code = f"""
<html>
<head>
<meta charset="UTF-8">

<style>

html, body {{
    margin: 0;
    padding: 0;
    height: 100%;
    overflow: hidden;
    font-family: 'Segoe UI', sans-serif;
}}

#viewport {{
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

/* TOP FIXO — sem sombra */
#top-area {{
    background: white;
    padding: 12px 18px;
    position: sticky;
    top: 0;
    z-index: 20;
    box-shadow: none;
}}

.grid-top {{
    display: grid;
    grid-template-columns: repeat({n}, 1fr);
    gap: 24px;
}}

.card-top {{
    padding: 12px;
    border-radius: 16px;
}}

.title {{
    font-size: 21px;
    font-weight: 700;
    line-height: 1.15;
}}

.gg {{
    color: #145efc;
    font-size: 18px;
    font-weight: 700;
    margin-top: 4px;
}}

.meta-line {{
    font-size: 15px;
    margin-top: 2px;
}}

#scroll-area {{
    flex: 1;
    overflow-y: auto;
    padding: 20px;
}}

.grid-row {{
    display: grid;
    grid-template-columns: repeat({n}, 1fr);
    gap: 24px;
}}

.cell {{
    background: white;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}}

.section-title {{
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 6px;
    display: flex;
    gap: 8px;
    align-items: center;
}}

.section-title img {{
    width: 20px;
}}

.text {{
    font-size: 15px;
    line-height: 1.45;
    white-space: pre-wrap;
}}

</style>
</head>

<body>
<div id="viewport">

    <div id="top-area">
        <div class="grid-top">
    """

    # ------------------ TOP CARDS CLEAN ------------------
    for p in profiles:
        job = html.escape(p["Job Profile"])
        gg = html.escape(str(p["Global Grade"]))
        jf = html.escape(p["Job Family"])
        sf = html.escape(p["Sub Job Family"])
        cp = html.escape(p["Career Path"])
        fc = html.escape(p["Full Job Code"])

        html_code += f"""
        <div class="card-top">
            <div class="title">{job}</div>
            <div class="gg">GG {gg}</div>

            <div class="meta-line"><b>Job Family:</b> {jf}</div>
            <div class="meta-line"><b>Sub Job Family:</b> {sf}</div>
            <div class="meta-line"><b>Career Path:</b> {cp}</div>
            <div class="meta-line"><b>Full Job Code:</b> {fc}</div>
        </div>
        """

    html_code += """
        </div>
    </div>

    <div id="scroll-area">
    """

    # ------------------ SEÇÕES ALINHADAS ------------------
    for sec in sections:
        html_code += f"""<div class="grid-row">"""

        for p in profiles:
            val = p.get(sec, "")
            icon = icons[sec]

            html_code += f"""
            <div class="cell">
                <div class="section-title">
                    <img src="assets/icons/sig/{icon}">
                    {html.escape(sec)}
                </div>
                <div class="text">{html.escape(str(val))}</div>
            </div>
            """
        html_code += "</div>"

    html_code += """
    </div>

</div>
</body>
</html>
"""

    return html_code


components.html(build_html(profiles), height=900, scrolling=False)
