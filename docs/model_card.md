# Model Card: Gaussian Process for Bayesian Optimization

## Model Details

**Model type:** Gaussian Process Regression (GPR) used as a surrogate model within a Bayesian Optimization loop.

**Implementation:** scikit-learn `GaussianProcessRegressor`

**Kernel:** `ConstantKernel(1.0, (0.1, 10.0)) * Matern(length_scale=0.5, nu=2.5) + WhiteKernel(noise_level=1e-5, noise_level_bounds=(1e-8, 1e-1))`
- Matern(nu=2.5): models smooth but non-trivial functions; twice differentiable
- WhiteKernel: accounts for observation noise, with learned noise level
- ConstantKernel: scales the overall amplitude

**Acquisition function:** Expected Improvement (EI) with per-function exploration parameter xi (ranging from 0.001 for exploitation to 0.05 for exploration).

**Optimization:** EI maximized via random candidate search with per-function local/broad split. Candidate counts ranged from 100k to 300k depending on function dimensionality and search strategy.

## Intended Use

**Primary use:** Propose the next query point for each of 8 black-box functions to maximize their output, given limited evaluation budget (13 rounds).

**Users:** ML practitioner (student) performing sequential optimization.

**Out of scope:** This model is not intended for real-time prediction or deployment. It is a surrogate used solely to guide the search process.

## Training Data

- **Initial data:** 10-40 points per function (provided as `.npy` files)
- **Accumulated data:** +1 point per function per submission round (13 rounds total)
- **Final dataset size:** 23-53 points per function
- **Input range:** [0, 0.999999] for all dimensions
- **Output range:** Varies by function (from -4.03 to 7716)

See `docs/datasheet.md` for full data description.

## Evaluation

**Metric:** Best function value found (higher is better) across all 13 rounds.

**Final results (all 13 rounds complete):**

| Function | Dim | Best Value | Best Round | Improvement over Initial |
|----------|-----|-----------|------------|--------------------------|
| F1       | 2D  | 8.58e-16  | Round 7    | +0.87e-16 (trivial)      |
| F2       | 2D  | 0.6747    | Round 6    | +0.064                   |
| F3       | 3D  | -0.0071   | Round 8    | +0.028                   |
| F4       | 4D  | 0.6502    | Round 12   | +4.676                   |
| F5       | 4D  | 7715.6    | Round 6    | +6626.7                  |
| F6       | 5D  | -0.0153   | Round 13   | +0.699                   |
| F7       | 6D  | 1.6920    | Round 7    | +0.327                   |
| F8       | 8D  | 9.9711    | Round 7    | +0.373                   |

**All 8 functions improved** over their initial best values.

## Performance Analysis

**Where the model worked well:**
- **F4** (4D): Most consistent improver. Climbed steadily from -4.03 to +0.65 across 12 rounds. The GP surrogate accurately guided exploitation in a landscape with gradual gradients.
- **F5** (4D): Largest absolute gain (+6627). The unimodal, smooth landscape was well-suited to the Matern 2.5 kernel.
- **F7/F8** (6D/8D): Both peaked during the Round 7 exploration round, demonstrating that deliberate broad search can unlock regions missed by exploitation.

**Where the model struggled:**
- **F1** (2D): The radiation source function has a sub-0.001-wide peak. The GP modelled it as a flat surface near zero, producing EI=0 everywhere. The surrogate was fundamentally unable to represent the extreme spikiness.
- **F2** (2D): Noisy, multimodal function. The GP gave different predictions at nearly identical points (0.675 vs 0.470 at the same region), indicating the noise model was insufficient.
- **F5 in later rounds**: Output values spanning 92 to 7716 violate the GP's homoscedastic noise assumption. The R6 best of 7716 was never replicated despite 7 subsequent attempts.

## Limitations

- **Single kernel for all functions:** Matern(nu=2.5) was used uniformly. F1 needed a rougher kernel (nu=0.5) for its spiky peak; F5 needed output transformations for its heteroscedastic range.
- **Homoscedastic noise assumption:** WhiteKernel assumes constant noise variance across the input space. Functions like F2 (noisy) and F5 (extreme range) violate this.
- **Random candidate search:** EI was maximized by evaluating random candidates rather than gradient-based optimization. This is inefficient in higher dimensions (F7, F8) and may miss narrow EI peaks.
- **GP overconfidence:** For F1, the GP assigned near-zero uncertainty everywhere, collapsing EI to zero. This prevented any meaningful acquisition-guided search.
- **Scalability:** GP complexity is O(n^3) in observations. Not an issue at our scale (max 53 points) but would not scale to thousands.
- **No output transformations:** Log or power transforms (as used in HEBO) could have helped with F5's extreme output range.

## Ethical Considerations

No ethical concerns. All functions are synthetic with no real-world impact. No personal data is used.

## Assumptions

- Functions are smooth enough for GP modeling (Matern 2.5 assumption)
- Input domain is [0, 1) for all dimensions
- Observation noise is moderate and constant (homoscedastic)
- All problems are maximization

## What We Would Do Differently

Based on 13 rounds of evidence:

1. **Per-function kernels**: Matern(nu=0.5) for F1 (spiky), wider noise bounds for F2 (noisy), RBF for F5 (smooth, unimodal)
2. **Output transformations**: Power or log transforms for F5 to handle 3-order-of-magnitude output range (as recommended by HEBO)
3. **L-BFGS-B multi-start EI optimization**: Replace random candidate search with gradient-based optimization of the acquisition function
4. **Max-uncertainty fallback**: When EI=0 (F1), switch to querying the point of maximum GP uncertainty rather than abandoning the function
5. **Adaptive trust regions**: Use TuRBO-style trust regions that expand/contract based on success, rather than manually tuning radius per round
