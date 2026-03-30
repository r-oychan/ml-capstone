"""
Propose next points for a submission round.

Usage:
    uv run python src/propose_round.py [--round N]

If --round is omitted, auto-detects the next round from existing data.

Strategy is configured per-function in the STRATEGIES dict below.
Adjust xi, radius, and candidate counts between rounds based on observations.
"""

import argparse
import sys
import numpy as np

sys.path.insert(0, "src")
from bo_utils import (
    FUNCTIONS, INPUT_MIN, INPUT_MAX,
    load_all_data, fit_gp_model, expected_improvement,
    sample_random_points, propose_next_point, get_completed_rounds,
    format_submission, print_status_report,
)


# ── Per-function strategy ─────────────────────────────────────────────────
#
# xi:       exploration parameter for Expected Improvement
#             low (0.001) = exploit known good regions
#             medium (0.01) = balanced (default)
#             high (0.05) = explore uncertain regions
#
# radius:   size of local search neighborhood around current best point
#             smaller = tighter exploitation, larger = wider local search
#
# n_local:  number of candidate points sampled near the best known point
# n_broad:  number of candidate points sampled across the full [0, 1) domain
#
# Together, n_local + n_broad = total candidates evaluated by EI.
# More candidates = better coverage but slower. Use more for high-D functions.

STRATEGIES = {
    # R7: Exploration round — broad search across all functions to gather GP data.
    # F1: Full-domain exploration. 5 rounds of local search failed.
    1: {"xi": 0.05, "radius": None, "n_local": 0,      "n_broad": 200_000},
    # F2: Full-domain exploration. Never beaten initial best.
    2: {"xi": 0.05, "radius": None, "n_local": 0,      "n_broad": 200_000},
    # F3: Full-domain exploration. Stuck at R1 best.
    3: {"xi": 0.05, "radius": None, "n_local": 0,      "n_broad": 200_000},
    # F4: Mostly explore, keep some local near R4 best.
    4: {"xi": 0.05, "radius": 0.15, "n_local": 50_000, "n_broad": 150_000},
    # F5: Reliable improver. Explore broadly but keep some local context.
    5: {"xi": 0.05, "radius": 0.10, "n_local": 50_000, "n_broad": 150_000},
    # F6: Full-domain exploration. 5 rounds stuck.
    6: {"xi": 0.05, "radius": None, "n_local": 0,      "n_broad": 200_000},
    # F7: Reliable improver. Explore broadly but keep some local context.
    7: {"xi": 0.05, "radius": 0.10, "n_local": 50_000, "n_broad": 150_000},
    # F8: Full-domain exploration. 8D needs massive sampling.
    8: {"xi": 0.05, "radius": None, "n_local": 0,      "n_broad": 300_000},
}


def propose_for_function(func_num, round_num):
    """Propose next point for a single function using its strategy."""
    strat = STRATEGIES[func_num]
    dim = FUNCTIONS[func_num]["dim"]
    xi = strat["xi"]
    radius = strat["radius"]
    n_local = strat["n_local"]
    n_broad = strat["n_broad"]

    X, y = load_all_data(func_num)

    # If only broad candidates (no local search), use the simple propose function
    # Seed must include func_num so different functions get different candidate pools
    seed = round_num * 100 + func_num
    if n_local == 0:
        bounds = np.array([[INPUT_MIN, INPUT_MAX]] * dim)
        x_next, ei_val, gp = propose_next_point(
            X, y, bounds, n_candidates=n_broad, xi=xi, random_state=seed
        )
        return x_next, ei_val

    # Otherwise: mix local + broad candidates
    gp = fit_gp_model(X, y, random_state=round_num)
    y_best = y.max()
    best_pt = X[np.argmax(y)]

    rng = np.random.default_rng(seed=round_num * 100 + func_num)
    candidates_parts = []

    # Local candidates: uniform in [best - radius, best + radius]
    if n_local > 0 and radius is not None:
        local = best_pt + rng.uniform(-radius, radius, size=(n_local, dim))
        local = np.clip(local, INPUT_MIN, INPUT_MAX)
        candidates_parts.append(local)

    # Broad candidates: uniform across full domain
    if n_broad > 0:
        bounds = np.array([[INPUT_MIN, INPUT_MAX]] * dim)
        broad = sample_random_points(bounds, n_broad, random_state=round_num * 10 + func_num)
        candidates_parts.append(broad)

    candidates = np.vstack(candidates_parts)
    ei = expected_improvement(candidates, gp, y_best, xi=xi)
    best_idx = np.argmax(ei)
    x_next = np.clip(candidates[best_idx], INPUT_MIN, INPUT_MAX)

    return x_next, ei[best_idx]


def main():
    parser = argparse.ArgumentParser(description="Propose next points for a BO round")
    parser.add_argument("--round", type=int, default=None,
                        help="Round number (auto-detects next round if omitted)")
    args = parser.parse_args()

    round_num = args.round or (get_completed_rounds() + 1)

    np.set_printoptions(precision=6, suppress=True)
    print_status_report()
    print(f"\nProposing points for Round {round_num}...")
    print("=" * 70)

    proposals = {}
    for fn in range(1, 9):
        strat = STRATEGIES[fn]
        x_next, ei_val = propose_for_function(fn, round_num)
        proposals[fn] = x_next

        strat_desc = f"xi={strat['xi']}"
        if strat["n_local"] > 0:
            strat_desc += f", {strat['n_local']//1000}k local ±{strat['radius']}"
        if strat["n_broad"] > 0:
            strat_desc += f", {strat['n_broad']//1000}k broad"

        print(f"F{fn}: EI={ei_val:.4e}  point={x_next}")
        print(f"     [{strat_desc}]")

    # Portal-ready submission strings
    print("\n" + "=" * 70)
    print("PORTAL SUBMISSIONS")
    print("=" * 70)
    for fn in range(1, 9):
        print(f"Function {fn}: {format_submission(proposals[fn])}")

    # inputs.txt format for saving
    print("\n" + "=" * 70)
    print("inputs.txt (copy to data/submissions/round_{:02d}/inputs.txt)".format(round_num))
    print("=" * 70)
    parts = []
    for fn in range(1, 9):
        parts.append(f"array({np.array2string(proposals[fn], separator=', ')})")
    print("[" + ", ".join(parts) + "]")


if __name__ == "__main__":
    main()
