def build_html(profiles):

    n = len(profiles)

    html_code = f"""
    <html>
    <head>
    <style>

    html, body {{
        margin: 0;
        padding: 0;
        overflow: hidden;
        font-family: 'Segoe UI', sans-serif;
    }}

    /* WRAPPER GERAL – DUAS ÁREAS: TOP (sticky) + SCROLL AREA */
    #layout {{
        display: flex;
        flex-direction: column;
        height: 100vh;
    }}

    /* BARRA SUPERIOR CONGELADA */
    #top-block {{
        position: sticky;
        top: 0;
        z-index: 100;
        background: white;
        padding-bottom: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.10);
    }}

    /* GRID DO TOPO */
    .grid-top {{
        display: grid;
        grid-template-columns: repeat({n}, 1fr);
        gap: 28px;
        padding: 16px;
    }}

    .card-top {{
        background: white;
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.12);
    }}

    .title {{
        font-size: 22px;
        font-weight: 700;
    }}

    .gg {{
        color: #145efc;
        font-size: 18px;
        font-weight: 700;
        margin-top: 8px;
    }}

    .meta {{
        background: #f5f3ee;
        border: 1px solid #e3e1dd;
        border-radius: 12px;
        padding: 14px;
        margin-top: 14px;
        font-size: 15px;
        line-height: 1.45;
    }}

    /* ÁREA INFERIOR ROLÁVEL UNIFICADA */
    #scroll-block {{
        flex: 1;
        overflow-y: auto;
        padding: 24px;
    }}

    .grid-desc {{
        display: grid;
        grid-template-columns: repeat({n}, 1fr);
        gap: 28px;
    }}

    .card-desc {{
        background: white;
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
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
        font-size: 15px;
        line-height: 1.45;
        margin-bottom: 18px;
        white-space: pre-wrap;
    }}

    </style>
    </head>

    <body>

    <div id="layout">

        <!-- ÁREA DE CIMA CONGELADA -->
        <div id="top-block">
            <div class="grid-top">
    """

    # ---------- TOP CARDS ----------
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

            <div class="meta">
                <b>Job Family:</b> {jf}<br>
                <b>Sub Job Family:</b> {sf}<br>
                <b>Career Path:</b> {cp}<br>
                <b>Full Job Code:</b> {fc}
            </div>
        </div>
        """

    html_code += """
            </div>
        </div>

        <!-- ÁREA ROLÁVEL UNIFICADA -->
        <div id="scroll-block">
            <div class="grid-desc">
    """

    # ---------- DESCRIPTIONS ----------
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
                <div class="text">{html.escape(str(val))}</div>
            """

        html_code += "</div>"

    html_code += """
            </div>
        </div>

    </div>

    </body>
    </html>
    """

    return html_code
