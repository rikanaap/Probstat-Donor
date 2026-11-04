"""Rencana pembagian form dalam bahasa awam."""
from calc import config, sampling

PRECISION = {"Cepat (cukup untuk gambaran)": 0.15, "Standar (disarankan)": 0.10, "Teliti (butuh lebih banyak form)": 0.05}


def counts_from_times(timestamps, sessions: dict) -> dict:
    return sampling.count_by_session(timestamps, sessions)


def make_plan(counts: dict, precision: str) -> list:
    e = PRECISION[precision]
    rows = []
    for name, total in counts.items():
        n = sampling.cochran(int(total), e)
        rows.append({"Sesi": name, "Perkiraan donor": int(total), "Form yang dibagikan": n,
                     "Beri form ke setiap donor ke-": sampling.sampling_interval(int(total), n)})
    return rows


def warnings(rows: list) -> list:
    need = sampling.min_for_regression(len(config.ITEMS))
    return [f"Sesi {r['Sesi']}: form kurang dari {need}. Hasil hanya cocok sebagai gambaran kasar."
            for r in rows if r["Form yang dibagikan"] < need]
