from __future__ import annotations

import argparse
from typing import Any

from app.main import analyze_single_bracket
from app.models.judo import BracketInput
from app.services.normalization import normalize_weight
from scripts.build_tournament_request import build


def run_analysis(top: int = 20, only_positive: bool = False, weight: str | None = None) -> dict[str, Any]:
    payload = build()
    competition_name = payload["competition_name"]
    weights_in = payload["weights"]

    if weight is not None:
        weights_in = [w for w in weights_in if normalize_weight(w["weight"]) == normalize_weight(weight)]

    results_by_weight = {}
    global_picks = []

    for w in weights_in:
        result = analyze_single_bracket(BracketInput(competition_name=competition_name, **w))
        results_by_weight[w["weight"]] = result
        global_picks.extend(result.recommended_picks)

    if only_positive:
        global_picks = [p for p in global_picks if p.edge > 0]

    global_picks = sorted(global_picks, key=lambda p: p.edge, reverse=True)
    return {
        "competition_name": competition_name,
        "num_weights": len(results_by_weight),
        "weights": results_by_weight,
        "global_top_picks": global_picks[:top],
    }


def print_report(report: dict[str, Any], top: int, only_positive: bool) -> None:
    print(f"Competition: {report['competition_name']}")
    print(f"Weights analyzed: {report['num_weights']}")
    print(f"Global recommended picks (top {top}, only_positive={only_positive}):")
    for p in report["global_top_picks"]:
        print(f"  - [{p.weight} {p.gender}] {p.market} {p.athlete}: edge={p.edge:.4f}, odds={p.odds}")

    for weight, result in report["weights"].items():
        print(f"\n=== {weight} ===")
        print("Top 5 Winner ranking:")
        for row in result.winner_ranking[:5]:
            print(f"  - {row['athlete']}: {row['prob']:.4f}")
        print("Top 5 Top4 ranking:")
        for row in result.top4_ranking[:5]:
            print(f"  - {row['athlete']}: {row['prob']:.4f}")

        pos_picks = [p for p in result.recommended_picks if p.edge > 0]
        print("Positive value picks:")
        for p in pos_picks[:10]:
            print(f"  - {p.market} {p.athlete}: edge={p.edge:.4f} odds={p.odds}")

        if result.warnings:
            print(f"Warnings ({len(result.warnings)}): {result.warnings[:3]}{' ...' if len(result.warnings) > 3 else ''}")
        else:
            print("Warnings: none")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze Qazaqstan Barysy Grand Slam 2026 locally")
    parser.add_argument("--top", type=int, default=20, help="Number of global picks to display")
    parser.add_argument("--only-positive", action="store_true", help="Show only picks with edge > 0")
    parser.add_argument("--weight", type=str, default=None, help='Analyze only one weight, e.g. "-60 kg"')
    args = parser.parse_args()

    report = run_analysis(top=args.top, only_positive=args.only_positive, weight=args.weight)
    print_report(report, top=args.top, only_positive=args.only_positive)


if __name__ == "__main__":
    main()
