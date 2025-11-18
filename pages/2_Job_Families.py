def header(icon_path: str, title: str):
    st.markdown(f"""
        <div style="
            display:flex;
            align-items:center;
            gap:18px;
            padding: 4px 0 14px 0;
        ">
            <img src="{icon_path}" style="width:56px; height:56px;">
            <h1 style="margin:0; padding:0; font-size:36px; font-weight:700;">
                {title}
            </h1>
        </div>
        <hr style="margin-top:0;">
    """, unsafe_allow_html=True)
