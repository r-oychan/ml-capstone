# Capstone Project - Black-Box Bayesian Optimization

## Summary

This project tackles eight unknown "black-box" functions using Bayesian optimization — a technique for finding optimal solutions when each evaluation is expensive and the underlying formula is hidden. Using Gaussian Process regression as a surrogate model and Expected Improvement as the acquisition function, we iteratively propose and evaluate input combinations to maximize each function's output. With only 13 submission attempts, the strategy balances exploring new regions of the input space against exploiting known promising areas. The approach mirrors real-world challenges like drug formulation, manufacturing tuning, and ML hyperparameter optimization where testing is costly and data is scarce.

## Project Overview

Black-Box Optimization (BBO) challenge: find the global maximum of 8 unknown functions where we cannot see the formula or gradients — only query specific points and observe noisy outputs. We have **13 total submission attempts**, making every query count.

**Real-world relevance:** BBO is essential wherever function evaluation is expensive — hyperparameter tuning, A/B testing, drug discovery, chemical process optimization.

## The 8 Functions

| Func | Dim | Description |
|------|-----|-------------|
| F1   | 2D  | Radiation source detection — very peaked signal |
| F2   | 2D  | ML model log-likelihood — noisy, multi-modal |
| F3   | 3D  | Drug discovery — minimize adverse reactions |
| F4   | 4D  | Warehouse product placement — dynamic, local optima |
| F5   | 4D  | Chemical process yield — unimodal |
| F6   | 5D  | Cake recipe optimization — minimize negative scores |
| F7   | 6D  | ML hyperparameter tuning — 6 parameters |
| F8   | 8D  | Complex high-dimensional black-box |

## Project Structure

```
├── data/
│   ├── initial/           # Starter .npy data (function_1/ ... function_8/)
│   └── submissions/       # Per-round inputs and outputs (round_01/ ... round_13/)
├── notebooks/
│   ├── 01_exploration.ipynb      # Initial data analysis and visualization
│   ├── 02_framework.ipynb        # BO framework development
│   └── 03_optimization.ipynb     # Main iterative optimization loop
├── src/
│   ├── bo_utils.py               # Shared GP, EI, and data loading utilities
│   └── propose_round.py          # Per-round proposal script with configurable strategy
├── results/
│   └── tracking.md               # Round-by-round results and observations
├── docs/
│   ├── datasheet.md              # Data description, limitations, context
│   └── model_card.md             # Model behaviour, assumptions, limitations
└── question.md                   # Problem description
```

## Technical Approach

### Surrogate Model: Gaussian Process Regression
- **Kernel:** `ConstantKernel * Matern(nu=2.5) + WhiteKernel` — captures smooth non-linear relationships with noise handling
- The GP provides both predicted mean and uncertainty at every point

### Acquisition Function: Expected Improvement (EI)
- Balances **exploitation** (high predicted value) with **exploration** (high uncertainty)
- `xi` parameter controls the exploration/exploitation tradeoff
- Next point chosen by maximizing EI over random candidates in the search space

### Iterative Workflow
1. Load all available data (initial + submitted rounds)
2. Fit GP model per function
3. Propose next point via EI maximization
4. Submit, record results, analyze, and adjust strategy

### Key Design Decisions
- **Not using deep learning** — data volume is too low (10–40 initial samples per function) for neural approaches
- **Per-function strategy** — different functions respond to different exploration/exploitation settings
- **Phased approach** — early rounds explore broadly, later rounds exploit best-known regions

## Results Summary

*All 13 rounds complete. See `results/tracking.md` for full round-by-round history.*

| Function | Dim | Description              | Best Value  | Best Round | Improvement over Initial |
|----------|-----|--------------------------|-------------|------------|--------------------------|
| F1       | 2D  | Radiation source         | 8.58e-16    | Round 7    | +0.87e-16 (trivial)      |
| F2       | 2D  | ML log-likelihood        | 0.6747      | Round 6    | +0.064                   |
| F3       | 3D  | Drug discovery           | -0.0071     | Round 8    | +0.028                   |
| F4       | 4D  | Warehouse placement      | 0.6502      | Round 12   | +4.676                   |
| F5       | 4D  | Chemical yield           | 7715.6      | Round 6    | +6626.7                  |
| F6       | 5D  | Cake recipe              | -0.0153     | Round 13   | +0.699                   |
| F7       | 6D  | ML hyperparameters       | 1.6920      | Round 7    | +0.327                   |
| F8       | 8D  | Complex black-box        | 9.9711      | Round 7    | +0.373                   |

### Key findings

- **All 8 functions improved** over their initial best values across 13 rounds.
- **F5** achieved the largest absolute gain (+6627), found via broad EI in Round 6. The R6 value of 7716 was never replicated — confirming extreme sensitivity in the chemical yield landscape.
- **F4** was the most consistent Phase 3 improver, climbing steadily from -4.03 to +0.65 across 12 rounds.
- **F6** was the latest bloomer — flat for 9 rounds then improved in every remaining round, finishing at -0.015 in the final submission.
- **F7 and F8** both peaked in the Round 7 exploration round, confirming that a deliberate exploration reset unlocked regions that pure exploitation had missed.
- **F1** proved the hardest function — the radiation source peak is sub-0.001 wide, making reliable GP-guided search infeasible within the submission budget.

## Documentation

- **[Datasheet](docs/datasheet.md)** — Data description, limitations, and context
- **[Model Card](docs/model_card.md)** — Model behaviour, assumptions, limitations, and interpretability

## Dependencies

```
numpy, scikit-learn, scipy, matplotlib
```

Install: `uv sync` | Run notebooks: `uv run jupyter notebook`
