import pandas as pd

def render_job_description(best_match_row: pd.Series, final_score: float) -> str:
    """
    Renderiza o cartão HTML do Job recomendado.
    best_match_row é uma linha (Series) do DataFrame final.
    """

    # Garantir fallback limpo
    def safe(x):
        if pd.isna(x):
            return ""
        return str(x)

    job_title = safe(best_match_row.get("Job Profile"))
    gg = safe(best_match_row.get("GG"))
    job_family = safe(best_match_row.get("Job Family"))
    sub_family = safe(best_match_row.get("Sub Job Family"))
    job_category = safe(best_match_row.get("Job Category"))
    geo_scope = safe(best_match_row.get("Geo Scope"))
    org_impact = safe(best_match_row.get("Org Impact"))
    autonomy = safe(best_match_row.get("Autonomy"))
    knowledge_depth = safe(best_match_row.get("Knowledge Depth"))
    operational_complexity = safe(best_match_row.get("Operational Complexity"))
    experience = safe(best_match_row.get("Experience"))
    education = safe(best_match_row.get("Education"))

    description = safe(best_match_row.get("Description"))
    responsibilities = safe(best_match_row.get("Responsibilities"))
    qualifications = safe(best_match_row.get("Qualifications"))

    html = f"""
    <style>
        .ja-card {{
            background: #ffffff;
            border-radius: 14px;
            padding: 24px 28px;
            border: 1px solid #e6e6e6;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            font-family: PPSIGFlow, sans-serif;
            width: 100%;
        }}

        .ja-title {{
            font-size: 30px;
            font-weight: 700;
            margin-bottom: 4px;
        }}

        .ja-gg {{
            font-size: 18px;
            font-weight: 600;
            color: #555;
            margin-bottom: 12px;
        }}

        .ja-meta {{
            margin-top: 4px;
            margin-bottom: 22px;
            color: #444;
            font-size: 15px;
        }}

        .ja-section-title {{
            font-size: 20px;
            font-weight: 700;
            margin-top: 26px;
            margin-bottom: 6px;
        }}

        .ja-text {{
            font-size: 15px;
            line-height: 1.5;
            margin-bottom: 12px;
            white-space: pre-wrap;
        }}

        .ja-score {{
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 18px;
            color: #145efc;
        }}
    </style>

    <div class="ja-card">

        <div class="ja-title">{job_title}</div>
        <div class="ja-gg">Global Grade: {gg}</div>

        <div class="ja-score">
            🎯 Match Score: {final_score:.1f}%
        </div>

        <div class="ja-meta">
            <strong>Job Family:</strong> {job_family}<br>
            <strong>Sub Job Family:</strong> {sub_family}<br>
            <strong>Job Category:</strong> {job_category}<br>
            <strong>Geo Scope:</strong> {geo_scope}<br>
            <strong>Org Impact:</strong> {org_impact}<br>
            <strong>Autonomy:</strong> {autonomy}<br>
            <strong>Knowledge Depth:</strong> {knowledge_depth}<br>
            <strong>Operational Complexity:</strong> {operational_complexity}<br>
            <strong>Experience:</strong> {experience}<br>
            <strong>Education:</strong> {education}<br>
        </div>

        <div class="ja-section-title">Description</div>
        <div class="ja-text">{description}</div>

        <div class="ja-section-title">Responsibilities</div>
        <div class="ja-text">{responsibilities}</div>

        <div class="ja-section-title">Qualifications</div>
        <div class="ja-text">{qualifications}</div>

    </div>
    """

    return html
