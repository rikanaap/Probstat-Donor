"""Perbandingan antar kelompok (nonparametrik)."""
from itertools import combinations
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests


def kruskal(df: pd.DataFrame, value: str, group: str) -> dict:
    groups = [g[value].values for _, g in df.groupby(group)]
    h, p = stats.kruskal(*groups)
    n, k = len(df), len(groups)
    return {"H": h, "p": p, "epsilon²": (h - k + 1) / (n - k)}


def pairwise(df: pd.DataFrame, value: str, group: str) -> pd.DataFrame:
    rows = [(a, b, stats.mannwhitneyu(df[df[group] == a][value], df[df[group] == b][value]).pvalue)
            for a, b in combinations(sorted(df[group].unique()), 2)]
    out = pd.DataFrame(rows, columns=["Kelompok A", "Kelompok B", "p mentah"])
    out["p Holm"] = multipletests(out["p mentah"], method="holm")[1]
    return out
