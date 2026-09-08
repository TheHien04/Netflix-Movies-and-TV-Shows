# Visualization specs

Publication figures in `figures/` are dark editorial cards designed to sit on a white GitHub README. Tableau remains the **interactive prototype**; Python is the **corrected readout**.

## Design tokens

| Token | Value | Use |
|---|---|---|
| Canvas | `#0E0E0E` | Figure background |
| Panel | `#161616` | Plot area |
| Netflix red | `#E50914` | Highlight, movies, kicker |
| Dim red | `#7A1218` | Context bars (not the peak) |
| TV blue | `#5BA3D9` | TV Shows |
| Kids / Teens / Adults | `#3DDC84` / `#F5C518` / `#E50914` | Maturity bands |
| Ink / muted | `#F4F1EA` / `#A39E96` | Title vs axis |
| Typeface | Inter | Titles semibold, labels regular |

## Grammar

1. **Title is a sentence.** Finding first, chart type never.
2. **Kicker** names the study or the Tableau sheet being rewritten.
3. **Highlight encoding.** Peak / top-N in bright red or the band color; everything else recedes (`#7A1218` or gray).
4. **Spaghetti is muted.** Genre trends: top five in color, remaining tags in gray.
5. **Missingness is a KPI.** Unknown is never a country.
6. **Grain and source** on every figure, including 2021-09-25 right-censor.
7. **Heatmap is a cross-tab.** Do not say correlation unless a coefficient is computed.
8. **No dual axis, no 3D, no rainbow categorical.**

## Tableau ↔ Python

| Tableau export | Publication figure |
|---|---|
| Dashboard.png | `08_briefing_board.png` |
| Content by years.png | `09_library_by_release_year.png` + `01_catalog_additions.png` |
| Top 10 producing countries.png | `04_producing_countries.png` |
| Distribution of content followed by countries.png | choropleth kept; ranking in `04` |
| Trend in publishing over years.png | `10_genre_trends.png` + `05_genre_incidence.png` |
| Number of Content followed by rating.png | `03_maturity_mix.png` |
| Number of rating's content years.png | `11_rating_over_release_year.png` + `07_maturity_over_add_year.png` |
| Age rating category correlations.png | `06_rating_genre_crosstab.png` |
| Distribution cast with different listed in.png | `12_cast_by_genre.png` |
