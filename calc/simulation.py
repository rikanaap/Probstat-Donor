"""Simulasi skenario probabilitas: kenaikan layanan -> peluang niat kembali -> ekspektasi donor."""
import numpy as np
import pandas as pd
from scipy import stats
from . import regression


def scenario(df: pd.DataFrame, items: list, outcome: str, changes: dict, N: int, threshold: int = 4) -> dict:
    model = regression.fit(df, items, outcome)
    coef = model.params[items]
    sigma = max(float(np.sqrt(model.mse_resid)), 1e-6)
    new_items = (df[items] + pd.Series(changes)).clip(1, 5)
    shift = ((new_items - df[items]) * coef).sum(axis=1)
    # Jawaban berupa bilangan bulat (skala Likert), batas sukses kategori threshold (misal >= 4) mulai 3.5.
    cut = threshold - 0.5
    base = model.fittedvalues
    prob0 = 1 - stats.norm.cdf((cut - base) / sigma)
    prob1 = 1 - stats.norm.cdf((cut - (base + shift)) / sigma)
    p0 = float((df[outcome] >= threshold).mean())
    p1 = float(np.clip(p0 + (prob1 - prob0).mean(), 0, 1))

    # Nilai harapan (Expected Value) jumlah donor berdistribusi Binomial(N, p)
    exp0 = N * p0
    exp1 = N * p1
    extra_donors = N * (p1 - p0)

    # Interval kepercayaan 95% untuk Binomial(N, p)
    ci0 = stats.binom.interval(0.95, N, p0)
    ci1 = stats.binom.interval(0.95, N, p1)

    # Interval kepercayaan 95% selisih proporsi (Wald CI)
    n_sample = max(len(df), 1)
    se_diff = float(np.sqrt((p0 * (1 - p0) + p1 * (1 - p1)) / n_sample))
    ci_diff = (max(0.0, N * (p1 - p0 - 1.96 * se_diff)), N * (p1 - p0 + 1.96 * se_diff))

    return {
        "p0": p0, "p1": p1, "N": N,
        "exp0": exp0, "exp1": exp1,
        "extra_donors": extra_donors,
        "ci0": ci0, "ci1": ci1,
        "ci_diff": ci_diff,
    }
