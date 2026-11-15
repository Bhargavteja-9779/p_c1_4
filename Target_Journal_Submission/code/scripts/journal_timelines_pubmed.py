"""Compute submission-to-acceptance timelines from PubMed 'received'/'accepted' history dates.

Usage: python scripts/journal_timelines_pubmed.py --out ../journal_selection/pubmed_timelines.json
Only articles that deposit both dates are counted; reviews/editorials/letters are excluded.
This measures *accepted* papers only (survivorship): it is the acceptance time conditional on
acceptance, not a guarantee for any individual manuscript.
"""
import argparse
import json
import statistics
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
JOURNALS = {
    "Sleep (OUP)": "Sleep[ta]",
    "Sleep Medicine (Elsevier)": "Sleep Med[ta]",
    "Journal of Sleep Research (Wiley)": "J Sleep Res[ta]",
    "Journal of Clinical Sleep Medicine (AASM)": "J Clin Sleep Med[ta]",
    "Sleep Health (Elsevier)": "Sleep Health[ta]",
    "Nature and Science of Sleep (Dove)": "Nat Sci Sleep[ta]",
    "Sleep and Breathing (Springer)": "Sleep Breath[ta]",
    "SLEEP Advances (OUP)": "Sleep Adv[ta]",
    "Computers in Biology and Medicine (Elsevier)": "Comput Biol Med[ta]",
    "IEEE J Biomed Health Inform (IEEE)": "IEEE J Biomed Health Inform[ta]",
    "Physiological Measurement (IOP)": "Physiol Meas[ta]",
}
FILTER = (' AND ("2025/07/01"[edat] : "2026/11/15"[edat]) AND journal article[pt]'
          ' NOT review[pt] NOT editorial[pt] NOT comment[pt] NOT letter[pt]')


def get(url):
    for k in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read()
        except Exception:
            time.sleep(2 * (k + 1))
    raise RuntimeError(url)


def pmids(term, retmax=400):
    q = urllib.parse.urlencode({"db": "pubmed", "term": term + FILTER, "retmax": retmax,
                                "sort": "pub_date", "retmode": "json"})
    js = json.loads(get(EUTILS + "esearch.fcgi?" + q))
    return js["esearchresult"]["idlist"], int(js["esearchresult"]["count"])


def history_days(ids):
    out = []
    for i in range(0, len(ids), 200):
        q = urllib.parse.urlencode({"db": "pubmed", "id": ",".join(ids[i:i + 200]), "retmode": "xml"})
        root = ET.fromstring(get(EUTILS + "efetch.fcgi?" + q))
        for art in root.iter("PubmedArticle"):
            d = {}
            for pd in art.iter("PubMedPubDate"):
                st = pd.get("PubStatus")
                if st in ("received", "accepted"):
                    try:
                        d[st] = date(int(pd.findtext("Year")), int(pd.findtext("Month")), int(pd.findtext("Day")))
                    except (TypeError, ValueError):
                        pass
            if "received" in d and "accepted" in d:
                dd = (d["accepted"] - d["received"]).days
                if 0 <= dd < 2000:
                    out.append(dd)
        time.sleep(0.4)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    res = {}
    for name, ta in JOURNALS.items():
        ids, total = pmids(ta)
        days = history_days(ids)
        if days:
            s = sorted(days)
            res[name] = {"query": ta + FILTER, "n_articles_matched": total, "n_sampled": len(ids),
                         "n_with_dates": len(days), "median_days": statistics.median(days),
                         "q1_days": s[len(s) // 4], "q3_days": s[(3 * len(s)) // 4],
                         "mean_days": round(statistics.mean(days), 1),
                         "frac_le_100": round(sum(x <= 100 for x in days) / len(days), 3),
                         "frac_le_60": round(sum(x <= 60 for x in days) / len(days), 3)}
        else:
            res[name] = {"query": ta + FILTER, "n_articles_matched": total, "n_with_dates": 0}
        print(name, res[name], flush=True)
        time.sleep(0.5)
    res["_meta"] = {"computed_on": str(date.today()), "source": EUTILS,
                    "window": "Entrez date 2025-07-01..2026-11-15, most recent <=400 per journal"}
    with open(args.out, "w") as f:
        json.dump(res, f, indent=2)


if __name__ == "__main__":
    main()
