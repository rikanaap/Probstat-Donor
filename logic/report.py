"""Merangkum semua hasil analisis sekali jalan (dipanggil saat tombol Analisis ditekan)."""
import pandas as pd
from . import insights


def build(df: pd.DataFrame) -> dict:
    return {"top": insights.priorities(df), "quality": insights.data_quality(df),
            "scores": insights.item_scores(df), "sessions": insights.session_summary(df)}
