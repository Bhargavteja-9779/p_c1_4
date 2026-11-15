"""Generate all tables (CSV + Markdown) and manuscript_numbers.json from machine-readable results.
No number is typed by hand: the manuscript renderer reads tables/manuscript_numbers.json.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.evaluation.conformal_eval import PARAMS, PROPOSED  # noqa: E402
from src.utils import RESULTS_DIR, TABLES_DIR, cache_root  # noqa: E402

STAGERS = {"yasa": "YASA (pretrained, external)", "lgbm_sc_s0": "LightGBM-SC (in-domain)"}
METHOD_LABEL = {"ba_loa": "Bland–Altman LoA", "scp_abs": "Split conformal (constant)",
                "scp_abs_mu": "Split conformal (constant, FFBS centre)", "bayes_pct": "FFBS percentiles (uncalibrated)",
                "ind_pct": "Independent-epoch percentiles (uncalibrated)", "cqr_ffbs": "CQR on FFBS quantiles",
                "cqr_qr": "CQR, quantile regression", "norm_entropy_reg": "Normalised by mean entropy",
                "norm_ffbs": "Normalised by FFBS SD (unregularised)", "norm_reg_ffbs": "Proposed (FFBS-normalised)",
                "norm_reg_ind": "Ablation: independent-epoch SD", "norm_reg_ffbs1": "Ablation: tau = 1"}
COHORTS = ["SC", "ST", "HMC"]
NUM = {}


def md(df, path, floatfmt=".3f"):
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(path.with_suffix(".csv"), index=False)
    try:
        path.with_suffix(".md").write_text(df.to_markdown(index=False, floatfmt=floatfmt))
    except ImportError:
        path.with_suffix(".md").write_text(df.to_string(index=False))


def fmt_ms(x, d=1):
    return f"{np.mean(x):.{d}f} ± {np.std(x, ddof=1):.{d}f}"


# ----------------------------------------------------------------------------- Table 1
def table1():
    meta = pd.read_csv(cache_root() / "sleep" / "nights.csv")
    rows = []
    for c in COHORTS:
        m = meta[meta.cohort == c]
        r = {"Cohort": c, "Nights": len(m), "Subjects": m.subject.nunique(),
             "Age, y (mean ± SD)": fmt_ms(m.age.dropna()) if m.age.notna().any() else "not released",
             "Female nights, n": int((m.sex == "F").sum()) if m.sex.notna().any() else "not released",
             "Scored epochs": int(m.n_scored.sum())}
        tot = m[[f"n_{s}" for s in ["W", "N1", "N2", "N3", "REM"]]].sum()
        for s in ["W", "N1", "N2", "N3", "REM"]:
            r[f"{s}, %"] = round(100 * tot[f"n_{s}"] / tot.sum(), 1)
        for st, lab in STAGERS.items():
            accs, kaps, ys, ps = [], [], [], []
            for p in sorted((RESULTS_DIR / "predictions" / st / c).glob("*.npz")):
                z = np.load(p)
                y, yp = z["y"], z["P"].argmax(1)
                k = y >= 0
                accs.append(np.mean(y[k] == yp[k]))
                kaps.append(cohen_kappa_score(y[k], yp[k]))
                ys.append(y[k]); ps.append(yp[k])
            r[f"{lab}: accuracy (per night)"] = fmt_ms(accs, 3)
            r[f"{lab}: kappa (per night)"] = fmt_ms(kaps, 3)
            r[f"{lab}: pooled kappa"] = round(cohen_kappa_score(np.concatenate(ys), np.concatenate(ps)), 3)
            NUM[f"acc_{st}_{c}"] = float(np.mean(accs))
            NUM[f"kappa_{st}_{c}"] = float(np.mean(kaps))
        rows.append(r)
        NUM[f"nights_{c}"] = len(m)
        NUM[f"subjects_{c}"] = int(m.subject.nunique())
    NUM["nights_total"] = int(len(meta))
    NUM["subjects_total"] = int(meta.subject.nunique())
    NUM["epochs_total"] = int(meta.n_scored.sum())
    t = pd.DataFrame(rows).set_index("Cohort").T.reset_index().rename(columns={"index": "Characteristic"})
    md(t, TABLES_DIR / "table1_cohorts")


if __name__ == "__main__":
    table1()
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    p = TABLES_DIR / "manuscript_numbers.json"
    old = json.loads(p.read_text()) if p.exists() else {}
    old.update(NUM)
    p.write_text(json.dumps(old, indent=2))
    print(open(TABLES_DIR / "table1_cohorts.md").read())
