"""Base stager 1: YASA pretrained LightGBM (Vallat & Walker, eLife 2021), EEG+EOG model.

The classifier was trained by its authors on NSRR cohorts; none of our cohorts (Sleep-EDF, HMC)
was used for its training, so every night here is an external test night for this model.
Features (116 per epoch, including per-night robust-scaled and rolling-window context features)
are computed with YASA's own feature extractor and cached so that the in-domain model (base
stager 2) can be trained on exactly the same representation.
"""
from __future__ import annotations

import numpy as np

YASA_ORDER = ["W", "N1", "N2", "N3", "R"]   # our class order (0..4)


def night_to_raw(night, eeg="eeg", eog="eog"):
    import mne
    mne.set_log_level("ERROR")
    x = np.stack([getattr(night, eeg), getattr(night, eog)]).astype(np.float64) * 1e-6
    return mne.io.RawArray(x, mne.create_info(["EEG", "EOG"], 100, ["eeg", "eog"]))


def yasa_features_and_proba(night, eeg="eeg", eog="eog"):
    """Return (features DataFrame [n_epochs x 116], proba [n_epochs x 5] in W,N1,N2,N3,R order)."""
    import yasa
    raw = night_to_raw(night, eeg, eog)
    sls = yasa.SleepStaging(raw, eeg_name="EEG", eog_name="EOG")
    sls.fit()
    F = sls._features
    clf = sls._load_model("auto")
    P = clf.predict_proba(F[clf.feature_name_])
    cols = list(clf.classes_)
    P = P[:, [cols.index(c) for c in YASA_ORDER]]
    n = night.n_epochs
    if len(F) != n:  # YASA drops an incomplete final epoch; pad by repetition if needed
        k = n - len(F)
        F = F.reindex(range(n), method="ffill") if k > 0 else F.iloc[:n]
        P = np.vstack([P, np.repeat(P[-1:], k, 0)]) if k > 0 else P[:n]
    return F, P, list(clf.feature_name_)
