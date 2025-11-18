import streamlit as st
import pandas as pd
import html
import streamlit.components.v1 as components

# -------------------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------------------
st.set_page_config(page_title="Job Profile Description", layout="wide")

# -------------------------------------------------------------------
# HEADER
# -------------------------------------------------------------------
st.markdown("""
<h1 style="font-size:36px; font-weight:700; margin-bottom:5px;">
    Job Profile Description
</h1>
<hr style="margin-top:0;">
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------------------
@st.cache_data
def load_profiles():
    return pd.read_excel("data/Job Profile.xlsx")

df = load_profiles()

# -------------------------------------------------------------------
# FILTERS
# -------------------------------------------------------------------
st.subheader("🔍 Job Profile Description Explorer")

f1, f2, f3 = st.columns(3)

with f1:
    jf = st.selectbox("Job Family",
                      ["All"] + sorted(df["Job Family"].dropna().unique()))

with f2:
    sf_list = df[df["Job Family"] == jf]["Sub Job Family"].dropna().unique() if jf != "All" else df["Sub Job Family"].dropna().unique()
    sf = st.selectbox("Sub Job Family",
                      ["All"] + sorted(sf_list))

with f3:
    cp_list = df[df["Sub Job Family"] == sf]["Career Path"].dropna().unique() if sf != "All" else df["Career Path"].dropna().unique()
    cp = st.selectbox("Career Path",
                      ["All"] + sorted(cp_list))

flt = df.copy()

if jf != "All":
    flt = flt[flt["Job Family"] == jf]
if sf != "All":
    flt = flt[flt["Sub Job Family"] == sf]
if cp != "All":
    flt = flt[flt["Career Path"] == cp]

flt["label"] = flt["GG"].astype(str) + " • " + flt["Job Profile"]

selected = st.multiselect("Select up to 3 profiles:", flt["label"].tolist(), max_selections=3)

if not selected:
    st.stop()

profiles = [flt[flt["label"] == s].iloc[0].to_dict() for s in selected]

# -------------------------------------------------------------------
# SECTIONS (STATIC ORDER)
# -------------------------------------------------------------------
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
    "Competencies 3"
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

# -------------------------------------------------------------------
# BUILD HTML
# -------------------------------------------------------------------
def build_html(profiles):

    n = len(profiles)

    html_code = f"""
    <html>
    <head>
    <style>

    body {{
        margin: 0;
        padding: 0;
        font-family: 'Segoe UI', sans-serif;
        background: white;
    }}

    /* WRAPPER FORÇANDO O STICKY FUNCIONAR */
    #wrap {{
        height: auto !important;
        overflow: visible !important;
    }}

    /* GRID */
    .grid {{
        display: grid;
        grid-template-columns: repeat({n}, 1fr);
        gap: 32px;
        width: 100%;
    }}

    /* CARD SUPERIOR (STICKY) */
    .card-top {{
        background: white;
        border-radius: 16px;
        padding: 22px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.10);
        position: sticky;
        top: 0;
        z-index: 50;
    }}

    .title {{
        font-size: 22px;
        font-weight: 700;
    }}

    .gg {{
        color: #145efc;
        font-weight: 700;
        font-size: 18px;
        margin-top: 8px;
    }}

    .meta {{
        background: #f5f3ef;
        padding: 14px;
        border-radius: 12px;
        font-size: 15px;
        margin-top: 14px;
        line-height: 1.45;
        border: 1px solid #e8e6e2;
    }}

    /* CARD INFERIOR */
    .card-desc {{
        background: white;
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        margin-bottom: 42px;
    }}

    .section-title {{
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .section-title img {{
        width: 20px;
    }}

    .text {{
        white-space: pre-wrap;
        line-height: 1.45;
        margin-bottom: 18px;
    }}

    .scroll-page {{
        height: 1500px;  /* TELA LONGA */
        overflow-y: auto;
        overflow-x: hidden;
        padding-right: 15px;
        margin-top: 20px;
    }}

    </style>
    </head>

    <body>
    <div id="wrap">

        <!-- GRID DOS TOP CARDS (STICKY) -->
        <div class="grid">
    """

    # ---------- TOP CARDS ----------
    for p in profiles:
        job = html.escape(str(p["Job Profile"]))
        gg = html.escape(str(p["GG"]))
        jf = html.escape(str(p["Job Family"]))
        sf = html.escape(str(p["Sub Job Family"]))
        cp = html.escape(str(p["Career Path"]))
        fc = html.escape(str(p["Full Job Code"]))

        html_code += f"""
        <div class="card-top">
            <div class="title">{job}</div>
            <div class="gg">GG {gg}</div>

            <div class="meta">
                <b>Job Family:</b> {jf}<br>
                <b>Sub Job Family:</b> {sf}<br>
                <b>Career Path:</b> {cp}<br>
                <b>Full Job Code:</b> {fc}
            </div>
        </div>
        """

    html_code += """
        </div>  <!-- end grid -->
    """

    # ---------- MAIN SCROLL AREA ----------
    html_code += """
        <div class="scroll-page">
            <div class="grid">
    """

    # ---------- DESCRIPTION CARDS ----------
    for p in profiles:
        html_code += "<div class='card-desc'>"

        for sec in sections:
            val = p.get(sec, "")
            if not val or str(val).strip() == "":
                continue

            icon = icons[sec]

            html_code += f"""
                <div class="section-title">
                    <img src="assets/icons/sig/{icon}">
                    {html.escape(sec)}
                </div>
                <div class="text">
                    {html.escape(str(val))}
                </div>
            """

        html_code += "</div>"

    html_code += """
            </div>
        </div> <!-- end scroll-page -->

    </div>
    </body>
    </html>
    """

    return html_code

# -------------------------------------------------------------------
# RENDER HTML FINAL
# -------------------------------------------------------------------
components.html(build_html(profiles), height=1800, scrolling=False)
