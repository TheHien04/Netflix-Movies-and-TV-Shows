"""Build processed tables, quality report, and publication figures."""

from __future__ import annotations

from .clean import build
from .quality import write_quality_report
from .viz import render_all


def main() -> None:
    tables = build()
    report = write_quality_report(tables["titles"], tables["genres"], tables["countries"])
    paths = render_all(tables["titles"], tables["genres"], tables["countries"])
    print(f"titles={len(tables['titles']):,}")
    print(f"quality_report={report}")
    for path in paths:
        print(f"figure={path}")


if __name__ == "__main__":
    main()
