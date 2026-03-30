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
│   └── submissions/       # Per-round inputs and outputs
│       ├── round_01/
│       ├── round_02/
│       └── round_03/
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

*Updated as rounds progress. See `results/tracking.md` for full history.*

| Function | Dim | Best Value Found | Improvement over Initial |
|----------|-----|-----------------|------------------------|
| F1       | 2D  | ~0.000          | —                      |
| F2       | 2D  | 0.611           | —                      |
| F3       | 3D  | -0.009          | +0.026                 |
| F4       | 4D  | -0.228          | +3.798                 |
| F5       | 4D  | 1609.836        | +520.977               |
| F6       | 5D  | -0.173          | +0.541                 |
| F7       | 6D  | 1.477           | +0.112                 |
| F8       | 8D  | 9.905           | +0.306                 |

## Documentation

- **[Datasheet](docs/datasheet.md)** — Data description, limitations, and context
- **[Model Card](docs/model_card.md)** — Model behaviour, assumptions, limitations, and interpretability

## Dependencies

```
numpy, scikit-learn, scipy, matplotlib
```

Install: `uv sync` | Run notebooks: `uv run jupyter notebook`
