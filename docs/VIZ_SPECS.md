# Visualization specs

Publication figures in `figures/` share the **Tableau workbook’s cream canvas and Tableau 10 hues**, so they sit next to the prototype without a theme clash. Tableau remains the interactive prototype; Python is the corrected readout.

## Design tokens (pixel-sampled from `Tableau/` PNGs)

| Token | Value | Matches Tableau |
|---|---|---|
| Canvas / panel | `#EFEBE8` | Worksheet cream (Top 10, Content by years, rating bars) |
| Movie | `#E15658` | Movie stack in Top 10 producing countries |
| Movie (context) | `#E79191` | Movie area in Content by years |
| TV Show | `#F28B25` | TV Show stack in Top 10 producing countries |
| Adults / TV-MA | `#4471A1` | Tableau blue on cast × listed_in |
| Teens | `#F1CF69` | Tableau gold on cast × listed_in |
| Kids | `#59A14F` | Tableau green |
| Unrated / Unknown | `#9C755F` / `#BAB0AC` | Tableau brown / gray |
| Genre extras | `#BC8FAE` purple, `#76B7B2` teal | Tableau 10 on the cast sheet |
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
| Dashboard.png | `viz_08_briefing_board.png` |
| Content by years.png | `viz_09_library_by_release_year.png` + `viz_01_catalog_additions.png` |
| Top 10 producing countries.png | `viz_04_producing_countries.png` |
| Distribution of content followed by countries.png | choropleth kept; ranking in `viz_04` |
| Trend in publishing over years.png | `viz_10_genre_trends.png` + `viz_05_genre_incidence.png` |
| Number of Content followed by rating.png | `viz_03_maturity_mix.png` |
| Number of rating's content years.png | `viz_11_rating_over_release_year.png` + `viz_07_maturity_over_add_year.png` |
| Age rating category correlations.png | `viz_06_rating_genre_crosstab.png` |
| Distribution cast with different listed in.png | `viz_12_cast_by_genre.png` |
