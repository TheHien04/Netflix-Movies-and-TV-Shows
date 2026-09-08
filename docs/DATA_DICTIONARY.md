# Data dictionary

Canonical tables live in `data/processed/`. Analytic tables keep `NULL`. The Tableau extract is the only file that uses the English label `Unknown`.

Machine-readable copies:

- [`data/dictionaries/field_dictionary.csv`](../data/dictionaries/field_dictionary.csv)
- [`data/dictionaries/maturity_band_codebook.csv`](../data/dictionaries/maturity_band_codebook.csv)
- [`data/processed/quality_report.md`](../data/processed/quality_report.md)

## Grains

| Table | Grain | Rows (this extract) |
|---|---|---|
| `netflix_titles.csv` | one title (`show_id`) | 8,807 |
| `netflix_title_genres.csv` | one (`show_id`, genre tag) | 19,323 |
| `netflix_title_countries.csv` | one (`show_id`, country credit) | ~10,012 |
| `netflix_titles_tableau.csv` | one title, display fills | 8,807 |

Exploded counts are **incidences**. A three-genre title is three genre rows. A US–India co-production is two country rows.

## Maturity band (not viewer age)

| Band | Ratings |
|---|---|
| Kids | `TV-Y`, `TV-Y7`, `TV-Y7-FV`, `G`, `TV-G` |
| Teens | `PG`, `TV-PG`, `TV-14` |
| Adults | `PG-13`, `R`, `NC-17`, `TV-MA` |
| Unrated | `NR`, `UR` |
| Unknown | null, plus three recoded Louis C.K. rows |

`family_adjacent` = Kids ratings plus `PG` and `TV-PG` (excludes `TV-14`).

## Recodes

Three stand-up specials had runtime in `rating` (`66 min`, `74 min`, `84 min`) and null `duration`. Pipeline moves the runtime back to `duration` and sets `rating` to null (`rating_was_duration = True`).
