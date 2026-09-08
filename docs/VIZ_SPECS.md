# Visualization specs

Publication figures in `figures/` follow the same grammar a senior analytics team would enforce in review. Tableau remains the **interactive prototype**; these PNGs are the **corrected, reviewable layer**.

## Design tokens

| Token | Value | Use |
|---|---|---|
| Netflix red | `#E50914` | Primary measure, movies |
| Tol blue | `#1C69A7` | TV Shows (not a second red) |
| Ink | `#221F1F` | Titles |
| Muted | `#564D4D` | Axes, source lines |
| Kids / Teens / Adults | `#4C9F38` / `#EEBB33` / `#E50914` | Maturity bands |

Palette is colorblind-aware (Tol + Netflix red). Do not use rainbow categorical scales.

## Grammar (what “senior vis” means here)

1. **Title is a sentence** that states the finding, not the chart type. (“Catalog additions peaked in 2019 — 2021 is an incomplete year”, not “Bar chart of date added”.)
2. **Subtitle states grain, N, and the trap.** Every chart says whether a bar is a title, a genre-credit, or a country-credit.
3. **Missingness is a KPI**, never a fake country named Unknown / `Không xác định`.
4. **Direct labels** on bars. Legends only when encoding is not already in the title.
5. **Source line on every figure**, including the 2021-09-25 right-censor.
6. **No dual axis**, no 3D, no pie for mix > two slices when a bar communicates rank.
7. **Heatmap is a cross-tab.** File names and titles must not say “correlation” unless a coefficient is computed.

## Tableau prototype

`Tableau/Netflix & TV Show.twbx` is the course dashboard. Refresh it from `data/processed/netflix_titles_tableau.csv` (English `Unknown`, recoded Louis C.K. rows). Calculated fields should alias Unknown as “No production country” and keep it **out** of a Top 10 country ranking.

Chart titles inside the workbook still carry studio wording (“Number of rating's content years”). Prefer the Python figures for any external read-out until the workbook titles are rewritten to sentence form.
