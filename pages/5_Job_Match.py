# ==========================================================
# match_engine.py — Engine responsável por:
# 1) Normalização dos dados selecionados pelo usuário
# 2) Validação de campos obrigatórios
# 3) Cálculo do score baseado em pesos
# 4) Seleção do melhor Job Profile
# ==========================================================

import pandas as pd

# ----------------------------------------------------------
# VALORES PADRONIZADOS (para normalização)
# ----------------------------------------------------------
def normalize(value):
    """Converte None, vazio, placeholder em vazio real."""
    if value is None:
        return ""
    if isinstance(value, str) and value.strip().lower() in ["choose option", "select option", ""]:
        return ""
    return value


# ----------------------------------------------------------
# LISTA DE CAMPOS OBRIGATÓRIOS NO FORMULÁRIO
# (Eles devem ser exatamente os mesmos nomes usados no 5_Job_Match)
# ----------------------------------------------------------
REQUIRED_FIELDS = [
    "Job Family",
    "Sub Job Family",
    "Job Category",
    "Span of Control",
    "Financial Impact",
    "Geographic Scope",
    "Stakeholder Complexity",
    "Organizational Impact",
    "Nature of Work",
    "Decision Type",
    "Decision Time Horizon",
    "Autonomy Level",
    "Knowledge Depth",
    "Problem Solving Complexity",
    "Operational Complexity",
    "Influence Level",
    "Education Level",
    "Experience Level",
    "Specialization Level",
    "Innovation Responsibility",
    "Leadership Type",
    "Organizational Influence"
]


# ----------------------------------------------------------
# FUNÇÃO: validar campos
# Retorna:
#   (is_valid, missing_fields)
# ----------------------------------------------------------
def validate_user_inputs(user_inputs: dict):
    missing = [f for f in REQUIRED_FIELDS if normalize(user_inputs.get(f, "")) == ""]
    return len(missing) == 0, missing


# ----------------------------------------------------------
# DICIONÁRIO DE PESOS
# (Peso maior = maior impacto no match)
# ----------------------------------------------------------
WEIGHTS = {
    "Job Category": 4,
    "Span of Control": 4,
    "Financial Impact": 4,
    "Geographic Scope": 3,
    "Organizational Impact": 3,
    "Stakeholder Complexity": 3,
    "Decision Type": 3,
    "Decision Time Horizon": 3,
    "Nature of Work": 2,
    "Autonomy Level": 2,
    "Problem Solving Complexity": 2,
    "Knowledge Depth": 2,
    "Operational Complexity": 2,
    "Influence Level": 2,
    "Experience Level": 2,
    "Specialization Level": 1,
    "Innovation Responsibility": 1,
    "Education Level": 1,
    "Leadership Type": 1,
    "Organizational Influence": 1,
}


# ----------------------------------------------------------
# FUNÇÃO PRINCIPAL: gerar match e score
# ----------------------------------------------------------
def compute_match(user_inputs: dict, df_profiles: pd.DataFrame):
    """
    user_inputs = dicionário com todos os valores selecionados
    df_profiles = dataframe carregado do Job Profile.xlsx
    """

    # Normalize inputs
    ui = {k: normalize(v) for k, v in user_inputs.items()}

    # VALIDAÇÃO
    valid, missing = validate_user_inputs(ui)
    if not valid:
        return None, missing

    # Agora começamos a calcular o score
    scores = []

    for idx, row in df_profiles.iterrows():

        profile_score = 0
        max_score = 0

        # Vamos comparar campo a campo
        for field, weight in WEIGHTS.items():
            max_score += weight

            # EXEMPLO:
            # Campo "Job Category" mapeia para coluna "job_category"
            df_col = field.lower().replace(" ", "_")

            # Se o dataframe não tiver a coluna, ignora
            if df_col not in df_profiles.columns:
                continue

            profile_value = normalize(row[df_col])
            user_value = ui[field]

            # Score: bateu exatamente → ganha peso
            if profile_value == user_value:
                profile_score += weight

        # Normaliza score final (%)
        final_percentage = int((profile_score / max_score) * 100)

        scores.append({
            "profile_index": idx,
            "Job Profile": row["job_profile"],
            "Job Family": row["job_family"],
            "Sub Job Family": row["sub_job_family"],
            "Career Path": row["career_path"],
            "Full Job Code": row["full_job_code"],
            "score": final_percentage,
        })

    # Ordena do maior score para o menor
    scores_sorted = sorted(scores, key=lambda x: x["score"], reverse=True)

    # Melhor match
    best = scores_sorted[0] if scores_sorted else None

    return best, []
