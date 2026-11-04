"""Perhitungan ukuran sampel dan pemisahan sesi."""
from math import ceil
import pandas as pd
from scipy.stats import norm


def cochran(N: int, e: float = 0.10, conf: float = 0.95, p: float = 0.5) -> int:
    """Cochran dengan koreksi populasi hingga."""
    if N <= 0:
        return 0
    z = norm.ppf(1 - (1 - conf) / 2)
    n0 = z**2 * p * (1 - p) / e**2
    return min(N, ceil(n0 / (1 + (n0 - 1) / N)))


def slovin(N: int, e: float = 0.10) -> int:
    return 0 if N <= 0 else min(N, ceil(N / (1 + N * e**2)))


def sampling_interval(N: int, n: int) -> int:
    """Setiap donor ke-k diberi form (sampel sistematis)."""
    return max(1, N // n) if n > 0 else 0


def min_for_regression(k_items: int, per_item: int = 10) -> int:
    return k_items * per_item


def assign_session(hour: int, sessions: dict) -> str:
    for name, (start, end) in sessions.items():
        if start <= hour < end:
            return name
    return "Di luar sesi"


def count_by_session(timestamps: pd.Series, sessions: dict) -> dict:
    hours = pd.to_datetime(timestamps, errors="coerce").dropna().dt.hour
    labels = hours.map(lambda h: assign_session(h, sessions))
    return labels.value_counts().to_dict()


def sample_table(counts: dict, e: float, conf: float, k_items: int) -> pd.DataFrame:
    rows = []
    for name, N in counts.items():
        n = cochran(N, e, conf)
        rows.append({"Sesi": name, "Populasi (N)": N, "Cochran": n,
                     "Slovin": slovin(N, e), "Interval (tiap ke-k)": sampling_interval(N, n),
                     "Cukup untuk regresi?": n >= min_for_regression(k_items)})
    return pd.DataFrame(rows)
