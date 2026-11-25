"""Perkiraan dampak perbaikan, dalam angka yang mudah dipahami."""
from calc import config, simulation


def what_if(df, improve: list, step: float, total_donors: int) -> dict:
    changes = {k: (step if k in improve else 0.0) for k in config.ITEMS}
    r = simulation.scenario(df, list(config.ITEMS), config.OUTCOME, changes, total_donors)
    return {"sekarang": r["p0"], "sesudah": r["p1"],
            "donor_tambahan": total_donors * (r["p1"] - r["p0"]) * come_pct, "kantong": r["extra_bags"]}
