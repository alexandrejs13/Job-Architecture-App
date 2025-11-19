# ==========================================================
# NOVO MATCH ENGINE (TF-IDF COM TODAS AS COLUNAS TEXTUAIS)
# ==========================================================
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def build_profiles_text(df_profiles: pd.DataFrame) -> pd.Series:
    """Concatena todas as colunas textuais possíveis em um único texto por linha."""
    text_cols = [c for c in df_profiles.columns if df_profiles[c].dtype == "object"]

    def join_row(row):
        parts = []
        for col in text_cols:
            val = row.get(col, "")
            if pd.notna(val) and str(val).strip():
                parts.append(str(val))
        return " ".join(parts)

    return df_profiles.apply(join_row, axis=1)


def build_query_text(inputs: dict) -> str:
    """Concatena todo o conteúdo do formulário em um único texto."""
    chunks = []
    for k, v in inputs.items():
        if v and v != "Choose option":
            chunks.append(str(v))
    return " ".join(chunks)


def compute_job_match(inputs: dict, df_profiles: pd.DataFrame):
    """Retorna o perfil mais parecido usando TF-IDF + cosseno."""
    if df_profiles.empty:
        return None

    profiles_text = build_profiles_text(df_profiles)

    vectorizer = TfidfVectorizer()
    M = vectorizer.fit_transform(profiles_text.fillna(""))

    query = build_query_text(inputs)
    if not query.strip():
        return None

    qv = vectorizer.transform([query])
    sims = linear_kernel(qv, M).flatten()

    best_idx = sims.argmax()
    best_score = float(sims[best_idx])

    return {
        "row": df_profiles.iloc[best_idx],
        "score": best_score,
    }
