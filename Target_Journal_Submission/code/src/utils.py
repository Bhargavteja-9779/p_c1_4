"""Shared utilities: configuration, seeding, hardware detection, logging, paths."""
from __future__ import annotations

import json
import logging
import os
import platform
import random
import sys
import time
from pathlib import Path

import numpy as np
import yaml

CODE_DIR = Path(__file__).resolve().parents[1]          # .../code
ROOT_DIR = CODE_DIR.parent                               # .../Target_Journal_Submission
RESULTS_DIR = Path(os.environ.get("LSA_RESULTS_DIR", ROOT_DIR / "results"))
_QUICK = "LSA_RESULTS_DIR" in os.environ and RESULTS_DIR != ROOT_DIR / "results"
FIGURES_DIR = RESULTS_DIR / "figures" if _QUICK else ROOT_DIR / "figures"
TABLES_DIR = RESULTS_DIR / "tables" if _QUICK else ROOT_DIR / "tables"


def load_config(path: str | os.PathLike) -> dict:
    with open(path, "r") as f:
        cfg = yaml.safe_load(f)
    return cfg


def data_root(cfg: dict | None = None) -> Path:
    """Raw-data directory. Priority: $LSA_DATA_ROOT > cfg['data_root'] > code/data/raw."""
    env = os.environ.get("LSA_DATA_ROOT")
    if env:
        return Path(env)
    if cfg and cfg.get("data_root"):
        p = Path(cfg["data_root"])
        return p if p.is_absolute() else (CODE_DIR / p)
    return CODE_DIR / "data" / "raw"


def cache_root() -> Path:
    p = Path(os.environ.get("LSA_CACHE_ROOT", CODE_DIR / "data" / "cache"))
    p.mkdir(parents=True, exist_ok=True)
    return p


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    try:
        import torch
        torch.manual_seed(seed)
        torch.use_deterministic_algorithms(True, warn_only=True)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass


def get_device():
    """Detect the best available accelerator (CUDA, Apple MPS) and fall back to CPU."""
    import torch
    if torch.cuda.is_available():
        return torch.device("cuda")
    if getattr(torch.backends, "mps", None) is not None and torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def hardware_info() -> dict:
    info = {"platform": platform.platform(), "python": sys.version.split()[0],
            "cpu_count": os.cpu_count()}
    try:
        import torch
        info["torch"] = torch.__version__
        info["device"] = str(get_device())
        info["torch_threads"] = torch.get_num_threads()
    except ImportError:
        info["torch"] = None
    return info


def get_logger(name: str, logfile: Path | None = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)
    if logfile is not None:
        logfile.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(logfile)
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return logger


def save_json(obj, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2, default=_json_default)


def _json_default(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, Path):
        return str(o)
    raise TypeError(f"not serializable: {type(o)}")


class Timer:
    def __enter__(self):
        self.t0 = time.perf_counter()
        return self

    def __exit__(self, *a):
        self.elapsed = time.perf_counter() - self.t0
