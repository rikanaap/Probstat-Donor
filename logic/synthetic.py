"""Generator data SIMULASI untuk demo. Bukan data nyata."""
import numpy as np
import pandas as pd
from calc.config import ITEMS, SATISFACTION, OUTCOME

TRUE_WEIGHTS = {"alur": .10, "daftar": .10, "tunggu": .30, "ramah": .25,
                "tusuk": .15, "ruang": .05, "makanan": .05}
SESSION_MEAN = {"Pagi": 3.9, "Siang": 3.3, "Sore": 3.6}


def generate(n_per_session: dict, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    frames = []
    for s, n in n_per_session.items():
        base = SESSION_MEAN.get(s, 3.6)
        lat = rng.normal(0, 0.6, n)
        d = {"sesi": [s] * n}
        for k in ITEMS:
            m = base - (0.4 if (k == "tunggu" and s == "Siang") else 0)
            d[k] = np.clip(np.round(m + lat + rng.normal(0, 0.7, n)), 1, 5)
        x = sum(TRUE_WEIGHTS[k] * np.array(d[k]) for k in ITEMS)
        d[SATISFACTION] = np.clip(np.round(0.3 + 0.9 * x + rng.normal(0, 0.5, n)), 1, 5)
        d[OUTCOME] = np.clip(np.round(0.2 + 0.9 * x + rng.normal(0, 0.6, n)), 1, 5)
        frames.append(pd.DataFrame(d))
    return pd.concat(frames, ignore_index=True)


def generate_arrivals(days: int = 14, per_day: int = 120, seed: int = 1) -> pd.Series:
    rng = np.random.default_rng(seed)
    n = days * per_day
    hours = rng.choice(np.arange(6, 20), size=n,
                       p=np.array([2, 5, 8, 7, 5, 4, 5, 6, 5, 4, 3, 2, 1, 1]) / 58)
    day = rng.integers(0, days, size=n)
    ts = pd.Timestamp("2025-01-06") + pd.to_timedelta(day, "D") + pd.to_timedelta(hours, "h") \
        + pd.to_timedelta(rng.integers(0, 60, size=n), "m")
    return pd.Series(ts)


def sample_xlsx(n_per_session: int = 90) -> bytes:
    """Contoh data survei sintetis (Excel) untuk diunduh dan dicoba."""
    from io import BytesIO
    buf = BytesIO()
    generate({"Pagi": n_per_session, "Siang": n_per_session, "Sore": n_per_session}).to_excel(buf, index=False)
    return buf.getvalue()
