# Reports

| File | What it is |
|---|---|
| **[Report Project.pdf](./Report%20Project.pdf)** | Official course report (print, A4). Stanford Design Thinking + Munzner nested model. Every domain task is **Tableau \| Python**. Rebuild: `python3 Report/build_academic_pdf.py` (needs `weasyprint`). |
| [ACADEMIC_REPORT.md](./ACADEMIC_REPORT.md) | Source markdown for that PDF. |
| `studio-draft-Report-Project.pdf` | September 2025 Word export. Historical only — do not cite (see Appendix A). |

```bash
python3 -m pip install weasyprint markdown
python3 Report/build_academic_pdf.py
```
