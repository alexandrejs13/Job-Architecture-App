import streamlit as st
import pandas as pd
from pathlib import Path
import html

st.set_page_config(page_title="Job Profile Description", layout="wide")

# ============================
# PAGE TITLE
# ============================
st.markdown("""
<h1 style="font-size:38px; font-weight:700; margin-bottom:6px;">
    Job Profile Description
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* GLOBAL */
body, html, [data-testid="stAppViewContainer"] {
    font-family: 'Segoe UI', sans-serif;
}

/* STICKY HEADER INSIDE SCROLL CONTAINER */
.profile-header {
    position: sticky;
    top: 0;
    background: white;
    padding: 14px;
    border-bottom: 1px solid #e6e6e6;
    z-index: 10;
}

/* METADATA BOX */
.meta-box {
    background: #f5f4f1;
    padding: 12px;
    border-radius: 10px;
    font-size: 0.92rem;
}

/* COLUMN CARD */
.profile-card {
    background: white;
    border: 1px solid #e6e6e6;
    border-radius: 14px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
    display: flex;
    flex-direction: column;
    height: max-content;
}

/* DESCRIPTION SECTION */
.desc-section {
    padding: 14px;
    border-bottom: 1px solid #eaeaea;
}
.desc-section:last-child {
    border-bottom: none;
}

/* MAIN SCROLL AREA */
#scroll-area {
    height: 76vh;              /* SCROLL ÁREA */
    overflow-y: auto;
    padding-right: 6px;
    margin-top: 18px;
}

/* GRID */
.grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 26px;
}
.grid-2 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 26px;
}
.grid-1 {
    display: grid;
    grid-template-columns: 1fr;
    gap: 26px;
}
</style>
""", unsafe_allow_html=True)

# ============================
# LOAD DATA
# ============================
@st.cache_data(ttl=600)
def load_data():
    p = Path("data")/"Job Profile.xlsx"
    if not p.exists(): return pd.DataFrame()
    df = pd.read_excel(p)
    df.columns = df.columns.str.strip()
    return df

df = load_data()
if df.empty:
    st.error("Could not load Job Profile.xlsx")
    st.stop()

# ============================
# FILTERS
# ============================
st.subheader("🔍 Job Profile Description Explorer")

families = sorted(df["Job Family"].dropna().unique())

col1, col2, col3 = st.columns(3)

with col1:
    family = st.selectbox("Job Family", ["Select..."] + families)

with col2:
    subs = sorted(df[df["Job Family"] == family]["Sub Job Family"].dropna().unique()) if family!="Select..." else []
    subfam = st.selectbox("Sub Job Family", ["Select..."] + subs)

with col3:
    paths = sorted(df[df["Sub Job Family"] == subfam]["Career Path"].dropna().unique()) if subfam!="Select..." else []
    cpath = st.selectbox("Career Path", ["Select..."] + paths)

flt = df.copy()
if family!="Select...": flt = flt[flt["Job Family"]==family]
if subfam!="Select...": flt = flt[flt["Sub Job Family"]==subfam]
if cpath!="Select...": flt = flt[flt["Career Path"]==cpath]

flt["label"] = flt.apply(lambda r: f"GG {str(r['Global Grade']).replace('.0','')} • {r['Job Profile']}", axis=1)

selected = st.multiselect("Select up to 3 profiles:", flt["label"].tolist(), max_selections=3)

if not selected:
    st.stop()

profiles = [flt[flt["label"]==s].iloc[0].to_dict() for s in selected]
cols = len(profiles)

# grid class
grid_class = "grid-1" if cols==1 else ("grid-2" if cols==2 else "grid-3")

# ============================
# RENDER PROFILES (INSIDE SCROLL AREA)
# ============================
html_cards = f'<div id="scroll-area"><div class="{grid_class}">'

for p in profiles:
    job = html.escape(str(p["Job Profile"]))
    gg = html.escape(str(p["Global Grade"])).replace(".0","")

    html_cards += f"""
    <div class="profile-card">

        <div class="profile-header">
            <div style="font-size:22px; font-weight:700;">{job}</div>
            <div style="font-size:18px; font-weight:700; color:#145efc;">GG {gg}</div>

            <div class="meta-box" style="margin-top:10px;">
                <b>Job Family:</b> {html.escape(str(p["Job Family"]))}<br>
                <b>Sub Job Family:</b> {html.escape(str(p["Sub Job Family"]))}<br>
                <b>Career Path:</b> {html.escape(str(p["Career Path"]))}<br>
                <b>Full Job Code:</b> {html.escape(str(p["Full Job Code"]))}
            </div>
        </div>
    """

    # descriptions
    for sec in [
        "Sub Job Family Description", "Job Profile Description",
        "Career Band Description", "Role Description",
        "Grade Differentiator", "Qualifications",
        "Specific parameters / KPIs", "Competencies 1",
        "Competencies 2", "Competencies 3"
    ]:
        v = str(p.get(sec,"")).strip()
        if v and v.lower()!="nan":
            html_cards += f"""
            <div class="desc-section">
                <div style="font-weight:700; margin-bottom:4px;">{sec}</div>
                <div style="font-size:0.92rem; line-height:1.38;">{html.escape(v)}</div>
            </div>
            """

    html_cards += "</div>"  # end profile-card

html_cards += "</div></div>"

st.markdown(html_cards, unsafe_allow_html=True)
