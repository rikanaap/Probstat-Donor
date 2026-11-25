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


def sampling_interval(N: int, n: int) -> int:
    """Setiap donor ke-k diberi form (sampel sistematis)."""
    return max(1, N // n) if n > 0 else 0


def min_for_regression(k_items: int, rule: str = "green") -> int:
    """Minimum sampel untuk regresi linear dengan k prediktor.

    green  : max(50 + 8k, 104 + k)  (Green, 1991)
    ten_x  : 10 * k                 (rule of thumb, batas bawah)
    """
    if rule == "ten_x":
        return 10 * k_items
    return max(50 + 8 * k_items, 104 + k_items)


def assign_session(hour: int, sessions: dict) -> str:
    for name, (start, end) in sessions.items():
        if start <= hour < end:
            return name
    return "Di luar sesi"


def count_by_session(timestamps: pd.Series, sessions: dict) -> dict:
    hours = pd.to_datetime(timestamps, errors="coerce").dropna().dt.hour
    labels = hours.map(lambda h: assign_session(h, sessions))
    return labels.value_counts().to_dict()

