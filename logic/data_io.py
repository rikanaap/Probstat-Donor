"""Validasi dan pembersihan data survei."""
import pandas as pd
from calc.config import REQUIRED_COLS, ITEMS, SATISFACTION, OUTCOME


def validate(df: pd.DataFrame) -> list:
    errors = [f"Kolom '{c}' tidak ditemukan." for c in REQUIRED_COLS if c not in df.columns]
    if errors:
        return errors
    for c in [*ITEMS, SATISFACTION, OUTCOME]:
        if not pd.to_numeric(df[c], errors="coerce").between(1, 5).all():
            errors.append(f"Kolom '{c}' harus berisi angka 1-5 tanpa sel kosong.")
    return errors


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for c in [*ITEMS, SATISFACTION, OUTCOME]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.dropna(subset=REQUIRED_COLS)


def template() -> pd.DataFrame:
    return pd.DataFrame([{"sesi": "Pagi", **{k: 4 for k in ITEMS}, SATISFACTION: 4, OUTCOME: 4}])


def read_table(file) -> pd.DataFrame:
    """Baca file unggahan Excel (.xlsx) atau CSV."""
    return pd.read_excel(file) if file.name.lower().endswith((".xlsx", ".xls")) else pd.read_csv(file)
