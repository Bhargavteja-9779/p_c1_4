"""Build the Sleep Medicine submission manuscript (DOCX + PDF) from Markdown section sources.

1. Placeholders {{expr}} or {{expr:fmt}} in sections/*.md are evaluated against
   ../tables/manuscript_numbers.json (keys sanitised: '%' -> 'pct', other non-identifier chars -> '_').
   A missing key aborts the build: no number in the manuscript can be typed by hand.
2. pandoc converts the rendered Markdown (LaTeX math -> native Word equations) using a reference
   DOCX with journal-style formatting (Times New Roman 12 pt, double spacing).
3. python-docx post-processing: continuous line numbers, page numbers, 2.5 cm margins.
4. LibreOffice converts the DOCX to PDF.
Usage: python build_manuscript.py [--no-pdf]
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SECTIONS = ["00_front", "01_introduction", "02_methods", "03_results", "04_discussion", "05_conclusion",
            "06_declarations", "07_references", "08_tables_figures"]


def sanitise(k):
    return re.sub(r"[^0-9a-zA-Z_]", "_", k.replace("%", "pct"))


def load_numbers():
    nums = json.loads((ROOT / "tables" / "manuscript_numbers.json").read_text())
    return {sanitise(k): v for k, v in nums.items()}


def render(text, ns):
    def rep(m):
        body = m.group(1)
        expr, _, fmt = body.partition(":") if not body.startswith("'") else (body, "", "")
        try:
            val = eval(expr, {"__builtins__": {}, "abs": abs, "min": min, "max": max, "round": round}, ns)
        except NameError as e:
            sys.exit(f"MISSING NUMBER for placeholder {{{{{body}}}}}: {e}")
        if val is None:
            sys.exit(f"Placeholder {{{{{body}}}}} evaluated to None (undefined statistic)")
        return format(val, fmt) if fmt else str(val)
    return re.sub(r"\{\{(.+?)\}\}", rep, text)


def make_reference_docx(path):
    """Reference DOCX for pandoc: Times New Roman 12 pt, double-spaced body, journal headings."""
    from docx import Document
    from docx.shared import Pt
    from docx.enum.text import WD_LINE_SPACING
    base = path.parent / "pandoc_default_ref.docx"
    subprocess.run(["pandoc", "-o", str(base), "--print-default-data-file", "reference.docx"], check=True,
                   stdout=open(base, "wb"))
    doc = Document(str(base))
    for name in ["Normal", "Body Text", "First Paragraph", "Compact", "Abstract", "Bibliography",
                 "Title", "Subtitle", "Author", "Date", "Heading 1", "Heading 2", "Heading 3",
                 "Block Text", "Table Caption", "Image Caption", "Caption"]:
        try:
            st = doc.styles[name]
        except KeyError:
            continue
        st.font.name = "Times New Roman"
        st.font.color.rgb = None
        rpr = st.element.get_or_add_rPr()
        rfonts = rpr.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rFonts")
        if rfonts is not None:
            for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
                rfonts.set("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}" + a.split(":")[1], "Times New Roman")
        pf = st.paragraph_format
        if name in ("Normal", "Body Text", "First Paragraph", "Abstract", "Bibliography", "Block Text"):
            st.font.size = Pt(12)
            pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
            pf.space_after = Pt(0)
        if name == "Compact":
            st.font.size = Pt(9)
            pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
        if name.startswith("Heading"):
            st.font.size = Pt({"Heading 1": 13, "Heading 2": 12, "Heading 3": 12}[name])
            st.font.bold = True
            st.font.italic = name == "Heading 3"
            pf.space_before = Pt(12)
            pf.space_after = Pt(6)
        if name == "Title":
            st.font.size = Pt(16)
            st.font.bold = True
        if name in ("Table Caption", "Image Caption", "Caption"):
            st.font.size = Pt(10)
            st.font.italic = False
    doc.save(str(path))


def postprocess(docx_path):
    from docx import Document
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm
    doc = Document(str(docx_path))
    for sec in doc.sections:
        sec.top_margin = sec.bottom_margin = sec.left_margin = sec.right_margin = Cm(2.5)
        sectPr = sec._sectPr
        ln = OxmlElement("w:lnNumType")
        ln.set(qn("w:countBy"), "1")
        ln.set(qn("w:restart"), "continuous")
        ln.set(qn("w:distance"), "283")
        sectPr.append(ln)
        # page number in footer
        p = sec.footer.paragraphs[0] if sec.footer.paragraphs else sec.footer.add_paragraph()
        p.alignment = 1
        run = p.add_run()
        for t, txt in (("begin", None), (None, "PAGE"), ("end", None)):
            if t:
                fc = OxmlElement("w:fldChar")
                fc.set(qn("w:fldCharType"), t)
                run._r.append(fc)
            else:
                it = OxmlElement("w:instrText")
                it.set(qn("xml:space"), "preserve")
                it.text = txt
                run._r.append(it)
    # tables: small font, single spacing, autofit borders
    for tbl in doc.tables:
        tbl.style = doc.styles["Table"] if "Table" in [s.name for s in doc.styles] else tbl.style
        for row in tbl.rows:
            for cell in row.cells:
                for par in cell.paragraphs:
                    par.paragraph_format.line_spacing = 1.0
                    for r in par.runs:
                        r.font.size = docx_pt(8)
    doc.save(str(docx_path))


def docx_pt(x):
    from docx.shared import Pt
    return Pt(x)


def word_count(md_text):
    body = md_text
    for cut in ("## Declaration", "## References", "## Tables"):
        if cut in body:
            body = body.split(cut)[0]
    m = re.search(r"## 1\. Introduction", body)
    body = body[m.start():] if m else body
    body = re.sub(r"\$\$.*?\$\$", " ", body, flags=re.S)
    body = re.sub(r"\$.*?\$", " x ", body)
    body = re.sub(r"[#*_>|\[\]()]", " ", body)
    return len(re.findall(r"\b\w[\w'’.-]*\b", body))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-pdf", action="store_true")
    a = ap.parse_args()
    ns = load_numbers()
    parts = []
    for s in SECTIONS:
        f = HERE / "sections" / f"{s}.md"
        if f.exists():
            parts.append(render(f.read_text(), ns))
    md = "\n\n".join(parts)

    def inject(m):  # generated tables are injected verbatim from ../tables/<name>.md
        f = ROOT / "tables" / f"{m.group(1)}.md"
        if not f.exists():
            sys.exit(f"MISSING TABLE {f}")
        return f.read_text()
    md = re.sub(r"<<TABLE:([\w-]+)>>", inject, md)
    build = HERE / "build"
    build.mkdir(exist_ok=True)
    (build / "manuscript_rendered.md").write_text(md)
    abstract = re.search(r"\*\*Abstract\*\*(.*?)\*\*Keywords", md, re.S)
    if abstract:  # do not count the section labels themselves
        abstract_txt = re.sub(r"\*(Objective|Methods|Results|Conclusions):\*", " ", abstract.group(1))
    else:
        abstract_txt = ""
    stats = {"main_text_words": word_count(md),
             "abstract_words": len(re.findall(r"\b[\w'’.%-]+\b", abstract_txt))}
    (build / "word_counts.json").write_text(json.dumps(stats, indent=2))
    md = md.replace("<<WORDCOUNT>>", f"{stats['main_text_words']:,}").replace("<<ABSTRACTCOUNT>>", str(stats["abstract_words"]))
    (build / "manuscript_rendered.md").write_text(md)
    print("word counts:", stats)
    ref = build / "reference.docx"
    make_reference_docx(ref)
    out = HERE / "Final_Manuscript.docx"
    subprocess.run(["pandoc", str(build / "manuscript_rendered.md"), "-o", str(out), "--reference-doc", str(ref),
                    "--resource-path", f"{ROOT}:{HERE}", "-f", "markdown+tex_math_dollars+pipe_tables+implicit_figures",
                    "--citeproc", "--bibliography", str(HERE / "references.json"), "--csl", str(HERE / "elsevier-vancouver.csl")],
                   check=True)
    postprocess(out)
    print("DOCX:", out)
    if not a.no_pdf:
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(HERE), str(out)],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("PDF:", HERE / "Final_Manuscript.pdf")


if __name__ == "__main__":
    main()
