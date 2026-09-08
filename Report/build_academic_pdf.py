#!/usr/bin/env python3
"""Render Report/ACADEMIC_REPORT.md to a print-quality A4 PDF."""

from __future__ import annotations

import re
from pathlib import Path

import markdown
from weasyprint import CSS, HTML

ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = ROOT / "Report"
MD_PATH = REPORT_DIR / "ACADEMIC_REPORT.md"
CSS_PATH = REPORT_DIR / "academic_report.css"
OUT_PDF = REPORT_DIR / "Report Project.pdf"
HTML_OUT = REPORT_DIR / "academic_report.html"

COVER_BANNER = ROOT / "Tableau" / "Netflix.jpg"


COVER = """
<section class="cover">
  <div class="kicker">Ho Chi Minh City University of Science &nbsp;·&nbsp; VNU-HCM</div>
  <p style="font-family:Inter,'Liberation Sans',sans-serif;font-size:9.5pt;color:#57534e;margin:3mm 0 0 0;">
    Faculty of Information Technology<br/>
    Course: <em>Data Visualization using Tableau</em><br/>
    Instructor: Nguyễn Ngọc Minh Châu
  </p>
  <h1>Netflix Movies and TV Shows</h1>
  <p class="subtitle">The catalog as designed supply — a visualization study through Stanford Design Thinking and Munzner’s nested model</p>
  <table class="cover-meta">
    <tr><th>Group</th><td>22HTTT · Group 11</td></tr>
    <tr><th>Authors</th><td>Nguyễn Thế Hiển (22127107, lead) · Bùi Công Mậu (22127260) · Nguyễn Trần Đại Quốc (22127355) · Thái Hữu Thọ (22127400)</td></tr>
    <tr><th>Corpus</th><td>Flixable / Kaggle Netflix titles extract &nbsp;·&nbsp; <em>N</em> = 8,807 titles</td></tr>
    <tr><th>Window</th><td>date_added 2008-01-01 → 2021-09-25 &nbsp;(2021 right-censored)</td></tr>
    <tr><th>Prototype</th><td>Tableau workbook <span style="font-family:Liberation Mono,monospace;font-size:8.5pt;">Tableau/Netflix &amp; TV Show.twbx</span></td></tr>
    <tr><th>Publication</th><td>Python pipeline <span style="font-family:Liberation Mono,monospace;font-size:8.5pt;">python -m netflix_catalog</span> → figures/viz_*.png</td></tr>
    <tr><th>Document</th><td>Course report (academic rewrite). Dual evidence: left Tableau, right Python.</td></tr>
  </table>
  {banner}
  <p class="cover-note">
    Working paper for the studio course. Unit of analysis is a title, not a viewer.
    This PDF supersedes the September 2025 Word draft (heart-disease copy-paste, rating-as-reviews,
    country-as-filming-location, and ranking “Không xác định” as a country are corrected).
  </p>
</section>
"""

TOC = """
<section class="front-matter">
  <div class="abstract-label">Contents</div>
  <h1 style="page-break-before:avoid;border-bottom:1.4pt solid #b4232c;">Contents</h1>
  <ul class="toc">
    <li><a href="#abstract">Abstract</a></li>
    <li><a href="#how-to-read-the-dual-evidence">How to read the dual evidence</a></li>
    <li><a href="#1-introduction">1. Introduction</a></li>
    <li><a href="#2-related-work-and-theoretical-frame">2. Related work and theoretical frame</a></li>
    <li><a href="#3-research-protocol-stanford-dschool">3. Research protocol (Stanford d.school)</a></li>
    <li><a href="#4-data-provenance-and-methods">4. Data, provenance, and methods</a></li>
    <li><a href="#5-visualization-grammar-shared">5. Visualization grammar</a></li>
    <li><a href="#6-domain-tasks-nested-model-dual-evidence">6. Domain tasks — nested model, dual evidence</a></li>
    <li><a href="#7-synthesis">7. Synthesis</a></li>
    <li><a href="#8-what-this-study-does-not-claim">8. What this study does not claim</a></li>
    <li><a href="#9-threats-to-validity">9. Threats to validity</a></li>
    <li><a href="#10-reproducibility">10. Reproducibility</a></li>
    <li><a href="#references">References</a></li>
    <li><a href="#appendix-a-errata-of-the-original-studio-pdf">Appendix A. Errata of the studio draft</a></li>
    <li><a href="#appendix-b-figure-index-tableau--python">Appendix B. Figure index</a></li>
  </ul>
</section>
"""


def md_to_html(source: str) -> str:
    source = re.sub(r"```mermaid[\s\S]*?```", "", source)
    source = source.replace("](../", "](")
    source = source.replace('src="../', 'src="')
    html = markdown.markdown(
        source,
        extensions=["tables", "fenced_code", "sane_lists", "smarty", "toc"],
        extension_configs={"toc": {"permalink": False}},
    )
    html = html.replace(
        "<table>\n<tr>\n<th align=\"center\" width=\"50%\">Tableau</th>",
        '<table class="pair">\n<tr>\n<th align="center" width="50%">Tableau</th>',
    )
    html = html.replace("<h2>Abstract</h2>", '<h2 id="abstract">Abstract</h2>', 1)
    html = html.replace("<h2>References</h2>", '<h2 id="references">References</h2>', 1)
    return html


def build() -> Path:
    source = MD_PATH.read_text(encoding="utf-8")
    cut = source.find("## Abstract")
    if cut == -1:
        raise SystemExit("ACADEMIC_REPORT.md has no ## Abstract heading")
    source = source[cut:]
    body = md_to_html(source)
    banner = ""
    if COVER_BANNER.exists():
        banner = f'<img class="cover-banner" src="{COVER_BANNER.as_uri()}" alt="Netflix catalog still"/>'
    cover = COVER.format(banner=banner)
    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>Netflix Movies and TV Shows — The catalog as designed supply</title>
</head>
<body>
{cover}
{TOC}
<article class="paper">
{body}
</article>
</body>
</html>
"""
    HTML_OUT.write_text(document, encoding="utf-8")
    HTML(string=document, base_url=str(ROOT)).write_pdf(
        OUT_PDF,
        stylesheets=[CSS(filename=str(CSS_PATH))],
    )
    return OUT_PDF


if __name__ == "__main__":
    path = build()
    print(f"wrote {path} ({path.stat().st_size / 1024:.0f} KB)")
    print(f"preview_html {HTML_OUT}")
