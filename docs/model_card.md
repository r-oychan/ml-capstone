# Model Card: Gaussian Process for Bayesian Optimization

## Model Details

**Model type:** Gaussian Process Regression (GPR) used as a surrogate model within a Bayesian Optimization loop.

**Implementation:** scikit-learn `GaussianProcessRegressor`

**Kernel:** `ConstantKernel(1.0) * Matern(length_scale=0.5, nu=2.5) + WhiteKernel(noise_level=1e-5)`
- Matern(nu=2.5): models smooth but non-trivial functions; twice differentiable
- WhiteKernel: accounts for observation noise
- ConstantKernel: scales the overall amplitude

**Acquisition function:** Expected Improvement (EI) with exploration parameter xi=0.01

**Optimization:** EI maximized via random search over candidate points (default 10,000 candidates per iteration).

## Intended Use

**Primary use:** Propose the next query point for each of 8 black-box functions to maximize their output, given limited evaluation budget (13 rounds).

**Users:** ML practitioner (student) performing sequential optimization.

**Out of scope:** This model is not intended for real-time prediction or deployment. It is a surrogate used solely to guide the search process.

## Training Data

- **Initial data:** 10–40 points per function (provided as `.npy` files)
- **Accumulated data:** +1 point per function per submission round
- **Input range:** [0, 0.999999] for all dimensions
- **Output range:** Varies by function (from ~-7.6 to ~1610)

See `docs/datasheet.md` for full data description.

## Evaluation

**Metric:** Best function value found (higher is better) across all rounds.

**Current results (after 3 rounds):**

| Function | Best Value | Improvement over Initial |
|----------|-----------|------------------------|
| F1       | ~0.000    | none                   |
| F2       | 0.611     | none                   |
| F3       | -0.009    | +0.026                 |
| F4       | -0.228    | +3.798                 |
| F5       | 1609.836  | +520.977               |
| F6       | -0.173    | +0.541                 |
| F7       | 1.477     | +0.112                 |
| F8       | 9.905     | +0.306                 |

## Limitations

- **Scalability:** GP complexity is O(n^3) in the number of observations. Not an issue here (max ~55 points per function) but would not scale to thousands.
- **High dimensions:** GP surrogate quality degrades in higher dimensions (6D, 8D) with limited data. F7 and F8 are the hardest to optimize.
- **Local optima:** EI can get stuck exploiting a local optimum. Functions with multiple peaks (F2, F4) are challenging.
- **Kernel choice:** A single kernel (Matern 2.5) is used for all functions. Per-function kernel selection could improve results.
- **Candidate search:** Random search for EI maximization may miss the true EI optimum, especially in high dimensions.

## Ethical Considerations

No ethical concerns — all functions are synthetic with no real-world impact. No personal data is used.

## Assumptions

- Functions are smooth enough for GP modeling (Matern 2.5 assumption)
- Input domain is [0, 1) for all dimensions
- Observation noise is moderate (handled by WhiteKernel)
- All problems are maximization (minimization problems pre-negated)

## Recommendations

- Consider per-function kernel tuning (RBF for smooth, Matern 1.5 for rough)
- Increase candidate count for higher-dimensional functions
- Try alternative acquisition functions (UCB, PI) for stuck functions
- Use local search refinement around best-known points in later rounds
