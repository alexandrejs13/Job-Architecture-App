html_final = f"""
<html>
<head>
<style>

html, body, #wrap {{
    margin: 0;
    padding: 0;
    height: auto !important;
    overflow: visible !important;
}}

.grid {{
    display: grid;
    gap: 24px;
    grid-template-columns: repeat({len(profiles)}, 1fr);
}}

.card {{
    background: #fff;
    border-radius: 16px;
    border: 1px solid #ddd;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
    overflow: visible !important;
    display: flex;
    flex-direction: column;
}}

.header {{
    position: sticky;
    top: 0;
    background: #fff;
    padding: 24px;
    border-bottom: 1px solid #eee;
    z-index: 50;
}}

.title {{
    font-size: 23px;
    font-weight: 700;
    margin-bottom: 6px;
}}

.gg {{
    font-size: 17px;
    font-weight: 700;
    color: #145efc;
    margin-bottom: 16px;
}}

.meta {{
    background: #f7f5ef;
    padding: 14px;
    border-radius: 10px;
}}

.body {{
    padding: 22px;
    overflow: visible !important;
}}

.section {{
    margin-bottom: 22px;
    padding-bottom: 16px;
    border-bottom: 1px solid #f1f1f1;
}}

.section-title {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 600;
}}

.section-title img {{
    width: 20px;
}}

.text {{
    margin-top: 8px;
    white-space: pre-wrap;
    line-height: 1.45;
}}

</style>
</head>

<body>
<div id="wrap">
<div class="grid">
"""

for p in profiles:

    job = html.escape(p["Job Profile"])
    gg  = str(p["Global Grade"]).replace(".0","")
    jf  = html.escape(p["Job Family"])
    sf  = html.escape(p["Sub Job Family"])
    cp  = html.escape(p["Career Path"])
    fc  = html.escape(p["Full Job Code"])


    html_final += f"""
    <div class="card">

        <div class="header">
            <div class="title">{job}</div>
            <div class="gg">GG {gg}</div>
            <div class="meta">
                <b>Job Family:</b> {jf}<br>
                <b>Sub Job Family:</b> {sf}<br>
                <b>Career Path:</b> {cp}<br>
                <b>Full Job Code:</b> {fc}
            </div>
        </div>

        <div class="body">
    """

    for sec in sections:
        val = p.get(sec, "")
        if not val or str(val).strip() == "":
            continue

        icon = icons[sec]

        html_final += f"""
        <div class="section">
            <div class="section-title">
                <img src="assets/icons/sig/{icon}">
                {html.escape(sec)}
            </div>
            <div class="text">{html.escape(str(val))}</div>
        </div>
        """

    html_final += "</div></div>"

html_final += """
</div></div>
</body>
</html>
"""

components.html(html_final, height=2000, scrolling=True)
