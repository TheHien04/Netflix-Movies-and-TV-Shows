"""Publication figures. Sentence titles, labeled grain, missingness as a KPI."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

from .constants import (
    BAND_COLORS,
    MATURITY_BAND_ORDER,
    PALETTE,
    RATING_DISPLAY_ORDER,
    SOURCE_NOTE,
    TYPE_COLORS,
)
from .clean import ROOT

FIGURES = ROOT / "figures"


def apply_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titlesize": 14.5,
            "axes.titleweight": "bold",
            "axes.titlelocation": "left",
            "axes.titlepad": 8,
            "axes.labelsize": 10.5,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.spines.left": False,
            "axes.spines.bottom": True,
            "axes.edgecolor": PALETTE["rule"],
            "axes.linewidth": 0.8,
            "axes.grid": True,
            "axes.axisbelow": True,
            "grid.color": PALETTE["grid"],
            "grid.linewidth": 0.7,
            "grid.linestyle": "-",
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "text.color": PALETTE["ink"],
            "axes.labelcolor": PALETTE["ink_muted"],
            "xtick.color": PALETTE["ink_muted"],
            "ytick.color": PALETTE["ink_muted"],
            "xtick.major.size": 0,
            "ytick.major.size": 0,
            "legend.frameon": False,
            "figure.dpi": 140,
            "savefig.dpi": 200,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.28,
        }
    )


def headline(fig: plt.Figure, title: str, subtitle: str, *, left: float = 0.08, plot_left: float | None = None) -> None:
    """Title and subtitle live in figure space so they cannot collide with the axes title."""
    fig.subplots_adjust(top=0.78, bottom=0.14, left=plot_left or 0.10, right=0.97)
    fig.text(left, 0.97, title, fontsize=15, fontweight="bold", va="top", color=PALETTE["ink"])
    fig.text(left, 0.905, subtitle, fontsize=9.5, va="top", color=PALETTE["ink_muted"], linespacing=1.4)


def _footer(fig, grain: str) -> None:
    fig.text(
        0.08,
        0.04,
        f"{SOURCE_NOTE}\nGrain: {grain}",
        ha="left",
        va="top",
        color=PALETTE["ink_muted"],
        fontsize=8,
        linespacing=1.35,
        transform=fig.transFigure,
    )


def _save(fig: plt.Figure, name: str) -> Path:
    FIGURES.mkdir(parents=True, exist_ok=True)
    path = FIGURES / name
    fig.savefig(path)
    plt.close(fig)
    return path


def fig_additions(titles: pd.DataFrame) -> Path:
    counts = titles.dropna(subset=["year_added"]).groupby("year_added").size().astype(int)
    years = counts.index.astype(int)
    fig, ax = plt.subplots(figsize=(11.2, 6.4))
    headline(
        fig,
        "Catalog additions peaked in 2019 — 2021 is an incomplete year",
        "Titles by year of date_added. 2021 stops on 25 September, so it is not comparable to a full year.",
    )
    ax.set_axisbelow(True)
    ax.yaxis.grid(True)
    ax.xaxis.grid(False)
    colors = [PALETTE["red"] if y != 2021 else "#F4A8AD" for y in years]
    bars = ax.bar(years, counts.values, color=colors, width=0.78)
    for bar, value, year in zip(bars, counts.values, years):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 40,
            f"{value:,}",
            ha="center",
            va="bottom",
            fontsize=8.5,
            color=PALETTE["ink"] if year != 2021 else PALETTE["ink_muted"],
        )
    ax.set_ylabel("Titles added")
    ax.set_xlabel("")
    ax.set_xlim(years.min() - 0.6, years.max() + 0.6)
    ax.annotate(
        "Right-censored\n(through 25 Sep)",
        xy=(2021, counts.loc[2021]),
        xytext=(2014.2, counts.max() * 0.72),
        fontsize=9,
        color=PALETTE["ink_muted"],
        arrowprops=dict(arrowstyle="-|>", color=PALETTE["ink_muted"], lw=0.8),
    )
    _footer(fig, "one title")
    return _save(fig, "01_catalog_additions.png")


def fig_missingness(titles: pd.DataFrame) -> Path:
    fields = [
        ("director_unknown", "Director"),
        ("country_unknown", "Country"),
        ("cast_unknown", "Cast"),
    ]
    types = ["Movie", "TV Show"]
    fig, ax = plt.subplots(figsize=(11.2, 6.2))
    headline(
        fig,
        "Missing director is a TV-show schema, not a data hole",
        "Percent missing by type. Filling these with a display string hides the pattern. Keep NULL in analytic tables.",
        left=0.16,
        plot_left=0.16,
    )
    ax.xaxis.grid(True)
    ax.yaxis.grid(False)
    y = np.arange(len(fields))
    height = 0.36
    for i, t in enumerate(types):
        subset = titles[titles["type"] == t]
        values = [100 * subset[col].mean() for col, _ in fields]
        offset = -height / 2 if i == 0 else height / 2
        bars = ax.barh(y + offset, values, height=height, color=TYPE_COLORS[t], label=t)
        for bar, val in zip(bars, values):
            ax.text(val + 0.8, bar.get_y() + bar.get_height() / 2, f"{val:.1f}%", va="center", fontsize=9, color=PALETTE["ink"])
    ax.set_yticks(y)
    ax.set_yticklabels([label for _, label in fields])
    ax.set_xlim(0, 105)
    ax.set_xlabel("Share of titles with the field missing")
    ax.legend(loc="lower right")
    _footer(fig, "one title")
    return _save(fig, "02_missingness_by_type.png")


def fig_maturity(titles: pd.DataFrame) -> Path:
    rating = titles["rating"].fillna("Unknown")
    counts = rating.value_counts()
    order = [r for r in RATING_DISPLAY_ORDER if r in counts.index]
    values = [int(counts[r]) for r in order]
    band_for = {r: titles.loc[titles["rating"].fillna("Unknown").eq(r), "maturity_band"].iloc[0] if r != "Unknown" else "Unknown" for r in order}
    # Unknown rating rows
    band_for["Unknown"] = "Unknown"
    colors = [BAND_COLORS.get(band_for[r], PALETTE["unknown"]) for r in order]
    fig, ax = plt.subplots(figsize=(11.2, 6.8))
    family_n = int(titles["family_adjacent"].sum())
    tv_ma_14 = int(titles["rating"].isin(["TV-MA", "TV-14"]).sum())
    headline(
        fig,
        "The catalog is built for mature individual viewing",
        f"TV-MA + TV-14 = {tv_ma_14:,} titles ({tv_ma_14 / len(titles):.1%}). "
        f"Family-adjacent ratings = {family_n:,} ({family_n / len(titles):.1%}). "
        "This is inventory mix, not audience preference.",
    )
    ax.xaxis.grid(False)
    ax.yaxis.grid(True)
    bars = ax.bar(range(len(order)), values, color=colors, width=0.78)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(order, rotation=40, ha="right")
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 35, f"{val:,}", ha="center", fontsize=8, color=PALETTE["ink"])
    handles = [
        plt.Rectangle((0, 0), 1, 1, color=BAND_COLORS[b], label=b)
        for b in ["Kids", "Teens", "Adults", "Unrated", "Unknown"]
    ]
    ax.legend(handles=handles, loc="upper right", title="Maturity band")
    ax.set_ylabel("Titles")
    _footer(fig, "one title")
    return _save(fig, "03_maturity_mix.png")


def fig_countries(titles: pd.DataFrame, countries: pd.DataFrame) -> Path:
    unknown = int(titles["country_unknown"].sum())
    stacked = (
        countries.groupby(["country_credit", "type"]).size().unstack(fill_value=0)
    )
    if "Movie" not in stacked:
        stacked["Movie"] = 0
    if "TV Show" not in stacked:
        stacked["TV Show"] = 0
    stacked["total"] = stacked["Movie"] + stacked["TV Show"]
    top = stacked.sort_values("total", ascending=True).tail(10)
    fig, ax = plt.subplots(figsize=(11.2, 6.8))
    headline(
        fig,
        "Production credits are concentrated — Unknown is not a country",
        f"{unknown:,} titles ({unknown / len(titles):.1%}) have no production country and are excluded from this ranking. "
        "Japan and South Korea are series-heavy; India is movie-heavy. Credits ≠ filming location ≠ viewership.",
        left=0.18,
        plot_left=0.18,
    )
    ax.xaxis.grid(True)
    ax.yaxis.grid(False)
    y = np.arange(len(top))
    ax.barh(y, top["Movie"], color=TYPE_COLORS["Movie"], label="Movie")
    ax.barh(y, top["TV Show"], left=top["Movie"], color=TYPE_COLORS["TV Show"], label="TV Show")
    ax.set_yticks(y)
    ax.set_yticklabels(top.index)
    for i, (_, row) in enumerate(top.iterrows()):
        ax.text(row["total"] + 30, i, f"{int(row['total']):,}", va="center", fontsize=9, color=PALETTE["ink"])
    ax.set_xlabel("Production credits (a co-production counts once per country)")
    ax.legend(loc="lower right")
    ax.set_xlim(0, top["total"].max() * 1.14)
    _footer(fig, "one country-credit (exploded)")
    return _save(fig, "04_producing_countries.png")


def fig_genres(genres: pd.DataFrame) -> Path:
    counts = genres["genre"].value_counts().head(15).sort_values()
    fig, ax = plt.subplots(figsize=(11.2, 7.2))
    headline(
        fig,
        "Genre is a tag cloud, not a partition of the catalog",
        "Top 15 listed_in tags. “International” is a platform taxonomy, not a film-studies genre.",
        left=0.22,
        plot_left=0.22,
    )
    ax.xaxis.grid(True)
    ax.yaxis.grid(False)
    y = np.arange(len(counts))
    ax.hlines(y, 0, counts.values, color=PALETTE["rule"], lw=1.2)
    ax.scatter(counts.values, y, s=42, color=PALETTE["red"], zorder=3)
    for i, val in enumerate(counts.values):
        ax.text(val + 40, i, f"{int(val):,}", va="center", fontsize=9)
    ax.set_yticks(y)
    ax.set_yticklabels(counts.index)
    ax.set_xlabel("Tag incidences (a title with 3 tags contributes 3)")
    _footer(fig, "one genre-credit (exploded)")
    return _save(fig, "05_genre_incidence.png")


def fig_rating_genre(genres: pd.DataFrame) -> Path:
    top_genres = genres["genre"].value_counts().head(12).index.tolist()
    rating_order = [r for r in RATING_DISPLAY_ORDER if r in set(genres["rating"].fillna("Unknown"))]
    sub = genres[genres["genre"].isin(top_genres)].copy()
    sub["rating"] = sub["rating"].fillna("Unknown")
    table = (
        sub.groupby(["genre", "rating"]).size().unstack(fill_value=0).reindex(index=top_genres, columns=rating_order, fill_value=0)
    )
    cmap = LinearSegmentedColormap.from_list("netflix_heat", ["#FFF7F7", "#F4A8AD", PALETTE["red_dark"]])
    fig, ax = plt.subplots(figsize=(12.0, 7.4))
    headline(
        fig,
        "Rating × genre is a cross-tab of inventory, not a correlation",
        "Cell = (title, genre tag) pairs. A large cell is tagging policy, not “this audience prefers this genre.”",
    )
    ax.grid(False)
    im = ax.imshow(table.values, aspect="auto", cmap=cmap)
    ax.set_xticks(range(len(table.columns)))
    ax.set_xticklabels(table.columns, rotation=40, ha="right")
    ax.set_yticks(range(len(table.index)))
    ax.set_yticklabels(table.index)
    vmax = table.values.max()
    for i in range(table.shape[0]):
        for j in range(table.shape[1]):
            val = int(table.values[i, j])
            if val == 0:
                continue
            color = "white" if val > vmax * 0.55 else PALETTE["ink"]
            ax.text(j, i, f"{val:,}", ha="center", va="center", fontsize=7, color=color)
    fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02, label="Tag incidences")
    _footer(fig, "one genre-credit (exploded)")
    return _save(fig, "06_rating_genre_crosstab.png")


def fig_maturity_over_time(titles: pd.DataFrame) -> Path:
    sub = titles.dropna(subset=["year_added"]).copy()
    sub = sub[sub["year_added"] >= 2015]
    counts = (
        sub.groupby(["year_added", "maturity_band"]).size().unstack(fill_value=0)
    )
    for band in MATURITY_BAND_ORDER:
        if band not in counts:
            counts[band] = 0
    counts = counts[MATURITY_BAND_ORDER]
    fig, ax = plt.subplots(figsize=(11.2, 6.4))
    headline(
        fig,
        "Mature titles dominate every add-year of the expansion era",
        "Stacked counts by year_added, 2015–2021. 2021 is truncated. Band is a recode of rating, not viewers.",
    )
    ax.xaxis.grid(False)
    years = counts.index.astype(int)
    bottom = np.zeros(len(counts))
    for band in MATURITY_BAND_ORDER:
        vals = counts[band].values
        ax.bar(years, vals, bottom=bottom, color=BAND_COLORS[band], label=band, width=0.78)
        bottom += vals
    ax.legend(loc="upper left", ncol=5)
    ax.set_ylabel("Titles added")
    _footer(fig, "one title")
    return _save(fig, "07_maturity_over_add_year.png")


def fig_briefing(titles: pd.DataFrame, countries: pd.DataFrame) -> Path:
    """One-page briefing board a VP can read in 30 seconds."""
    fig = plt.figure(figsize=(12.4, 8.2))
    fig.subplots_adjust(top=0.86, bottom=0.08, left=0.08, right=0.97)
    gs = fig.add_gridspec(2, 2, hspace=0.48, wspace=0.32, top=0.82, bottom=0.10)
    fig.text(0.08, 0.97, "Netflix catalog supply — briefing board", fontsize=16, fontweight="bold", color=PALETTE["ink"], va="top")
    fig.text(
        0.08,
        0.925,
        "N = 8,807 titles  ·  Last date_added = 2021-09-25  ·  No viewing data in this file",
        color=PALETTE["ink_muted"],
        fontsize=10,
        va="top",
    )

    ax1 = fig.add_subplot(gs[0, 0])
    counts = titles.dropna(subset=["year_added"]).groupby("year_added").size()
    years = counts.index.astype(int)
    colors = [PALETTE["red"] if y != 2021 else "#F4A8AD" for y in years]
    ax1.bar(years, counts.values, color=colors, width=0.8)
    ax1.set_title("Additions peak in 2019", loc="left", fontsize=12)
    ax1.xaxis.grid(False)
    ax1.set_ylabel("Titles")

    ax2 = fig.add_subplot(gs[0, 1])
    share = titles["maturity_band"].value_counts().reindex(MATURITY_BAND_ORDER).fillna(0)
    ax2.barh(share.index[::-1], share.values[::-1], color=[BAND_COLORS[b] for b in share.index[::-1]])
    ax2.yaxis.grid(False)
    ax2.set_title("Adults + Teens are the catalog", loc="left", fontsize=12)
    for i, (band, val) in enumerate(share[::-1].items()):
        ax2.text(val + 40, i, f"{int(val):,}", va="center", fontsize=9)

    ax3 = fig.add_subplot(gs[1, 0])
    miss = pd.Series(
        {
            "Director\n(TV Show)": titles.loc[titles["type"] == "TV Show", "director_unknown"].mean() * 100,
            "Director\n(Movie)": titles.loc[titles["type"] == "Movie", "director_unknown"].mean() * 100,
            "Country": titles["country_unknown"].mean() * 100,
            "Cast": titles["cast_unknown"].mean() * 100,
        }
    )
    ax3.barh(miss.index[::-1], miss.values[::-1], color=PALETTE["tv"])
    ax3.yaxis.grid(False)
    ax3.set_title("Missingness is structured", loc="left", fontsize=12)
    ax3.set_xlabel("% missing")

    ax4 = fig.add_subplot(gs[1, 1])
    top = countries["country_credit"].value_counts().head(8).sort_values()
    ax4.barh(top.index, top.values, color=PALETTE["red"])
    ax4.yaxis.grid(False)
    ax4.set_title("U.S. still anchors production credits", loc="left", fontsize=12)
    ax4.set_xlabel("Credits")

    fig.text(0.08, 0.03, SOURCE_NOTE, color=PALETTE["ink_muted"], fontsize=8)
    FIGURES.mkdir(parents=True, exist_ok=True)
    path = FIGURES / "08_briefing_board.png"
    fig.savefig(path)
    plt.close(fig)
    return path


def render_all(titles: pd.DataFrame, genres: pd.DataFrame, countries: pd.DataFrame) -> list[Path]:
    apply_style()
    return [
        fig_additions(titles),
        fig_missingness(titles),
        fig_maturity(titles),
        fig_countries(titles, countries),
        fig_genres(genres),
        fig_rating_genre(genres),
        fig_maturity_over_time(titles),
        fig_briefing(titles, countries),
    ]
