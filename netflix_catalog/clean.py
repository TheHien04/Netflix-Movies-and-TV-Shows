"""Title-grain wrangling for the Netflix catalog extract.

Presentation fills belong in the viz layer. Statistical missingness stays NULL
in the analytic tables. The Tableau-friendly 12-column file uses the English
label "Unknown" only where a BI tool cannot plot nulls.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .constants import (
    ADULTS_RATINGS,
    DURATION_AS_RATING,
    FAMILY_ADJACENT_RATINGS,
    KIDS_RATINGS,
    TEENS_RATINGS,
    UNRATED_RATINGS,
)

ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = ROOT / "data" / "raw" / "netflix_titles.csv"
PROCESSED = ROOT / "data" / "processed"
DICTIONARIES = ROOT / "data" / "dictionaries"

TITLE_COLUMNS = [
    "show_id",
    "type",
    "title",
    "director",
    "cast",
    "country",
    "date_added",
    "release_year",
    "rating",
    "duration",
    "listed_in",
    "description",
]


def maturity_band(rating: object) -> str:
    if rating is None or (isinstance(rating, float) and pd.isna(rating)):
        return "Unknown"
    value = str(rating).strip()
    if value in {"", "Unknown"}:
        return "Unknown"
    if value in KIDS_RATINGS:
        return "Kids"
    if value in TEENS_RATINGS:
        return "Teens"
    if value in ADULTS_RATINGS:
        return "Adults"
    if value in UNRATED_RATINGS:
        return "Unrated"
    return "Unknown"


def recode_duration_rating_swap(frame: pd.DataFrame) -> pd.DataFrame:
    """Move leaked runtimes out of `rating` (three Louis C.K. specials)."""
    out = frame.copy()
    leaked = out["rating"].isin(DURATION_AS_RATING) & out["duration"].isna()
    out.loc[leaked, "duration"] = out.loc[leaked, "rating"]
    out.loc[leaked, "rating"] = pd.NA
    out["rating_was_duration"] = leaked
    return out


def parse_date_added(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    parsed = pd.to_datetime(out["date_added"].astype("string").str.strip(), errors="coerce")
    out["date_added_parsed"] = parsed
    out["year_added"] = parsed.dt.year.astype("Int64")
    out["month_added"] = parsed.dt.month.astype("Int64")
    out["year_added_incomplete"] = out["year_added"] == 2021
    return out


def parse_duration(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    raw = out["duration"].astype("string")
    out["duration_value"] = pd.to_numeric(raw.str.extract(r"(\d+)", expand=False), errors="coerce").astype("Int64")
    out["duration_unit"] = pd.NA
    out.loc[raw.str.contains("min", na=False), "duration_unit"] = "minutes"
    out.loc[raw.str.contains("Season", na=False), "duration_unit"] = "seasons"
    return out


def annotate_title_fields(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    out["rating"] = out["rating"].astype("string")
    out.loc[out["rating"].isin(list(DURATION_AS_RATING)), "rating"] = pd.NA
    out["maturity_band"] = out["rating"].map(maturity_band)
    out["family_adjacent"] = out["rating"].isin(FAMILY_ADJACENT_RATINGS)
    out["n_genre_tags"] = (
        out["listed_in"].astype("string").fillna("").map(lambda s: 0 if s == "" else len([p for p in s.split(",") if p.strip()]))
    )
    out["n_countries"] = (
        out["country"].astype("string").fillna("").map(lambda s: 0 if s == "" else len([p for p in s.split(",") if p.strip()]))
    )
    out["n_cast"] = (
        out["cast"].astype("string").fillna("").map(lambda s: 0 if s == "" else len([p for p in s.split(",") if p.strip()]))
    )
    out["country_unknown"] = out["country"].isna()
    out["director_unknown"] = out["director"].isna()
    out["cast_unknown"] = out["cast"].isna()
    return out


def clean_titles(raw: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in TITLE_COLUMNS if c not in raw.columns]
    if missing:
        raise ValueError(f"Raw extract missing columns: {missing}")
    out = raw[TITLE_COLUMNS].copy()
    out["show_id"] = out["show_id"].astype("string").str.strip()
    if out["show_id"].duplicated().any():
        raise ValueError("show_id is not unique")
    out = recode_duration_rating_swap(out)
    out = parse_date_added(out)
    out = parse_duration(out)
    out = annotate_title_fields(out)
    return out


def explode_comma(frame: pd.DataFrame, column: str, out_name: str) -> pd.DataFrame:
    base = frame.loc[:, ["show_id", "type", "rating", "maturity_band", "year_added", column]].copy()
    split = base[column].astype("string").fillna("").str.split(",")
    exploded = base.assign(**{out_name: split}).explode(out_name, ignore_index=True)
    exploded[out_name] = exploded[out_name].str.strip()
    exploded = exploded[exploded[out_name].ne("") & exploded[out_name].notna()]
    return exploded.drop(columns=[column])


def tableau_friendly(titles: pd.DataFrame) -> pd.DataFrame:
    """Original 12-column schema with English Unknown fills for BI tools."""
    out = titles[TITLE_COLUMNS].copy()
    out["director"] = out["director"].fillna("Unknown")
    out["cast"] = out["cast"].fillna("Unknown")
    out["country"] = out["country"].fillna("Unknown")
    out["date_added"] = out["date_added"].fillna("Unknown")
    out["rating"] = out["rating"].fillna("Unknown")
    out["duration"] = out["duration"].fillna("Unknown")
    return out


def write_codebooks(titles: pd.DataFrame) -> None:
    DICTIONARIES.mkdir(parents=True, exist_ok=True)
    fields = [
        ("show_id", "title", "Primary key in this extract"),
        ("type", "title", "Movie or TV Show"),
        ("title", "title", "Display name; not a key"),
        ("director", "title", "Comma-separated credits; missingness is structural for TV Shows"),
        ("cast", "title", "Comma-separated credits"),
        ("country", "title", "Production credits, not filming location; explode for incidence"),
        ("date_added", "title", "Netflix availability date; strip before parse"),
        ("release_year", "title", "Original release year, not add year"),
        ("rating", "title", "Parental-guideline / MPAA-style maturity label, not a quality score"),
        ("duration", "title", "Heterogeneous: minutes for movies, seasons for shows"),
        ("listed_in", "title", "Multi-label genre tags (1–3)"),
        ("description", "title", "Short synopsis"),
        ("date_added_parsed", "title", "ISO date; 10 raw nulls remain null"),
        ("year_added", "title", "Policy clock for catalog growth"),
        ("duration_value", "title", "Integer minutes or season count"),
        ("duration_unit", "title", "minutes or seasons"),
        ("maturity_band", "title", "Derived from rating; not viewer age"),
        ("family_adjacent", "title", "Kids ratings plus PG / TV-PG"),
        ("country_unknown", "title", "True when production country is missing"),
        ("genre", "genre-credit", "One listed_in tag; counts are incidences"),
        ("country_credit", "country-credit", "One production country; multi-credited titles appear once per country"),
    ]
    pd.DataFrame(fields, columns=["field", "grain", "definition"]).to_csv(
        DICTIONARIES / "field_dictionary.csv", index=False
    )

    bands = (
        titles.groupby(["rating", "maturity_band", "family_adjacent"], dropna=False)
        .size()
        .reset_index(name="titles")
        .sort_values(["maturity_band", "rating"], na_position="last")
    )
    bands.to_csv(DICTIONARIES / "maturity_band_codebook.csv", index=False)


def build(raw_path: Path = RAW_PATH) -> dict[str, pd.DataFrame]:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    if not raw_path.exists():
        fallback = ROOT / "netflix_titles.csv"
        if not fallback.exists():
            raise FileNotFoundError(raw_path)
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        fallback_df = pd.read_csv(fallback)
        fallback_df.to_csv(raw_path, index=False)

    raw = pd.read_csv(raw_path)
    titles = clean_titles(raw)
    genres = explode_comma(titles, "listed_in", "genre")
    countries = explode_comma(titles, "country", "country_credit")
    friendly = tableau_friendly(titles)

    titles.to_csv(PROCESSED / "netflix_titles.csv", index=False)
    genres.to_csv(PROCESSED / "netflix_title_genres.csv", index=False)
    countries.to_csv(PROCESSED / "netflix_title_countries.csv", index=False)
    friendly.to_csv(PROCESSED / "netflix_titles_tableau.csv", index=False)

    # Root compatibility extracts (English Unknown, recoded ratings).
    friendly.to_csv(ROOT / "netflix_titles_cleaned.csv", index=False)
    genre_compat = genres.rename(columns={"genre": "listed_in"}).loc[:, ["show_id", "rating", "listed_in", "maturity_band"]]
    genre_compat = genre_compat.rename(columns={"maturity_band": "Age Group"})
    genre_compat.to_csv(ROOT / "netflix_titles_genres_split.csv", index=False)

    write_codebooks(titles)

    snapshot = {
        "n_titles": int(len(titles)),
        "n_movies": int((titles["type"] == "Movie").sum()),
        "n_shows": int((titles["type"] == "TV Show").sum()),
        "n_genre_rows": int(len(genres)),
        "n_country_credits": int(len(countries)),
        "country_unknown": int(titles["country_unknown"].sum()),
        "rating_was_duration": int(titles["rating_was_duration"].sum()),
        "date_added_max": str(titles["date_added_parsed"].max().date()),
        "year_added_peak": int(titles["year_added"].value_counts().idxmax()),
        "family_adjacent_share": round(float(titles["family_adjacent"].mean()), 4),
        "tv_ma_tv14_share": round(float(titles["rating"].isin(["TV-MA", "TV-14"]).mean()), 4),
    }
    (PROCESSED / "build_snapshot.json").write_text(json.dumps(snapshot, indent=2) + "\n")
    return {"titles": titles, "genres": genres, "countries": countries, "tableau": friendly}
