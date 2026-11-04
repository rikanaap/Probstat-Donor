"""Reliabilitas instrumen."""
import pandas as pd


def cronbach_alpha(df: pd.DataFrame) -> float:
    k = df.shape[1]
    total_var = df.sum(axis=1).var(ddof=1)
    return float("nan") if k < 2 or total_var == 0 else k / (k - 1) * (1 - df.var(ddof=1).sum() / total_var)


def item_total(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for c in df.columns:
        rest = df.drop(columns=c)
        rows.append({"Item": c, "r item-total (terkoreksi)": df[c].corr(rest.sum(axis=1)),
                     "Alpha jika dihapus": cronbach_alpha(rest) if rest.shape[1] >= 2 else float("nan")})
    return pd.DataFrame(rows)
