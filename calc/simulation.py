"""Simulasi skenario: layanan naik -> niat kembali -> kantong darah."""
import numpy as np
import pandas as pd
from scipy import stats
from . import regression


def scenario(df: pd.DataFrame, items: list, outcome: str, changes: dict, N: int,
             conversion: float, reject_rate: float, threshold: int = 4) -> dict:
    model = regression.fit(df, items, outcome)
    coef = model.params[items]
    sigma = max(float(np.sqrt(model.mse_resid)), 1e-6)
    new_items = (df[items] + pd.Series(changes)).clip(1, 5)
    shift = ((new_items - df[items]) * coef).sum(axis=1)
    # Jawaban berupa bilangan bulat, jadi "skor 4" mencakup prediksi mulai 3,5.
    cut = threshold - 0.5
    base = model.fittedvalues
    prob0 = 1 - stats.norm.cdf((cut - base) / sigma)
    prob1 = 1 - stats.norm.cdf((cut - (base + shift)) / sigma)
    p0 = float((df[outcome] >= threshold).mean())
    p1 = float(np.clip(p0 + (prob1 - prob0).mean(), 0, 1))
    return {"p0": p0, "p1": p1, "N": N,
            "ci0": stats.binom.interval(.95, N, p0), "ci1": stats.binom.interval(.95, N, p1),
            "extra_bags": N * (p1 - p0) * conversion * (1 - reject_rate)}
