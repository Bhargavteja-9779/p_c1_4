"""Build references.json (CSL-JSON) by fetching metadata for every DOI from the DOI registry
(Crossref/DataCite content negotiation). Entries without a DOI are entered manually below and are
flagged 'manual' in the audit file. Output: references.json, reference_audit.csv
"""
import csv
import json
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOIS = {
    "rosenberg2013": "10.5664/jcsm.2350",
    "dankerhopfe2009": "10.1111/j.1365-2869.2008.00700.x",
    "stephansen2018": "10.1038/s41467-018-07229-3",
    "perslev2021": "10.1038/s41746-021-00440-5",
    "vallat2021": "10.7554/eLife.70092",
    "baumert2023": "10.1016/j.sleep.2023.04.002",
    "svensson2024": "10.1016/j.sleep.2024.01.020",
    "beau2025": "10.1016/j.sleep.2025.106698",
    "rohrscheib2026": "10.1016/j.sleep.2026.108828",
    "hardarson2023": "10.1007/s40675-023-00253-w",
    "fiorillo2021": "10.1109/TNSRE.2021.3117970",
    "phan2022": "10.1109/TBME.2022.3147187",
    "heremans2024": "10.1016/j.compbiomed.2024.108205",
    "bechny2024": "10.2147/NSS.S455649",
    "kang2021": "10.1038/s41746-021-00515-3",
    "vangorp2022": "10.1093/sleep/zsac134",
    "bakker2023": "10.1093/sleep/zsac154",
    "li2025conmil": "10.1007/s41666-025-00207-7",
    "ganglberger2024": "10.1093/sleep/zsae202",
    "mikkelsen2020": "10.1109/EMBC44109.2020.9175743",
    "kemp2000": "10.1109/10.867928",
    "sleepedf_data": "10.13026/C2X676",
    "goldberger2000": "10.1161/01.CIR.101.23.e215",
    "pollard2026": "10.1038/s44360-026-00096-z",
    "alvarez2021": "10.1371/journal.pone.0256111",
    "hmc_data": "10.13026/t79q-fr32",
    "bourlard1994": "10.1007/978-1-4615-3210-1",
    "carter1994": "10.1093/biomet/81.3.541",
    "fruhwirth1994": "10.1111/j.1467-9892.1994.tb00184.x",
    "vovk2005": "10.1007/b106715",
    "lei2018": "10.1080/01621459.2017.1307116",
    "angelopoulos2023": "10.1561/2200000101",
    "barber2023": "10.1214/23-AOS2276",
    "bland1986": "10.1016/S0140-6736(86)90837-8",
    "gneiting2007": "10.1198/016214506000001437",
    "mcgraw1996": "10.1037/1082-989X.1.1.30",
    "berry2017": "10.5664/jcsm.6576",
    "rabiner1989": "10.1109/5.18626",
    "kaneda2026": "10.1093/sleepadvances/zpag054",
    "deirossi2025": "10.1038/s41746-025-02237-2",
    "vainikka2026": "10.1109/TBME.2025.3623380",
    "vangorp2023jbhi": "10.1109/JBHI.2023.3304010",
    "vangorp2023icassp": "10.1109/ICASSP49357.2023.10096894",
    "barber2021": "10.1214/20-AOS1965",
    "bland1999": "10.1177/096228029900800204",
    "chib1996": "10.1016/0304-4076(95)01770-4",
    "moser2009": "10.1093/sleep/32.2.139",
}
MANUAL = [
    {"id": "philips2024patent", "type": "patent",
     "title": "System for estimating uncertainty of overnight sleep parameters through a stochastic neural network",
     "author": [{"family": "van Gorp", "given": "H"}, {"family": "Fonseca", "given": "P"}, {"family": "van Gilst", "given": "M M"},
                {"family": "Overeem", "given": "S"}, {"family": "van Sloun", "given": "R J G"}],
     "publisher": "Koninklijke Philips N.V.", "number": "EP4388985A1", "issued": {"date-parts": [[2024, 6, 26]]},
     "note": "European patent application, published 26 June 2024 (withdrawn)"},
    {"id": "alexandari2020", "type": "paper-conference",
     "title": "Maximum likelihood with bias-corrected calibration is hard-to-beat at label shift adaptation",
     "author": [{"family": "Alexandari", "given": "A"}, {"family": "Kundaje", "given": "A"}, {"family": "Shrikumar", "given": "A"}],
     "container-title": "Proceedings of the 37th International Conference on Machine Learning (PMLR 119)",
     "page": "222-232", "issued": {"date-parts": [[2020]]}},
    {"id": "romano2019", "type": "paper-conference", "title": "Conformalized quantile regression",
     "author": [{"family": "Romano", "given": "Y"}, {"family": "Patterson", "given": "E"}, {"family": "Candès", "given": "E"}],
     "container-title": "Advances in Neural Information Processing Systems 32 (NeurIPS 2019)", "page": "3543-3553",
     "issued": {"date-parts": [[2019]]}},
    {"id": "tibshirani2019", "type": "paper-conference", "title": "Conformal prediction under covariate shift",
     "author": [{"family": "Tibshirani", "given": "RJ"}, {"family": "Foygel Barber", "given": "R"}, {"family": "Candès", "given": "E"},
                {"family": "Ramdas", "given": "A"}],
     "container-title": "Advances in Neural Information Processing Systems 32 (NeurIPS 2019)", "page": "2530-2540",
     "issued": {"date-parts": [[2019]]}},
]


OVERRIDES = {  # registry records missing fields (verified against the publisher landing page)
    "vovk2005": {"author": [{"family": "Vovk", "given": "V"}, {"family": "Gammerman", "given": "A"},
                            {"family": "Shafer", "given": "G"}], "publisher": "Springer", "type": "book"},
    "bourlard1994": {"type": "book", "publisher": "Springer (Kluwer Academic Publishers)"},
    "li2025conmil": {"note": "ConMIL: conformalised multiple-instance learning; arXiv:2501.16215"},
    "bland1986": {"author": [{"family": "Bland", "given": "J M"}, {"family": "Altman", "given": "D G"}]},
}
AUTHOR_FIXES = {  # (doi-key, index) -> corrected name, where the registry splits names wrongly
    ("deirossi2025", 0): {"family": "Dei Rossi", "given": "Alvise"},
    ("deirossi2025", 4): {"family": "van der Meer", "given": "Julia"},
    ("vangorp2023icassp", 0): {"family": "van Gorp", "given": "Hans"},
}


def normalise(key, rec):
    """Clean registry quirks: HTML entities, ALL-CAPS names/titles, 'Volume 16' volumes."""
    import html
    import re
    for f in ("title", "container-title"):
        if isinstance(rec.get(f), str):
            t = html.unescape(rec[f]).replace("&Amp;", "&")
            if t.isupper():
                t = t[0] + t[1:].lower()
            rec[f] = t
    for i, a in enumerate(rec.get("author", []) or []):
        for part in ("family", "given"):
            v = a.get(part)
            if isinstance(v, str) and v.isupper() and len(v) > 2:
                a[part] = v.title()
        if (key, i) in AUTHOR_FIXES:
            rec["author"][i] = dict(AUTHOR_FIXES[(key, i)])
    if isinstance(rec.get("volume"), str):
        rec["volume"] = re.sub(r"^Volume\s*", "", rec["volume"])
    return rec


def fetch(doi):
    req = urllib.request.Request(f"https://doi.org/{doi}", headers={"Accept": "application/vnd.citationstyles.csl+json"})
    for k in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except Exception as e:  # noqa: BLE001
            err = e
            time.sleep(2 * (k + 1))
    raise RuntimeError(f"{doi}: {err}")


def main():
    items, audit = [], []
    for key, doi in DOIS.items():
        d = fetch(doi)
        keep = {k: d[k] for k in ("type", "title", "author", "editor", "container-title", "volume", "issue", "page",
                                  "issued", "DOI", "publisher", "URL", "number", "article-number") if k in d}
        if "page" not in keep and "article-number" in keep:
            keep["page"] = keep["article-number"]
        if isinstance(keep.get("container-title"), list):
            keep["container-title"] = keep["container-title"][0] if keep["container-title"] else ""
        if keep.get("type") == "dataset":
            keep["type"] = "dataset"
        keep["id"] = key
        keep["DOI"] = doi
        keep.update(OVERRIDES.get(key, {}))
        keep = normalise(key, keep)
        items.append(keep)
        first = (keep.get("author") or [{}])[0]
        audit.append(dict(key=key, doi=doi, source="doi-registry", title=d.get("title"),
                          first_author=first.get("family", first.get("literal", "")),
                          year=(d.get("issued", {}).get("date-parts") or [[None]])[0][0],
                          container=keep.get("container-title", ""), volume=d.get("volume", ""), pages=d.get("page", "")))
        time.sleep(0.3)
    for m in MANUAL:
        items.append(m)
        audit.append(dict(key=m["id"], doi="", source="manual (no DOI; verified against proceedings listing)",
                          title=m["title"], first_author=m["author"][0]["family"], year=m["issued"]["date-parts"][0][0],
                          container=m.get("container-title", m.get("number", "")), volume="", pages=m.get("page", "")))
    (HERE / "references.json").write_text(json.dumps(items, indent=1, ensure_ascii=False))
    with open(HERE / "reference_audit.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(audit[0]))
        w.writeheader()
        w.writerows(audit)
    for a in audit:
        print(f"{a['key']:16s} {a['year']} {a['first_author']:14s} {str(a['title'])[:70]} | {str(a['container'])[:40]}")


if __name__ == "__main__":
    main()
