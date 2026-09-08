"""Mappings, grains, and visualization tokens.

Maturity bands are title-level recodes of parental-guideline ratings.
They are not viewer ages.
"""

from __future__ import annotations

# Louis C.K. specials: duration leaked into `rating` in the Kaggle extract.
DURATION_AS_RATING = {"66 min", "74 min", "84 min"}

KIDS_RATINGS = {"TV-Y", "TV-Y7", "TV-Y7-FV", "G", "TV-G"}
TEENS_RATINGS = {"PG", "TV-PG", "TV-14"}
ADULTS_RATINGS = {"PG-13", "R", "NC-17", "TV-MA"}
UNRATED_RATINGS = {"NR", "UR"}

# Household co-viewing inventory — not a demand segment.
FAMILY_ADJACENT_RATINGS = {
    "G",
    "TV-Y",
    "TV-Y7",
    "TV-Y7-FV",
    "TV-G",
    "PG",
    "TV-PG",
}

MATURITY_BAND_ORDER = ["Kids", "Teens", "Adults", "Unrated", "Unknown"]

RATING_DISPLAY_ORDER = [
    "TV-Y",
    "TV-Y7",
    "TV-Y7-FV",
    "G",
    "TV-G",
    "PG",
    "TV-PG",
    "PG-13",
    "TV-14",
    "R",
    "NC-17",
    "TV-MA",
    "NR",
    "UR",
    "Unknown",
]

# Paul Tol + Netflix red. Colorblind-safe categorical set.
PALETTE = {
    "red": "#E50914",
    "red_dark": "#B20710",
    "ink": "#221F1F",
    "ink_muted": "#564D4D",
    "grid": "#E8E6E3",
    "rule": "#D0CBC4",
    "paper": "#FFFBFC",
    "movie": "#E50914",
    "tv": "#1C69A7",  # Tol blue, not Netflix rainbow
    "kids": "#4C9F38",
    "teens": "#EEBB33",
    "adults": "#E50914",
    "unrated": "#888780",
    "unknown": "#9B8AA6",
    "accent": "#46D369",
    "heat": "#E50914",
}

TYPE_COLORS = {"Movie": PALETTE["movie"], "TV Show": PALETTE["tv"]}
BAND_COLORS = {
    "Kids": PALETTE["kids"],
    "Teens": PALETTE["teens"],
    "Adults": PALETTE["adults"],
    "Unrated": PALETTE["unrated"],
    "Unknown": PALETTE["unknown"],
}

SOURCE_NOTE = (
    "Source: Kaggle / Flixable Netflix titles extract. "
    "Unit of analysis is a title, not a viewer. "
    "date_added ends 2021-09-25 (2021 is right-censored)."
)
