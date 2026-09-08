"""Publication figures — Tableau-harmonious editorial theme.

Cream canvas, Tableau 10 hues sampled from the workbook, highlight encoding.
Tableau remains the interactive prototype; these PNGs are the readout.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager as fm
from matplotlib.colors import LinearSegmentedColormap

from .clean import ROOT
from .constants import (
    MATURITY_BAND_ORDER,
    RATING_DISPLAY_ORDER,
    SOURCE_NOTE,
)

FIGURES = ROOT / "figures"

# Pixel-sampled from Tableau/ exports so README Python + prototype share one palette.
BG = "#EFEBE8"       # worksheet cream (Top 10 / Content by years / rating bars)
PANEL = "#EFEBE8"    # same cream as Tableau — no white plot island
INK = "#2C2A28"
MUTED = "#6F6860"
FAINT = "#DDD6CC"
MOVIE = "#E15658"    # Movie stack in Top 10 producing countries
MOVIE_SOFT = "#E79191"  # Movie area in Content by years
TV = "#F28B25"       # TV Show stack in Top 10 producing countries
BLUE = "#4471A1"     # Tableau blue on cast × listed_in
TEAL = "#76B7B2"
GREEN = "#59A14F"
GOLD = "#F1CF69"     # Tableau gold on cast × listed_in
PURPLE = "#BC8FAE"   # Tableau purple on cast × listed_in
PINK = "#FF9DA7"
BROWN = "#9C755F"
GRAY = "#BAB0AC"
WHITE = "#FFFFFF"
ACCENT = MOVIE       # kicker / peak highlight, not Netflix #E50914

TYPE_COLORS = {"Movie": MOVIE, "TV Show": TV}
BAND_COLORS = {
    "Kids": GREEN,
    "Teens": GOLD,
    "Adults": BLUE,
    "Unrated": BROWN,
    "Unknown": GRAY,
}
HIGHLIGHT_GENRES = [
    "International Movies",
    "Dramas",
    "Comedies",
    "International TV Shows",
    "Documentaries",
]
GENRE_COLORS = {
    "International Movies": MOVIE,
    "Dramas": PURPLE,
    "Comedies": BLUE,
    "International TV Shows": GREEN,
    "Documentaries": TV,
}


def _font(weight: str = "regular", size: float = 11) -> fm.FontProperties:
    return fm.FontProperties(family="Inter", weight=weight, size=size)


def apply_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "Inter",
            "font.size": 11,
            "text.color": INK,
            "axes.labelcolor": MUTED,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.spines.left": False,
            "axes.spines.bottom": False,
            "axes.grid": False,
            "axes.axisbelow": True,
            "figure.facecolor": BG,
            "axes.facecolor": PANEL,
            "xtick.major.size": 0,
            "ytick.major.size": 0,
            "legend.frameon": False,
            "figure.dpi": 150,
            "savefig.dpi": 220,
            "savefig.facecolor": BG,
            "savefig.edgecolor": BG,
        }
    )


def canvas(
    title: str,
    subtitle: str,
    *,
    grain: str,
    figsize: tuple[float, float] = (12.4, 7.15),
    plot: tuple[float, float, float, float] = (0.10, 0.13, 0.86, 0.62),
    kicker: str = "NETFLIX CATALOG  ·  SUPPLY STUDY",
) -> tuple[plt.Figure, plt.Axes]:
    fig = plt.figure(figsize=figsize, facecolor=BG)
    fig.add_artist(
        plt.Line2D([0, 1], [1, 1], transform=fig.transFigure, color=ACCENT, lw=3.5, solid_capstyle="butt", clip_on=False)
    )
    fig.text(0.055, 0.945, kicker, color=ACCENT, fontproperties=_font("semibold", 8.2), va="top")
    fig.text(0.055, 0.905, title, color=INK, fontproperties=_font("semibold", 17.5), va="top")
    fig.text(0.055, 0.845, subtitle, color=MUTED, fontproperties=_font("regular", 10.2), va="top", linespacing=1.45)
    fig.text(
        0.055,
        0.035,
        f"{SOURCE_NOTE}\nGrain: {grain}",
        color=MUTED,
        fontproperties=_font("regular", 7.6),
        va="bottom",
        linespacing=1.45,
    )
    ax = fig.add_axes(list(plot))
    ax.set_facecolor(PANEL)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors=MUTED, labelsize=9)
    return fig, ax


def _grid_y(ax: plt.Axes) -> None:
    ax.yaxis.grid(True, color=FAINT, lw=0.7)
    ax.xaxis.grid(False)
    ax.set_axisbelow(True)


def _grid_x(ax: plt.Axes) -> None:
    ax.xaxis.grid(True, color=FAINT, lw=0.7)
    ax.yaxis.grid(False)
    ax.set_axisbelow(True)


def _save(fig: plt.Figure, name: str) -> Path:
    FIGURES.mkdir(parents=True, exist_ok=True)
    path = FIGURES / name
    fig.savefig(path, pad_inches=0.08)
    plt.close(fig)
    return path


def fig_additions(titles: pd.DataFrame) -> Path:
    counts = titles.dropna(subset=["year_added"]).groupby("year_added").size().astype(int)
    years = counts.index.astype(int)
    peak = int(counts.idxmax())
    fig, ax = canvas(
        "Catalog additions peaked in 2019 — 2021 is not a full year",
        "Titles by year they joined Netflix (date_added). 2021 stops on 25 September, so the last bar is not a collapse.",
        grain="one title",
    )
    _grid_y(ax)
    colors = [ACCENT if y == peak else (MOVIE_SOFT if y != 2021 else GRAY) for y in years]
    bars = ax.bar(years, counts.values, color=colors, width=0.78, zorder=3)
    for bar, value, year in zip(bars, counts.values, years):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 55,
            f"{value:,}",
            ha="center",
            va="bottom",
            color=INK if year == peak else MUTED,
            fontproperties=_font("medium" if year == peak else "regular", 8.5),
        )
    ax.set_ylabel("Titles added", color=MUTED)
    ax.set_xlim(years.min() - 0.7, years.max() + 0.7)
    ax.annotate(
        "Right-censored\nthrough 25 Sep",
        xy=(2021, counts.loc[2021]),
        xytext=(2013.4, counts.max() * 0.78),
        color=MUTED,
        fontproperties=_font("regular", 9),
        arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.8),
    )
    ax.set_ylim(0, counts.max() * 1.16)
    return _save(fig, "viz_01_catalog_additions.png")


def fig_missingness(titles: pd.DataFrame) -> Path:
    fields = [("director_unknown", "Director"), ("country_unknown", "Country"), ("cast_unknown", "Cast")]
    fig, ax = canvas(
        "Missing director is a TV-show schema, not a hole to fill",
        "Percent of titles with the field null. Keep NULL in analytic tables — a display string hides this pattern.",
        grain="one title",
        plot=(0.16, 0.14, 0.78, 0.60),
    )
    _grid_x(ax)
    y = np.arange(len(fields))
    height = 0.34
    for i, t in enumerate(["Movie", "TV Show"]):
        subset = titles[titles["type"] == t]
        values = [100 * subset[col].mean() for col, _ in fields]
        offset = -height / 2 if i == 0 else height / 2
        bars = ax.barh(y + offset, values, height=height, color=TYPE_COLORS[t], label=t, zorder=3)
        for bar, val in zip(bars, values):
            ax.text(
                val + 1.2,
                bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%",
                va="center",
                color=INK if val > 40 else MUTED,
                fontproperties=_font("medium", 9),
            )
    ax.set_yticks(y)
    ax.set_yticklabels([lab for _, lab in fields], fontproperties=_font("medium", 11), color=INK)
    ax.set_xlim(0, 108)
    ax.set_xlabel("Share of titles missing the field", color=MUTED)
    ax.legend(loc="lower right", prop=_font("medium", 10), labelcolor=INK)
    return _save(fig, "viz_02_missingness_by_type.png")


def fig_maturity(titles: pd.DataFrame) -> Path:
    rating = titles["rating"].fillna("Unknown")
    counts = rating.value_counts()
    order = [r for r in RATING_DISPLAY_ORDER if r in counts.index]
    values = [int(counts[r]) for r in order]
    band_for = {
        r: titles.loc[titles["rating"].fillna("Unknown").eq(r), "maturity_band"].iloc[0] if r != "Unknown" else "Unknown"
        for r in order
    }
    band_for["Unknown"] = "Unknown"
    colors = [BAND_COLORS.get(band_for[r], PURPLE) for r in order]
    family_n = int(titles["family_adjacent"].sum())
    tv_ma_14 = int(titles["rating"].isin(["TV-MA", "TV-14"]).sum())
    fig, ax = canvas(
        "The catalog is built for mature individual viewing",
        f"TV-MA + TV-14 = {tv_ma_14:,} titles ({tv_ma_14 / len(titles):.1%}). "
        f"Family-adjacent ratings = {family_n:,} ({family_n / len(titles):.1%}). Inventory mix, not audience preference.",
        grain="one title",
        figsize=(12.4, 7.35),
        plot=(0.10, 0.16, 0.86, 0.58),
    )
    _grid_y(ax)
    ax.bar(range(len(order)), values, color=colors, width=0.78, zorder=3)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(order, rotation=42, ha="right", fontproperties=_font("regular", 8.5))
    for i, val in enumerate(values):
        ax.text(i, val + 55, f"{val:,}", ha="center", color=INK if val > 1500 else MUTED, fontproperties=_font("medium", 7.8))
    handles = [plt.Rectangle((0, 0), 1, 1, color=BAND_COLORS[b], label=b) for b in ["Kids", "Teens", "Adults", "Unrated", "Unknown"]]
    ax.legend(handles=handles, loc="upper right", title="Maturity band", prop=_font("medium", 9), labelcolor=INK, title_fontsize=9)
    ax.set_ylabel("Titles", color=MUTED)
    ax.set_ylim(0, max(values) * 1.14)
    return _save(fig, "viz_03_maturity_mix.png")


def fig_countries(titles: pd.DataFrame, countries: pd.DataFrame) -> Path:
    unknown = int(titles["country_unknown"].sum())
    stacked = countries.groupby(["country_credit", "type"]).size().unstack(fill_value=0)
    for col in ("Movie", "TV Show"):
        if col not in stacked:
            stacked[col] = 0
    stacked["total"] = stacked["Movie"] + stacked["TV Show"]
    top = stacked.sort_values("total", ascending=True).tail(10)
    fig, ax = canvas(
        "Production credits are concentrated — Unknown is not a country",
        f"{unknown:,} titles ({unknown / len(titles):.1%}) have no production country and are excluded. "
        "Japan and South Korea are series-heavy; India is movie-heavy. Credits ≠ filming location ≠ viewership.",
        grain="one country-credit (exploded)",
        plot=(0.18, 0.14, 0.76, 0.60),
    )
    _grid_x(ax)
    y = np.arange(len(top))
    ax.barh(y, top["Movie"], color=TYPE_COLORS["Movie"], label="Movie", zorder=3)
    ax.barh(y, top["TV Show"], left=top["Movie"], color=TYPE_COLORS["TV Show"], label="TV Show", zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(top.index, fontproperties=_font("medium", 10.5), color=INK)
    for i, (_, row) in enumerate(top.iterrows()):
        ax.text(row["total"] + 40, i, f"{int(row['total']):,}", va="center", color=INK, fontproperties=_font("medium", 9))
    ax.set_xlabel("Production credits (a co-production counts once per country)", color=MUTED)
    ax.legend(loc="lower right", prop=_font("medium", 10), labelcolor=INK)
    ax.set_xlim(0, top["total"].max() * 1.16)
    return _save(fig, "viz_04_producing_countries.png")


def fig_genres(genres: pd.DataFrame) -> Path:
    counts = genres["genre"].value_counts().head(15).sort_values()
    fig, ax = canvas(
        "Genre is a tag cloud, not a partition of the catalog",
        "Top 15 listed_in tags. “International” is a platform taxonomy, not a film-studies genre. A title with 3 tags contributes 3.",
        grain="one genre-credit (exploded)",
        plot=(0.24, 0.13, 0.70, 0.62),
        figsize=(12.4, 7.5),
    )
    _grid_x(ax)
    y = np.arange(len(counts))
    highlight = set(HIGHLIGHT_GENRES)
    ax.hlines(y, 0, counts.values, color=FAINT, lw=1.4, zorder=2)
    for i, (name, val) in enumerate(counts.items()):
        color = GENRE_COLORS.get(name, MUTED)
        ax.plot(val, i, "o", color=color, ms=8.5, zorder=3)
        ax.text(val + 55, i, f"{int(val):,}", va="center", color=INK if name in highlight else MUTED, fontproperties=_font("medium", 9))
    ax.set_yticks(y)
    ax.set_yticklabels(counts.index, fontproperties=_font("medium", 10), color=INK)
    ax.set_xlabel("Tag incidences", color=MUTED)
    return _save(fig, "viz_05_genre_incidence.png")


def fig_rating_genre(genres: pd.DataFrame) -> Path:
    top_genres = genres["genre"].value_counts().head(12).index.tolist()
    rating_order = [r for r in RATING_DISPLAY_ORDER if r in set(genres["rating"].fillna("Unknown"))]
    sub = genres[genres["genre"].isin(top_genres)].copy()
    sub["rating"] = sub["rating"].fillna("Unknown")
    table = (
        sub.groupby(["genre", "rating"]).size().unstack(fill_value=0).reindex(index=top_genres, columns=rating_order, fill_value=0)
    )
    cmap = LinearSegmentedColormap.from_list("tableau_heat", ["#EFEBE8", "#F2C9C0", MOVIE, "#B33A3C"])
    fig, ax = canvas(
        "Rating × genre is a cross-tab of inventory — not a correlation",
        "Cell = (title, genre tag) pairs. A large cell is tagging policy, not “this audience prefers this genre.”",
        grain="one genre-credit (exploded)",
        figsize=(12.8, 7.6),
        plot=(0.20, 0.16, 0.70, 0.58),
    )
    im = ax.imshow(table.values, aspect="auto", cmap=cmap)
    ax.set_xticks(range(len(table.columns)))
    ax.set_xticklabels(table.columns, rotation=42, ha="right", fontproperties=_font("regular", 8))
    ax.set_yticks(range(len(table.index)))
    ax.set_yticklabels(table.index, fontproperties=_font("medium", 9.5), color=INK)
    vmax = table.values.max()
    for i in range(table.shape[0]):
        for j in range(table.shape[1]):
            val = int(table.values[i, j])
            if val == 0:
                continue
            color = WHITE if val > vmax * 0.45 else INK
            ax.text(j, i, f"{val:,}", ha="center", va="center", color=color, fontproperties=_font("medium", 6.6))
    cbar = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02)
    cbar.ax.yaxis.set_tick_params(color=MUTED)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=MUTED)
    cbar.set_label("Tag incidences", color=MUTED)
    return _save(fig, "viz_06_rating_genre_crosstab.png")


def fig_maturity_over_time(titles: pd.DataFrame) -> Path:
    sub = titles.dropna(subset=["year_added"]).copy()
    sub = sub[sub["year_added"] >= 2015]
    counts = sub.groupby(["year_added", "maturity_band"]).size().unstack(fill_value=0)
    for band in MATURITY_BAND_ORDER:
        if band not in counts:
            counts[band] = 0
    counts = counts[MATURITY_BAND_ORDER]
    fig, ax = canvas(
        "Mature titles dominate every add-year of the expansion era",
        "Stacked counts by year_added, 2015–2021. 2021 is truncated. Band is a recode of rating, not viewers.",
        grain="one title",
    )
    _grid_y(ax)
    years = counts.index.astype(int)
    bottom = np.zeros(len(counts))
    for band in MATURITY_BAND_ORDER:
        vals = counts[band].to_numpy(dtype=float)
        ax.bar(years, vals, bottom=bottom, color=BAND_COLORS[band], label=band, width=0.78, zorder=3)
        bottom += vals
    ax.legend(loc="upper left", ncol=5, prop=_font("medium", 9), labelcolor=INK)
    ax.set_ylabel("Titles added", color=MUTED)
    return _save(fig, "viz_07_maturity_over_add_year.png")


def fig_release_year(titles: pd.DataFrame) -> Path:
    """Tableau counterpart: Content by years (library age, not add policy)."""
    sub = titles[titles["release_year"] >= 1980].copy()
    pivot = sub.groupby(["release_year", "type"]).size().unstack(fill_value=0)
    for col in ("Movie", "TV Show"):
        if col not in pivot:
            pivot[col] = 0
    fig, ax = canvas(
        "The library is contemporary — this is what Netflix chose to carry",
        "Titles by original release_year (1980–2021), stacked Movie / TV Show. Not global cinema output. 2021 is incomplete.",
        grain="one title",
        kicker="TABLEAU VIEW  ·  CONTENT BY YEARS",
    )
    _grid_y(ax)
    years = pivot.index.astype(int)
    ax.stackplot(
        years,
        pivot["Movie"],
        pivot["TV Show"],
        colors=[MOVIE, TV],
        labels=["Movie", "TV Show"],
        alpha=0.92,
        lw=0,
    )
    ax.legend(loc="upper left", prop=_font("medium", 10), labelcolor=INK)
    ax.set_ylabel("Titles in the catalog", color=MUTED)
    ax.set_xlim(1980, 2021)
    return _save(fig, "viz_09_library_by_release_year.png")


def fig_genre_trends(titles: pd.DataFrame, genres: pd.DataFrame) -> Path:
    """Tableau counterpart: Trend in publishing genres over years — without spaghetti."""
    g = genres.dropna(subset=["year_added"]).copy()
    g = g[(g["year_added"] >= 2014) & (g["year_added"] <= 2021)]
    yearly = g.groupby(["year_added", "genre"]).size().unstack(fill_value=0)
    fig, ax = canvas(
        "A few tags carry the expansion — the rest are a long tail",
        "Genre-tag incidences by year_added. Top five tags in color; every other tag is drawn in muted gray so the spaghetti can be read.",
        grain="one genre-credit (exploded)",
        kicker="TABLEAU VIEW  ·  TREND IN PUBLISHING GENRES",
        figsize=(12.4, 7.35),
    )
    _grid_y(ax)
    others = [c for c in yearly.columns if c not in HIGHLIGHT_GENRES]
    for col in others:
        ax.plot(yearly.index, yearly[col], color="#D5D0C8", lw=1.05, zorder=2)
    for name in HIGHLIGHT_GENRES:
        if name not in yearly:
            continue
        ax.plot(yearly.index, yearly[name], color=GENRE_COLORS[name], lw=2.6, zorder=4, label=name)
        ax.scatter(yearly.index, yearly[name], color=GENRE_COLORS[name], s=18, zorder=5)
    ax.legend(loc="upper left", ncol=1, prop=_font("medium", 9), labelcolor=INK)
    ax.set_ylabel("Tag incidences added", color=MUTED)
    ax.set_xlim(2014, 2021)
    return _save(fig, "viz_10_genre_trends.png")


def fig_rating_years(titles: pd.DataFrame) -> Path:
    """Tableau counterpart: Number of rating's content years."""
    sub = titles[titles["release_year"] >= 2000].copy()
    pivot = sub.groupby(["release_year", "maturity_band"]).size().unstack(fill_value=0)
    for band in MATURITY_BAND_ORDER:
        if band not in pivot:
            pivot[band] = 0
    pivot = pivot[MATURITY_BAND_ORDER]
    fig, ax = canvas(
        "Mature ratings thicken as the library becomes contemporary",
        "Stacked titles by original release_year and maturity band, 2000–2021. Family-adjacent inventory stays a thin band.",
        grain="one title",
        kicker="TABLEAU VIEW  ·  RATINGS OVER RELEASE YEARS",
    )
    _grid_y(ax)
    ax.stackplot(
        pivot.index.astype(int),
        *[pivot[b] for b in MATURITY_BAND_ORDER],
        colors=[BAND_COLORS[b] for b in MATURITY_BAND_ORDER],
        labels=MATURITY_BAND_ORDER,
        lw=0,
        alpha=0.95,
    )
    ax.legend(loc="upper left", ncol=5, prop=_font("medium", 8.5), labelcolor=INK)
    ax.set_ylabel("Titles", color=MUTED)
    ax.set_xlim(2000, 2021)
    return _save(fig, "viz_11_rating_over_release_year.png")


def fig_cast(titles: pd.DataFrame, genres: pd.DataFrame) -> Path:
    """Tableau counterpart: Distribution of cast with different listed_in."""
    merged = genres.merge(titles.loc[:, ["show_id", "n_cast"]], on="show_id", how="left")
    totals = merged.groupby("genre")["n_cast"].sum().sort_values().tail(12)
    fig, ax = canvas(
        "Ensemble tags accumulate more names — that is format, not star power",
        "Sum of parsed cast-list length by genre tag. Missing cast (825 titles) is excluded from the name count. Not a bankability ranking.",
        grain="one (genre tag × cast name-token)",
        kicker="TABLEAU VIEW  ·  CAST × LISTED IN",
        plot=(0.26, 0.13, 0.68, 0.62),
        figsize=(12.4, 7.45),
    )
    _grid_x(ax)
    y = np.arange(len(totals))
    colors = [GENRE_COLORS.get(name, GRAY) for name in totals.index]
    ax.barh(y, totals.values, color=colors, height=0.72, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(totals.index, fontproperties=_font("medium", 10), color=INK)
    for i, val in enumerate(totals.values):
        ax.text(val + 80, i, f"{int(val):,}", va="center", color=INK, fontproperties=_font("medium", 9))
    ax.set_xlabel("Cast name-tokens (sum of list lengths)", color=MUTED)
    ax.set_xlim(0, totals.max() * 1.14)
    return _save(fig, "viz_12_cast_by_genre.png")


def fig_briefing(titles: pd.DataFrame, countries: pd.DataFrame) -> Path:
    fig = plt.figure(figsize=(13.2, 8.55), facecolor=BG)
    fig.add_artist(
        plt.Line2D([0, 1], [1, 1], transform=fig.transFigure, color=ACCENT, lw=3.5, solid_capstyle="butt", clip_on=False)
    )
    fig.text(0.045, 0.955, "NETFLIX CATALOG  ·  BRIEFING BOARD", color=ACCENT, fontproperties=_font("semibold", 8.2), va="top")
    fig.text(0.045, 0.915, "Four facts a content meeting can use — and the limits of this file", color=INK, fontproperties=_font("semibold", 18), va="top")
    fig.text(
        0.045,
        0.868,
        "N = 8,807 titles   ·   last date_added = 2021-09-25   ·   no watch-time, cost, or subscribers in this extract",
        color=MUTED,
        fontproperties=_font("regular", 10),
        va="top",
    )
    gs = fig.add_gridspec(2, 2, left=0.07, right=0.97, top=0.82, bottom=0.08, hspace=0.38, wspace=0.22)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(PANEL)
    counts = titles.dropna(subset=["year_added"]).groupby("year_added").size()
    years = counts.index.astype(int)
    colors = [ACCENT if y == 2019 else MOVIE_SOFT for y in years]
    colors = [GRAY if y == 2021 else c for y, c in zip(years, colors)]
    ax1.bar(years, counts.values, color=colors, width=0.82, zorder=3)
    ax1.set_title("Additions peak in 2019", loc="left", color=INK, fontproperties=_font("semibold", 12.5), pad=8)
    ax1.yaxis.grid(True, color=FAINT, lw=0.6)
    ax1.set_axisbelow(True)
    for spine in ax1.spines.values():
        spine.set_visible(False)
    ax1.tick_params(colors=MUTED, labelsize=8)

    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(PANEL)
    share = titles["maturity_band"].value_counts().reindex(MATURITY_BAND_ORDER).fillna(0)
    ax2.barh(share.index[::-1], share.values[::-1], color=[BAND_COLORS[b] for b in share.index[::-1]], zorder=3)
    ax2.set_title("Adults + Teens are the catalog", loc="left", color=INK, fontproperties=_font("semibold", 12.5), pad=8)
    ax2.xaxis.grid(True, color=FAINT, lw=0.6)
    ax2.set_axisbelow(True)
    for i, val in enumerate(share.values[::-1]):
        ax2.text(val + 50, i, f"{int(val):,}", va="center", color=INK, fontproperties=_font("medium", 9))
    for spine in ax2.spines.values():
        spine.set_visible(False)
    ax2.tick_params(colors=MUTED, labelsize=9)

    ax3 = fig.add_subplot(gs[1, 0])
    ax3.set_facecolor(PANEL)
    miss = pd.Series(
        {
            "Director · TV Show": titles.loc[titles["type"] == "TV Show", "director_unknown"].mean() * 100,
            "Director · Movie": titles.loc[titles["type"] == "Movie", "director_unknown"].mean() * 100,
            "Country": titles["country_unknown"].mean() * 100,
            "Cast": titles["cast_unknown"].mean() * 100,
        }
    )
    ax3.barh(miss.index[::-1], miss.values[::-1], color=BLUE, zorder=3)
    ax3.set_title("Missingness is structured", loc="left", color=INK, fontproperties=_font("semibold", 12.5), pad=8)
    ax3.xaxis.grid(True, color=FAINT, lw=0.6)
    ax3.set_axisbelow(True)
    ax3.set_xlabel("% missing", color=MUTED)
    for spine in ax3.spines.values():
        spine.set_visible(False)
    ax3.tick_params(colors=MUTED, labelsize=8)

    ax4 = fig.add_subplot(gs[1, 1])
    ax4.set_facecolor(PANEL)
    top = countries["country_credit"].value_counts().head(8).sort_values()
    ax4.barh(top.index, top.values, color=MOVIE, zorder=3)
    ax4.set_title("U.S. still anchors production credits", loc="left", color=INK, fontproperties=_font("semibold", 12.5), pad=8)
    ax4.xaxis.grid(True, color=FAINT, lw=0.6)
    ax4.set_axisbelow(True)
    ax4.set_xlabel("Credits (Unknown excluded)", color=MUTED)
    for spine in ax4.spines.values():
        spine.set_visible(False)
    ax4.tick_params(colors=MUTED, labelsize=8)

    fig.text(0.045, 0.025, SOURCE_NOTE, color=MUTED, fontproperties=_font("regular", 7.6))
    return _save(fig, "viz_08_briefing_board.png")


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
        fig_release_year(titles),
        fig_genre_trends(titles, genres),
        fig_rating_years(titles),
        fig_cast(titles, genres),
    ]
