# match_engine.py
from typing import Dict, Any, Optional

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def _build_profiles_text(df_profiles: pd.DataFrame) -> pd.Series:
    """
    Constrói uma coluna de texto único para cada linha,
    concatenando TODAS as colunas textuais (dtype object).
    """

    # Todas as colunas textuais possíveis
    text_cols = [c for c in df_profiles.columns if df_profiles[c].dtype == "object"]

    def row_to_text(row):
        parts = []
        for col in text_cols:
            val = row.get(col, "")
            if pd.notna(val) and str(val).strip():
                parts.append(str(val))
        return " ".join(parts)

    return df_profiles.apply(row_to_text, axis=1)


def _build_query_text(form_inputs: Dict[str, Any]) -> str:
    """
    Constrói o texto da query a partir de TODOS os campos do formulário.
    Aceita strings, listas (multiselect), etc.
    """

    parts = []

    for key, val in form_inputs.items():
        if val is None:
            continue

        # multiselect (lista)
        if isinstance(val, (list, tuple, set)):
            for v in val:
                if v:
                    parts.append(str(v))
        else:
            if str(val).strip():
                parts.append(str(val))

    return " ".join(parts)


def compute_job_match(
    form_inputs: Dict[str, Any],
    df_profiles: pd.DataFrame,
    min_score: float = 0.0,
) -> Optional[Dict[str, Any]]:
    """
    Compara a descrição do formulário com TODOS os perfis da planilha
    usando TF-IDF + similaridade de cosseno, considerando todas as
    colunas textuais possíveis do df_profiles.

    Retorna:
        None se nenhum match for relevante
        ou
        {
            "row": <pandas.Series do melhor match>,
            "final_score": <float com o score de similaridade>
        }
    """

    if df_profiles.empty:
        return None

    # Texto de cada perfil
    profiles_text = _build_profiles_text(df_profiles)

    # Vetoriza perfis
    vectorizer = TfidfVectorizer()
    matrix_profiles = vectorizer.fit_transform(profiles_text.fillna(""))

    # Texto da query com TODOS os campos do formulário
    query_text = _build_query_text(form_inputs)
    if not query_text.strip():
        return None

    query_vec = vectorizer.transform([query_text])
    scores = linear_kernel(query_vec, matrix_profiles).flatten()

    best_idx = scores.argmax()
    best_score = float(scores[best_idx])

    if best_score < min_score:
        return None

    best_row = df_profiles.iloc[best_idx]

    return {
        "row": best_row,
        "final_score": best_score,
    }
