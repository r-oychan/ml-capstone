# Capstone 1 - Black-Box Bayesian Optimization Competition

## Project Overview

Maximize 8 unknown black-box functions using Bayesian Optimization with **13 total submission attempts**. Each attempt submits one query point per function and receives the output. We cannot see the function formulas — only query and observe.

**Final deliverable:** Public GitHub repository submitted via discussion board in Module 25. Must be a portfolio-quality artefact presenting the project from start to finish.

## Current State

- **Attempts used:** 6 of 13
- **Attempts remaining:** 7
- See `results/tracking.md` for per-function best values and round-by-round history.

## Project Structure

```
capstone1/
├── CLAUDE.md              # This file — project instructions
├── README.md              # ~100-word non-technical summary + project overview
├── question.md            # Problem description (8 functions)
├── pyproject.toml         # Dependencies
├── data/
│   ├── initial/           # Starter .npy files (function_1/ ... function_8/)
│   └── submissions/       # One folder per round
│       └── round_NN/
│           ├── inputs.txt   # What we submitted (8 arrays, one per function)
│           └── outputs.txt  # What we got back (8 values)
├── notebooks/
│   ├── 01_exploration.ipynb    # Initial data analysis & visualization
│   ├── 02_framework.ipynb      # BO framework development
│   └── 03_optimization.ipynb   # Main iterative loop (primary working notebook)
├── src/
│   ├── bo_utils.py        # Shared utilities (GP, EI, data loading)
│   └── propose_round.py   # Per-round proposal script (configurable strategy)
├── results/
│   └── tracking.md        # Round-by-round results and observations
└── docs/
    ├── datasheet.md       # Data description, limitations, context
    └── model_card.md      # Model behaviour, assumptions, limitations
```

## Required Deliverables (from FAQ)

1. **README.md** — ~100-word non-technical summary of purpose, process, and results
2. **Datasheet** (`docs/datasheet.md`) — describes data used, limitations, and context
3. **Model Card** (`docs/model_card.md`) — model behaviour, assumptions, limitations, interpretability
4. **Jupyter Notebooks** — well-documented, clear, reproducible code for all 8 functions
5. **Visualizations** — convergence plots, acquisition function evolution, surrogate model evolution per function
6. **Summary of findings** — best input/output per function, why BO was chosen, challenges & key insights (can be in notebook or README)

## Submission Format (CRITICAL)

Portal submission format: `x1-x2-x3-...-xn`

**Rules:**
- Each value **must start with 0** (i.e., in range [0.000000, 0.999999])
- Each value must have **exactly 6 decimal places**
- Values separated by **hyphens, no spaces**
- Example: `0.498317-0.625531` (correct) vs `0.498317 - 0.625531` (WRONG)

Use `format_submission(point)` from `src/bo_utils.py` to generate the correct format.

## Functions Summary

| Func | Dim | Initial Samples | Description                        |
|------|-----|-----------------|------------------------------------|
| F1   | 2D  | 10              | Radiation source (very peaked)     |
| F2   | 2D  | 10              | ML log-likelihood (noisy, multimodal) |
| F3   | 3D  | 15              | Drug discovery (side effects)      |
| F4   | 4D  | 30              | Warehouse placement (local optima) |
| F5   | 4D  | 20              | Chemical yield (unimodal)          |
| F6   | 5D  | 20              | Cake recipe (negative scores→0)    |
| F7   | 6D  | 30              | ML hyperparameter tuning           |
| F8   | 8D  | 40              | Complex 8D black-box               |

## Workflow — Each Submission Round

1. **Adjust strategy** (if needed): Edit `STRATEGIES` dict in `src/propose_round.py` — tune xi, radius, candidate counts per function
2. **Generate proposals**: `uv run python src/propose_round.py --round N` — outputs portal-ready strings and inputs.txt content
3. **Review**: Check EI values — low EI means the model doesn't expect improvement. Consider adjusting strategy.
4. **Submit**: Copy portal-ready strings into submission portal. Values must be [0, 0.999999], 6 decimals, hyphen-separated.
5. **Save inputs**: Script auto-saves to `data/submissions/round_NN/inputs.txt` (or copy from output)
6. **Record outputs**: After portal returns results, save to `data/submissions/round_NN/outputs.txt`
7. **Update tracking**: Update `results/tracking.md` with new results
8. **Analyze**: Check which functions improved, which regressed, and adjust STRATEGIES for next round
9. **Document strategy**: Update the "Strategy Log" section below with the rationale for any parameter changes

### Key Parameters in `src/propose_round.py`

- **xi** — exploration parameter for Expected Improvement acquisition function
  - Low (0.001) = exploit: prefer points GP predicts will be good
  - Medium (0.01) = balanced (default)
  - High (0.05) = explore: prefer points where GP is uncertain
- **radius** — local search neighborhood around current best point (e.g. 0.08 = ±8% of domain)
- **n_local** — candidate points sampled near the best known point (exploitation)
- **n_broad** — candidate points sampled across full [0, 1) domain (exploration)
- **random_state** — derived from round number to avoid proposing duplicate points across rounds

### Data Format

**inputs.txt** — Python list of 8 arrays (one per function):
```
[array([0.636961, 0.269786]), array([0.775367, 0.935228]), ..., array([0.024602, ...])]
```

**outputs.txt** — Python list of 8 float values:
```
[np.float64(-3.76e-49), np.float64(0.150), ..., np.float64(9.905)]
```

## Strategy Overview

### Phased approach

**Phase 1 — Rounds 4–6: Diagnose & diversify**
- Per-function xi tuning, increased candidate counts (50k+), targeted local/broad mix

**Phase 2 — Rounds 7–9: Targeted exploitation**
- Exploit improving functions, local search around best-known points, try UCB for stuck functions

**Phase 3 — Rounds 10–13: Final polish**
- Pure exploitation, multi-start local search around top-N best points, GP ensemble

## Strategy Log

Each round records: what we observed, why we changed strategy, and the exact parameters used.

### Rounds 1–3 (Baseline) — One-size-fits-all

**Rationale:** First submissions. Used default `propose_next_point()` from `bo_utils.py` with uniform settings across all 8 functions. No per-function tuning.

| Parameter     | Value  | Notes                                       |
|---------------|--------|---------------------------------------------|
| xi            | 0.01   | Balanced exploration/exploitation (default)  |
| n_candidates  | 10,000 | Full-domain random sampling only             |
| radius        | —      | No local search — all broad                 |
| random_state  | 0      | Same seed each round (caused near-duplicate proposals in R2/R3) |

**Result (R1):** 4 new bests (F3, F4, F5, F6, F8). Good first round — broad search found improvements for most functions.
**Result (R2):** 2 new bests (F5, F7). Diminishing returns. F1/F2 still stuck at initial best. Same random_state caused similar proposals.
**Result (R3):** 1 new best (F5 only). Near-identical proposals to R2 for F1, F3, F5, F6 due to fixed random_state. Clear signal that uniform strategy was exhausted.

**Lessons learned:**
- 10k candidates is too few — EI landscape undersampled especially for higher-D functions
- Same random_state across rounds → duplicate proposals. Must vary per round.
- F1 needs precision local search, not broad random. F3/F4/F6 need exploitation, not balanced xi.
- F5 is the only function consistently responding to standard BO.

### Round 4 (Phase 1) — First per-function tuning

**Rationale:** Rounds 1–3 used a one-size-fits-all approach. F5 improved consistently but F1/F2 never beat initial best, and F3/F4/F6 peaked in round 1 then regressed. Switched to per-function xi and local/broad mix.

| Func | xi    | radius | n_local | n_broad | Why                                                    |
|------|-------|--------|---------|---------|--------------------------------------------------------|
| F1   | 0.001 | 0.05   | 100k    | 0       | Extremely peaked — dense local search near [0.731, 0.733] |
| F2   | 0.01  | 0.10   | 50k     | 50k     | Noisy/multimodal — balanced local + broad              |
| F3   | 0.001 | 0.08   | 50k     | 50k     | Exploit near R1 best [0.362, 0.330, 0.464]             |
| F4   | 0.001 | 0.08   | 50k     | 50k     | Exploit near R1 best [0.407, 0.414, 0.378, 0.455]      |
| F5   | 0.01  | —      | 0       | 100k    | Consistently improving — standard broad EI             |
| F6   | 0.001 | 0.08   | 50k     | 50k     | Exploit near R1 best [0.437, 0.384, 0.555, 0.797, 0.137] |
| F7   | 0.01  | 0.15   | 50k     | 100k    | 6D needs wider search                                  |
| F8   | 0.01  | 0.15   | 100k    | 200k    | 8D needs massive candidate pool                        |

**Result:** Best round yet — 3 new bests (F4, F5, F7). Per-function tuning validated.

### Round 5 (Phase 1) — React to R4 breakthroughs

**Rationale:** R4 showed F4/F5/F7 responded to exploitation while F3/F6 stayed stuck. Tighten search for winners, broaden search for losers.

| Func | xi    | radius | n_local | n_broad | Why                                                    |
|------|-------|--------|---------|---------|--------------------------------------------------------|
| F1   | 0.001 | 0.005  | 200k    | 0       | R4 got 7.66e-16 vs initial 7.71e-16 — within 0.001 of peak, need ultra-precision |
| F2   | 0.001 | 0.05   | 80k     | 20k     | R4 explored [0.656, 1.0] → 0.557, wrong direction. Refocus near initial best [0.703, 0.927] |
| F3   | 0.02  | 0.10   | 30k     | 70k     | Exploitation failed 3 rounds (-0.009 never beaten). Switch to broader exploration |
| F4   | 0.001 | 0.05   | 80k     | 20k     | Breakthrough to +0.327 at [0.395, 0.438, 0.401, 0.420] — exploit this region |
| F5   | 0.001 | 0.08   | 80k     | 20k     | Massive jump to 4121, dims 2-4 near 1.0. Switch from broad-only to local search around new best |
| F6   | 0.02  | 0.12   | 30k     | 70k     | Same as F3 — exploitation stalled since R1, try broader exploration with higher xi |
| F7   | 0.001 | 0.08   | 80k     | 20k     | New best at [0.010, 0.388, 0.184, 0.150, 0.336, 0.763] — exploit near it |
| F8   | 0.001 | 0.10   | 150k    | 150k    | Best still R1. Switch to exploitation with tighter radius and lower xi |

**Result:** 2 new bests (F5, F7). F5 jumped to 5232 (dims 2-4 maxed, dim 1 trending up). F7 to 1.651. F1/F2/F3/F4/F6/F8 did not improve.

### Round 6 (Phase 2) — Targeted exploitation, tighter radii

**Rationale:** Phase 2 begins. F5/F7 are our reliable improvers — keep exploiting. F1 gave up on precision after 5 failed rounds — switching to full-domain exploration to gather GP data. F2/F4 have narrow peaks that R5 missed — use ultra-tight radii. F3/F6 are the hardest — back to exploitation for F3, balanced for F6. F8 needs tighter focus on R1 best.

| Func | xi    | radius | n_local | n_broad | Why                                                    |
|------|-------|--------|---------|---------|--------------------------------------------------------|
| F1   | 0.1   | —      | 0       | 200k    | 5 rounds stuck, EI=0. Full-domain exploration to gather GP info, maybe find a second peak |
| F2   | 0.001 | 0.03   | 150k    | 0       | R5 at [0.667, 0.914] too far. Ultra-tight near initial best [0.703, 0.927] |
| F3   | 0.001 | 0.05   | 80k     | 20k     | Broader exploration failed in R5. Return to tight exploitation near R1 best |
| F4   | 0.001 | 0.03   | 150k    | 0       | R4 best (+0.327) at very specific point. Ultra-tight radius to find the narrow peak |
| F5   | 0.001 | 0.05   | 80k     | 20k     | Dims 2-4 maxed. Focus on optimizing dim 1 (trending up: 0.596→0.676) |
| F6   | 0.01  | 0.08   | 50k     | 50k     | Neither exploitation nor exploration working. Balanced search, moderate xi |
| F7   | 0.001 | 0.05   | 100k    | 0       | Steady climber. Tight exploitation around R5 best [0.0, 0.319, 0.161, 0.185, 0.336, 0.804] |
| F8   | 0.001 | 0.08   | 200k    | 100k    | Best still R1. Tighter radius, heavy local search around [0.025, 0.258, 0.057, 0.319, 0.819, 0.337, 0.182, 0.547] |

**Result:** Submitted but portal did not return results. Skipping to round 7.

### Round 7 (Phase 2) — Exploration rebalance

**Rationale:** After 5 rounds of mostly exploitation, only F5/F7 are improving. F1/F2/F3/F4/F6/F8 may be stuck in local optima. Dedicating one round to broad exploration across all functions to gather GP data from new regions. This gives the GP new information to work with in later exploitation rounds.

| Func | xi    | radius | n_local | n_broad | Why                                                    |
|------|-------|--------|---------|---------|--------------------------------------------------------|
| F1   | 0.05  | —      | 0       | 200k    | 5 rounds of local search failed. Full-domain exploration to find alternative peaks |
| F2   | 0.05  | —      | 0       | 200k    | Never beaten initial best. Let GP discover new promising regions |
| F3   | 0.05  | —      | 0       | 200k    | Stuck at R1 best. Broad exploration to escape local optimum |
| F4   | 0.05  | 0.15   | 50k     | 150k    | Keep some local near R4 best but mostly explore new territory |
| F5   | 0.05  | 0.10   | 50k     | 150k    | Reliable improver — still explore broadly but don't abandon the trend |
| F6   | 0.05  | —      | 0       | 200k    | 5 rounds stuck. Full reset — gather data everywhere |
| F7   | 0.05  | 0.10   | 50k     | 150k    | Reliable improver — explore broadly but keep some local context |
| F8   | 0.05  | —      | 0       | 300k    | 8D needs massive sampling. Full-domain with high xi |

**Result:** *(pending — submit and record in tracking.md)*

## Technical Notes

- **Input range**: All values must be in **[0.000000, 0.999999]** — strictly less than 1
- **GP kernel**: `ConstantKernel * Matern(nu=2.5) + WhiteKernel` — good default but consider per-function tuning
- **Bounds**: Should be [0, 0.999999] for all dimensions (confirmed by FAQ)
- **Random state**: Use different random_state values across rounds to avoid proposing duplicate points
- Deep learning is not suitable here — too little data, too few dimensions
- Submissions processed at end of each module; late submissions within 24-48 hours

## Presentation & Code Quality Guidelines (from FAQ)

- Code in **Jupyter Notebooks**, well-documented, clear, reproducible, easy to follow
- **Visualize**: convergence/best-value-over-time plots, acquisition function landscape, GP surrogate surface (for 2D functions)
- **Document reasoning**: explain strategy choices, why BO, exploration vs exploitation tradeoffs
- Start with Function 1 (2D) to show workflow, then gradually move to higher dimensions
- Large datasets should NOT be stored on GitHub — link to external source in README

## Dependencies

```
numpy, scikit-learn, scipy, matplotlib
```

Run with: `uv run jupyter notebook` or use VSCode notebook support.
