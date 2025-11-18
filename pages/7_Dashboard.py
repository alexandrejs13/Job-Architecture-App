# ==========================================================
# TAB 1 — OVERVIEW
# ==========================================================
with tab1:

    st.markdown("## Overview")

    # ---- KPI CARDS ----
    kpis = {
        "Families": df[COL_FAMILY].nunique(),
        "Subfamilies": df[COL_SUBFAMILY].nunique(),
        "Job Profiles": df[COL_PROFILE].nunique(),
        "Career Paths": df[COL_CAREER_PATH].nunique(),
        "Career Bands": df[COL_BAND].nunique(),
        "Global Grades": df[COL_GRADE].nunique(),
        "Avg Profiles / Family": round(df[COL_PROFILE].nunique() / df[COL_FAMILY].nunique(), 1),
        "Avg Profiles / Subfamily": round(df[COL_PROFILE].nunique() / df[COL_SUBFAMILY].nunique(), 1),
    }

    st.markdown("<div class='sig-card-grid'>", unsafe_allow_html=True)
    for title, value in kpis.items():
        st.markdown(
            f"""
            <div class='sig-card'>
                <div class='sig-card-title'>{title}</div>
                <div class='sig-card-value'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("</div>", unsafe_allow_html=True)


    # ==========================================================
    # DONUT — Subfamilies per Family (SIG)
    # ==========================================================
    st.markdown("<div class='block-space'></div>", unsafe_allow_html=True)
    st.markdown("## Subfamilies per Family")

    df_sub = (
        df.groupby(COL_FAMILY)[COL_SUBFAMILY]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    colA, colB = st.columns([1, 1])

    with colA:
        st.altair_chart(sig_donut_chart(df_sub, COL_FAMILY, "Count"),
                        use_container_width=True)

    with colB:
        sig_legend(df_sub, COL_FAMILY, "Count")


    # ==========================================================
    # BARRA HORIZONTAL SIG — Profiles per Subfamily
    # ==========================================================
    st.markdown("<div class='block-space'></div>", unsafe_allow_html=True)
    st.markdown("## Profiles per Subfamily")

    df_prof = (
        df.groupby(COL_SUBFAMILY)[COL_PROFILE]
        .nunique()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
    )

    colL, colR = st.columns([1.2, 1])

    with colL:
        bar = (
            alt.Chart(df_prof)
            .mark_bar(size=22)
            .encode(
                x=alt.X("Count:Q", title=""),
                y=alt.Y(COL_SUBFAMILY, sort='-x', title=""),
                color=alt.Color(COL_SUBFAMILY,
                                scale=alt.Scale(range=SIG_COLORS),
                                legend=None),
                tooltip=[COL_SUBFAMILY, "Count"],
            )
        )
        st.altair_chart(bar, use_container_width=True)

    with colR:
        sig_legend(df_prof, COL_SUBFAMILY, "Count")
