"""DEVELOPMENT PILOT (DS1 only, patient-grouped CV). Not a reported result."""
import sys, time
import numpy as np
sys.path.insert(0, "/home/user/p_c1_4/Target_Journal_Submission/code")
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import GroupKFold
from sklearn.metrics import f1_score
from src.utils import data_root, cache_root
from src.data import ecg
from src.adaptation.calibration import BCTS
from src.adaptation import label_shift as ls, empirical_bayes as eb

K = 4
recs = [r for r in ecg.load_db("mitdb", data_root(), cache_root()) if r.record in ecg.DS1]
X = [ecg.handcrafted_features(r) for r in recs]
Y = [r.y for r in recs]


def fit_model(idx, seed=0):
    Xt = np.concatenate([X[i] for i in idx]); yt = np.concatenate([Y[i] for i in idx])
    cw = len(yt) / (K * np.maximum(np.bincount(yt, minlength=K), 1))
    m = HistGradientBoostingClassifier(max_iter=200, learning_rate=0.1, random_state=seed)
    m.fit(Xt, yt, sample_weight=cw[yt])
    return m


def logp(m, Xa):
    return np.log(np.clip(m.predict_proba(Xa), 1e-12, 1))


outer = np.array_split(np.arange(len(recs)), 11)
res = {k: [] for k in ["raw", "none", "mlls", "bbse", "rlls", "mapls", "im_prior", "hmm_fixed", "ml_hmm", "eb_iid", "eb_hmm"]}
true_all, prior_err = [], {k: [] for k in res}
t0 = time.time()
for fo, test_idx in enumerate(outer):
    train_idx = [i for i in range(len(recs)) if i not in test_idx]
    # inner OOF for calibration / confusion
    gkf = GroupKFold(n_splits=4)
    oof_lp, oof_y = [], []
    for tr, va in gkf.split(train_idx, groups=train_idx):
        m = fit_model([train_idx[i] for i in tr])
        for i in va:
            oof_lp.append(logp(m, X[train_idx[i]])); oof_y.append(Y[train_idx[i]])
    oof_lp = np.concatenate(oof_lp); oof_y = np.concatenate(oof_y)
    cal = BCTS().fit(oof_lp, oof_y)
    P_src = cal.transform(oof_lp)
    pi_s = np.bincount(oof_y, minlength=K) / len(oof_y)
    C = ls.soft_confusion(P_src, oof_y, K)
    seqs = [Y[i] for i in train_idx]
    alpha_eb = eb.fit_class_prior(seqs, K)
    beta_eb = eb.fit_transition_prior(seqs, K)
    A_pop = eb.pooled_transition_matrix(seqs, K)
    model = fit_model(train_idx)
    for i in test_idx:
        lp = logp(model, X[i]); P = cal.transform(lp)
        y = Y[i]; true_all.append(y)
        res["raw"].append(np.argmax(lp, 1))
        tp = np.bincount(y, minlength=K) / len(y)
        kw = dict(C=C, n_src=len(oof_y), alpha_eb=alpha_eb, beta_eb=beta_eb, A_pop=A_pop)
        for name in list(res)[1:]:
            a = ls.METHODS[name](P, pi_s, **kw)
            res[name].append(np.argmax(a.post, 1))
            prior_err[name].append(np.abs(a.prior - tp))
    print(f"fold {fo} done {time.time()-t0:.0f}s alpha_eb={np.round(alpha_eb,3)}", flush=True)

yt = np.concatenate(true_all)
print("\nmethod      acc    F1_N   F1_S   F1_V   F1_F  macroF1 | MAE prior S,V,F (pp)")
for name, preds in res.items():
    yp = np.concatenate(preds)
    f = f1_score(yt, yp, labels=range(K), average=None, zero_division=0)
    pe = np.mean(prior_err[name], axis=0) * 100 if prior_err[name] else [np.nan] * 4
    print(f"{name:10s} {np.mean(yt==yp):.4f} " + " ".join(f"{v:.3f}" for v in f) + f"  {f.mean():.3f} | {pe[1]:.2f} {pe[2]:.2f} {pe[3]:.2f}")
