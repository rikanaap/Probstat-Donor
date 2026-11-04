"""Menerjemahkan hasil hitung menjadi temuan yang mudah dibaca."""
import pandas as pd
from calc import comparison, config, regression, reliability

LABEL = config.ITEMS


def data_quality(df: pd.DataFrame) -> tuple:
    n = len(df)
    consistent = reliability.cronbach_alpha(df[list(LABEL)]) >= 0.6
    if n < 30:
        return "Kurang", f"Baru {n} jawaban. Kumpulkan lebih banyak sebelum mengambil keputusan."
    if not consistent:
        return "Perlu dicek", "Jawaban antar pertanyaan kurang sejalan. Cek apakah form diisi dengan sungguh-sungguh."
    if n < 100:
        return "Cukup", f"{n} jawaban. Cukup untuk gambaran awal."
    return "Baik", f"{n} jawaban. Cukup untuk dipakai sebagai dasar keputusan."


def item_scores(df: pd.DataFrame) -> pd.Series:
    return df[list(LABEL)].mean().rename(index=LABEL).round(2)


def priorities(df: pd.DataFrame, top: int = 3) -> list:
    pm = regression.priority_map(df, list(LABEL), config.OUTCOME)
    pm["urgensi"] = pm["Pengaruh (beta)"].clip(lower=0) * (5 - pm["Kinerja (rerata)"])
    best = pm.sort_values("urgensi", ascending=False).head(top)
    return [{"key": k, "item": LABEL[k], "skor": round(r["Kinerja (rerata)"], 1)} for k, r in best.iterrows()]


def session_summary(df: pd.DataFrame) -> dict:
    m = df.groupby(config.SESSION_COL)[config.SATISFACTION].mean()
    real = df[config.SESSION_COL].nunique() > 1 and comparison.kruskal(df, config.SATISFACTION, config.SESSION_COL)["p"] < 0.05
    return {"rendah": m.idxmin(), "tinggi": m.idxmax(), "nyata": bool(real), "skor": m.round(1).to_dict()}


def level(score: float) -> tuple:
    """Status skor: (teks, warna markdown Streamlit)."""
    if score >= 4:
        return "Baik", "green"
    return ("Cukup", "orange") if score >= 3.5 else ("Perlu perbaikan", "red")
