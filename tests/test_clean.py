"""Wrangling invariants for the Netflix catalog extract."""

from pathlib import Path

import pandas as pd
import pytest

from netflix_catalog.clean import clean_titles, explode_comma, tableau_friendly
from netflix_catalog.constants import DURATION_AS_RATING, FAMILY_ADJACENT_RATINGS

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "netflix_titles.csv"


@pytest.fixture(scope="module")
def raw() -> pd.DataFrame:
    path = RAW if RAW.exists() else ROOT / "netflix_titles.csv"
    return pd.read_csv(path)


@pytest.fixture(scope="module")
def titles(raw: pd.DataFrame) -> pd.DataFrame:
    return clean_titles(raw)


def test_row_count(titles: pd.DataFrame) -> None:
    assert len(titles) == 8807


def test_show_id_unique(titles: pd.DataFrame) -> None:
    assert titles["show_id"].is_unique


def test_duration_no_longer_in_rating(titles: pd.DataFrame) -> None:
    assert ~titles["rating"].isin(DURATION_AS_RATING).any()
    assert int(titles["rating_was_duration"].sum()) == 3
    restored = titles.loc[titles["rating_was_duration"], "duration"]
    assert restored.notna().all()
    assert restored.str.contains("min").all()


def test_no_vietnamese_placeholders(titles: pd.DataFrame) -> None:
    blob = titles.astype("string").fillna("")
    for col in ["director", "cast", "country"]:
        assert ~blob[col].str.contains("Không").any()


def test_tableau_unknown_is_english(titles: pd.DataFrame) -> None:
    friendly = tableau_friendly(titles)
    assert (friendly["country"] == "Unknown").sum() == int(titles["country_unknown"].sum())
    assert ~friendly["country"].astype("string").str.contains("Không").any()


def test_right_censor_date(titles: pd.DataFrame) -> None:
    assert str(titles["date_added_parsed"].max().date()) == "2021-09-25"
    assert int(titles["year_added"].value_counts().idxmax()) == 2019


def test_family_adjacent_definition(titles: pd.DataFrame) -> None:
    expected = titles["rating"].isin(FAMILY_ADJACENT_RATINGS)
    assert titles["family_adjacent"].equals(expected)
    assert titles["family_adjacent"].mean() == pytest.approx(0.2337, abs=0.001)


def test_tv_show_director_missingness_is_structural(titles: pd.DataFrame) -> None:
    tv = titles.loc[titles["type"] == "TV Show", "director_unknown"].mean()
    movie = titles.loc[titles["type"] == "Movie", "director_unknown"].mean()
    assert tv > 0.85
    assert movie < 0.10


def test_genre_explode_preserves_all_titles(titles: pd.DataFrame) -> None:
    genres = explode_comma(titles, "listed_in", "genre")
    assert set(genres["show_id"]) == set(titles["show_id"])
    assert genres["genre"].isna().sum() == 0
    assert titles["n_genre_tags"].mean() == pytest.approx(2.19, abs=0.02)


def test_country_unknown_not_exploded_as_nation(titles: pd.DataFrame) -> None:
    countries = explode_comma(titles, "country", "country_credit")
    assert "Unknown" not in set(countries["country_credit"])
    assert "Không xác định" not in set(countries["country_credit"])
    assert int(titles["country_unknown"].sum()) == 831
