"""Perkiraan dampak perbaikan berbasis teori probabilitas."""
from calc import config, simulation


def what_if(df, improve: list, step: float, total_donors: int) -> dict:
    changes = {k: (step if k in improve else 0.0) for k in config.ITEMS}
    r = simulation.scenario(df, list(config.ITEMS), config.OUTCOME, changes, total_donors)
    return {
        "p0": r["p0"],
        "p1": r["p1"],
        "exp0": r["exp0"],
        "exp1": r["exp1"],
        "donor_tambahan": r["extra_donors"],
        "ci0": r["ci0"],
        "ci1": r["ci1"],
        "ci_diff": r["ci_diff"],
        "total": total_donors,
    }
