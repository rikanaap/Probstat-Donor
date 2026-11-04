"""Perhitungan inti: pengaruh tiap item terhadap niat kembali."""
import pandas as pd
import statsmodels.api as sm


def fit(df: pd.DataFrame, items: list, outcome: str):
    return sm.OLS(df[outcome], sm.add_constant(df[items])).fit()


def standardized_beta(df: pd.DataFrame, items: list, outcome: str) -> pd.Series:
    cols = items + [outcome]
    z = (df[cols] - df[cols].mean()) / df[cols].std(ddof=1)
    return sm.OLS(z[outcome], z[items]).fit().params


def priority_map(df: pd.DataFrame, items: list, outcome: str) -> pd.DataFrame:
    return pd.DataFrame({"Pengaruh (beta)": standardized_beta(df, items, outcome),
                         "Kinerja (rerata)": df[items].mean()})
