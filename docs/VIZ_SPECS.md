# Visualization specs

Publication figures in `figures/` share the **Tableau workbook’s cream canvas and Tableau 10 hues**, so they sit next to the prototype without a theme clash. Tableau remains the interactive prototype; Python is the corrected readout.

## Design tokens (from the workbook)

| Token | Value | Matches Tableau |
|---|---|---|
| Canvas | `#F4F1EC` | Worksheet cream |
| Panel | `#F8F6F2` | Plot area |
| Movie | `#E15759` | Salmon in Content by years / Top 10 |
| Movie (context) | `#E8A090` | Soft fill from the same sheet |
| TV Show | `#F28E2B` | Orange in Content by years / Top 10 |
| Adults / TV-MA | `#4E79A7` | Blue on Ratings over years |
| Teens | `#EDC948` | Tableau gold |
| Kids | `#59A14F` | Tableau green |
| Unrated / Unknown | `#9C755F` / `#BAB0AC` | Tableau brown / gray |
| Genre extras | `#B07AA1` purple, `#76B7B2` teal | Tableau 10 |
| Typeface | Inter | Publication layer (Tableau sheets stay serif) |

## Grammar

1. **Title is a sentence.** Finding first, chart type never.
2. **Kicker** names the study or the Tableau sheet being rewritten.
3. **Highlight encoding.** Peak in Tableau red; other years in salmon; 2021 in gray.
4. **Spaghetti is muted.** Genre trends: top five in Tableau 10; remaining tags in `#D5D0C8`.
5. **Missingness is a KPI.** Unknown is never a country.
6. **Grain and source** on every figure, including 2021-09-25 right-censor.
7. **Heatmap is a cross-tab** on a cream–coral sequential, not a rainbow.
8. **No dual axis, no 3D.**

## Tableau ↔ Python

| Tableau export | Publication figure |
|---|---|
| Dashboard.png | `pub_08_briefing_board.png` |
| Content by years.png | `pub_09_library_by_release_year.png` + `pub_01_catalog_additions.png` |
| Top 10 producing countries.png | `pub_04_producing_countries.png` |
| Distribution of content followed by countries.png | choropleth kept; ranking in `pub_04` |
| Trend in publishing over years.png | `pub_10_genre_trends.png` + `pub_05_genre_incidence.png` |
| Number of Content followed by rating.png | `pub_03_maturity_mix.png` |
| Number of rating's content years.png | `pub_11_rating_over_release_year.png` + `pub_07_maturity_over_add_year.png` |
| Age rating category correlations.png | `pub_06_rating_genre_crosstab.png` |
| Distribution cast with different listed in.png | `pub_12_cast_by_genre.png` |
