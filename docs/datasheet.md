# Datasheet: Black-Box Optimisation Functions

This datasheet documents the optimisation decisions, learning and reasoning for every function in the black-box optimisation project, following the Module 25 template structure.

---

## Function Overview

### F1: Radiation Source Detection (2D)

- **Real-world scenario:** Locating a radioactive contamination source in a 2D spatial grid
- **Dimensionality:** 2D input
- **Initial data points:** 10
- **Output represents:** Signal strength (extremely peaked; near-zero everywhere except at the source)

### F2: ML Model Log-Likelihood (2D)

- **Real-world scenario:** Tuning 2 hyperparameters of a machine learning model to maximise log-likelihood
- **Dimensionality:** 2D input
- **Initial data points:** 10
- **Output represents:** Log-likelihood score (noisy, multimodal)

### F3: Drug Discovery (3D)

- **Real-world scenario:** Optimising a drug compound formulation to minimise adverse side effects
- **Dimensionality:** 3D input
- **Initial data points:** 15
- **Output represents:** Negative adverse reaction severity (higher = fewer side effects)

### F4: Warehouse Product Placement (4D)

- **Real-world scenario:** Optimising product placement in a warehouse across 4 configuration parameters
- **Dimensionality:** 4D input
- **Initial data points:** 30
- **Output represents:** Placement efficiency score (contains local optima)

### F5: Chemical Process Yield (4D)

- **Real-world scenario:** Maximising chemical production yield by tuning 4 process parameters
- **Dimensionality:** 4D input
- **Initial data points:** 20
- **Output represents:** Chemical yield (unimodal, extreme output range: 92 to 7716)

### F6: Cake Recipe Optimisation (5D)

- **Real-world scenario:** Optimising a recipe across 5 ingredient/process parameters
- **Dimensionality:** 5D input
- **Initial data points:** 20
- **Output represents:** Negative recipe score (values near 0 are best)

### F7: ML Hyperparameter Tuning (6D)

- **Real-world scenario:** Tuning 6 hyperparameters of a machine learning model
- **Dimensionality:** 6D input
- **Initial data points:** 30
- **Output represents:** Model performance score

### F8: Complex High-Dimensional Black-Box (8D)

- **Real-world scenario:** Complex optimisation problem with 8 input dimensions
- **Dimensionality:** 8D input
- **Initial data points:** 40
- **Output represents:** Unknown performance metric

---

## Nature of the Data

### Dataset structure

- **Inputs:** NumPy arrays (`.npy`), each row is a D-dimensional point in [0, 0.999999]
- **Outputs:** NumPy arrays (`.npy`), scalar values per input point
- **Initial sizes:** 10 samples (F1, F2), 15 (F3), 20 (F5, F6), 30 (F4, F7), 40 (F8)
- **Final sizes:** 23 samples (F1, F2) to 53 (F8) after 13 submission rounds

### Dataset evolution across rounds

Each round added exactly 1 new observation per function. The exploration pattern shifted across three phases:
- **Rounds 1-3:** Uniform broad search with 10k random candidates. Sampling was largely undirected.
- **Rounds 4-7:** Per-function strategy introduced. Local search near known bests mixed with broad exploration. Round 7 was a deliberate full-exploration round.
- **Rounds 8-13:** Tight exploitation with progressively shrinking search radii (0.15 down to 0.001) and increasing candidate counts (up to 300k).

### Noise and randomness per function

| Function | Noise Level | Evidence |
|----------|------------|---------|
| F1 | None apparent | Output is deterministic but extremely peaked (sub-0.001 wide). All values effectively 0 except at exact peak. |
| F2 | **High** | Same region [0.70, 0.93] returned values from 0.470 to 0.675 across rounds. Repeated queries gave different results. |
| F3 | Low-moderate | Values near best were consistent (-0.007 to -0.015) but small perturbations caused larger shifts. |
| F4 | Low | Steady improvement trajectory suggests smooth, low-noise landscape with gradual gradients. |
| F5 | **Extreme** | R6 best of 7716 at [0.989, 0.949, 0.965, 0.929]. Nearly identical point in R13 returned 92. Function appears highly sensitive. |
| F6 | Moderate | Nearby points gave -0.074 and -0.367 in consecutive rounds. |
| F7 | Low-moderate | Consistent recovery pattern (1.159 to 1.580 over 4 rounds) suggests smooth landscape with noise. |
| F8 | Low | Outputs stable around 9.9 for 5 consecutive rounds. Consistent but unable to exceed R7 peak. |

### Function modality (based on observations)

| Function | Apparent Modality | Reasoning |
|----------|------------------|-----------|
| F1 | Extremely peaked (needle-in-haystack) | Two peaks found at [0.731, 0.733] and [0.923, 0.954], both ~1e-16. GP surface is flat near zero everywhere. |
| F2 | Multimodal, noisy | GP surface shows multiple peaks. Best region at [0.70, 0.93] but competing optima visible in 3D plots. |
| F3 | Likely unimodal | Best points cluster around [0.36-0.41, 0.33-0.37, 0.42-0.46]. Consistent region across rounds. |
| F4 | Unimodal with gradual gradient | Optimum drifted smoothly from [0.395, 0.438] to [0.353, 0.401] across 9 rounds. |
| F5 | Unimodal but extremely sensitive | Clear gradient toward high values on dims 2-4 (near 1.0), but output magnitude varies wildly. |
| F6 | Likely unimodal, late-converging | Flat for 9 rounds, then rapid improvement in final 3. Best region near [0.43, 0.41, 0.60, 0.78, 0.09]. |
| F7 | Broad optimum | Best at [0.0, 0.23, 0.23, 0.21, 0.27, 0.89]. Dim 1 consistently at boundary (0.0). |
| F8 | Broad, high-dimensional | Stable ~9.9 across many different points. Best at [0.157, 0.041, 0.081, 0.036, 0.556, 0.283, 0.151, 0.558]. |

---

## Optimisation Strategy

### Method

Bayesian Optimisation using Gaussian Process regression as the surrogate model, with Expected Improvement (EI) as the acquisition function. EI was maximised via random candidate search with a configurable mix of local candidates (near the best known point) and broad candidates (across the full domain).

### Why this method

- **Sample efficiency:** With only 13 total evaluations per function and 10-40 initial points, GP-based BO is the most sample-efficient approach for low-to-moderate dimensionality (2D-8D)
- **Uncertainty quantification:** GPs provide closed-form uncertainty estimates, enabling principled exploration-exploitation tradeoffs
- **No gradient access:** The functions are black-box with no derivative information, ruling out gradient-based methods
- **Small data regime:** 10-53 points per function is far too few for neural network surrogates

### Exploration-exploitation balance

Controlled via three parameters per function:
- **xi (exploration parameter):** Low (0.001) for exploitation, medium (0.01) for balanced, high (0.02-0.05) for exploration
- **radius:** Local search neighbourhood around current best point (0.001 to 0.15)
- **n_local / n_broad:** Split between exploitation candidates near best and exploration candidates across full domain

### Strategy evolution across rounds

| Phase | Rounds | Strategy | Rationale |
|-------|--------|----------|-----------|
| Baseline | 1-3 | Uniform xi=0.01, 10k candidates, same seed | Initial exploration. Produced 7 new bests across 3 rounds but hit diminishing returns due to fixed random seed causing duplicate proposals. |
| Phase 1 | 4-6 | Per-function xi, local/broad mix, 50k-200k candidates | Functions respond differently. F1 needs precision, F5 needs broad search, F4 needs exploitation. Best single-round results (R6: 3 new bests). |
| Phase 2 | 7 | Full exploration: xi=0.05, broad-heavy for all | Deliberate reset after sustained exploitation. Produced 4 new bests including F7/F8 all-time bests. Most surprising result of the project. |
| Phase 3 | 8-13 | Pure exploitation: xi=0.001, tight radii (0.001-0.02), 150k-300k candidates | Convert GP model quality into score improvements. F4 climbed steadily, F6 broke through in R10-13. |

---

## Data Handling and Preprocessing

### Input rescaling

No rescaling applied. All inputs are naturally in [0, 0.999999]. The GP's `normalize_y=True` setting handles output normalisation internally.

### Surrogate model

Gaussian Process Regressor from scikit-learn with kernel:
```
ConstantKernel(1.0, (0.1, 10.0)) * Matern(length_scale=0.5, nu=2.5) + WhiteKernel(noise_level=1e-5, noise_level_bounds=(1e-8, 1e-1))
```

- **Matern(nu=2.5):** Assumes twice-differentiable functions. Standard BO default.
- **WhiteKernel:** Models observation noise with learned noise level.
- **n_restarts_optimizer=5:** Restarts kernel hyperparameter optimisation to avoid local optima.

### Outlier handling

No outliers were removed. F5's extreme output range (92 to 7716) was left untransformed, which in hindsight was a limitation. Output power transforms (as used in HEBO) would have been more appropriate for heteroscedastic functions.

---

## Weekly Iteration and Learning

### How new data changed understanding

- **Rounds 1-3:** Revealed that F5 responds well to BO while F1 returns ~0 regardless of input. Identified F3/F4/F6 best values from R1 that took many rounds to beat.
- **Round 4:** Per-function tuning validated. F4 went positive for the first time (+0.327), F5 jumped to 4121.
- **Rounds 5-6:** F5's dims 2-4 pushing toward 1.0 became clear. R6 produced F5's all-time best (7716).
- **Round 7:** Exploration reset revealed F1's second peak at [0.923, 0.954] and set F7/F8 bests that exploitation never matched.
- **Rounds 8-13:** F4's optimum was drifting (dim 1: 0.395 to 0.353 across rounds). F6 was flat until R10 then suddenly responded to tight exploitation.

### Local optima encountered

- **F4:** Early submissions in rounds 2-3 were trapped near [0.44, 0.42, 0.34, 0.47] with negative outputs. Breaking free required the per-function tuning shift in R4.
- **F2:** Multiple competing peaks visible in GP surface. Queries sometimes went to wrong peak (0.15 vs 0.67 at different locations).
- **F6:** Stuck at -0.173 from R1 for 9 rounds. Only broke through when R10's slight parameter shift found -0.117.

### Most informative queries

- **R6 F5 [0.989, 0.949, 0.965, 0.929] = 7716:** Revealed the extreme sensitivity of the chemical yield function. All subsequent attempts to replicate failed.
- **R7 exploration round:** 4 new bests from broad search. Proved that the GP had blind spots that exploitation alone could never find.
- **R11 F1 [0.15, 0.55] = -1.17e-64:** Deliberate exploration of the largest unexplored region (identified via maximin distance analysis). Confirmed that F1's peaks are only at [0.731, 0.733] and [0.923, 0.954].
- **R13 F5 [0.999, 0.959, 0.973, 0.938] = 92:** Nearly identical to R6 best but output was 99% lower. Revealed catastrophic sensitivity that the GP could not model.

### What we would do differently

1. **Per-function kernels from the start:** Matern(nu=0.5) for F1's spiky peak, wider noise bounds for F2
2. **Output power transforms for F5:** Handle the 92-to-7716 range properly (HEBO approach)
3. **L-BFGS-B multi-start EI optimisation:** Replace random candidate search with gradient-based acquisition optimisation
4. **Max-uncertainty fallback for F1:** When EI=0, query the point of maximum GP uncertainty instead of abandoning the function
5. **Per-function random seeds from R1:** The fixed seed in rounds 1-3 caused near-duplicate proposals, wasting 2 rounds

---

## Performance and Results

### Per-function results

| Function | Best Value | Best Input | Best Round | Improvement | Confidence in Global Max |
|----------|-----------|-----------|------------|-------------|--------------------------|
| F1 | 8.58e-16 | [0.923, 0.954] | R7 | +0.87e-16 | **Very low.** Value is essentially 0. Peak is sub-0.001 wide; we likely never found the true maximum. |
| F2 | 0.6747 | [0.699, 0.926] | R6 | +0.064 | **Low.** High noise means same region gives 0.47-0.67. May not be global max. |
| F3 | -0.0071 | [0.392, 0.358, 0.435] | R8 | +0.028 | **Moderate.** Consistent cluster of near-optimal points. Likely near a local/global max. |
| F4 | 0.6502 | [0.360, 0.402, 0.427, 0.418] | R12 | +4.676 | **Moderate.** Still improving in R12; more rounds would likely find higher values. |
| F5 | 7715.6 | [0.989, 0.949, 0.965, 0.929] | R6 | +6627 | **Low.** Never replicated in 7 attempts. May be a lucky evaluation rather than the true peak. |
| F6 | -0.0153 | [0.432, 0.413, 0.599, 0.774, 0.091] | R13 | +0.699 | **Moderate.** Was still improving; likely near but not at the global max. |
| F7 | 1.6920 | [0.000, 0.229, 0.232, 0.205, 0.271, 0.893] | R7 | +0.327 | **Moderate.** Found via exploration; exploitation never matched it. May be near global max. |
| F8 | 9.9711 | [0.157, 0.041, 0.081, 0.036, 0.556, 0.283, 0.151, 0.558] | R7 | +0.373 | **Moderate.** Stable ~9.9 across many rounds. Likely near but not at global max in 8D space. |

### Alignment with expectations

- **F5 (chemical yield):** Expected a smooth, unimodal function. The extreme sensitivity (7716 vs 92 at nearly identical points) was unexpected and suggests either noise or extreme non-linearity.
- **F1 (radiation source):** Expected a peaked function but not this extreme. The sub-0.001 peak width made GP-based search fundamentally infeasible.
- **F4 (warehouse):** Description mentioned "local optima" but the function behaved more like a smooth gradient with a drifting optimum. Exceeded expectations.
- **F7/F8:** Both responded best to exploration rather than exploitation, suggesting the initial data was insufficient to characterise these higher-dimensional landscapes.

---

## Ethical, Practical and General Considerations

### Real-world applicability

BBO directly applies to any setting where function evaluation is expensive:
- Drug discovery (clinical trials are costly and slow)
- Manufacturing process optimisation (production line changes are disruptive)
- ML hyperparameter tuning (training runs are compute-intensive)
- A/B testing (each test consumes real user traffic)

### Limitations from synthetic nature

- The true functions are unknown, so we cannot validate whether the GP's assumptions (smoothness, stationarity) were appropriate
- No feature names or domain knowledge to guide the search
- Fixed input domain [0, 0.999999] may not reflect real-world constraints

### Scalability

- **Would scale to:** Problems with <100 dimensions and <1000 observations (GP complexity is O(n^3))
- **Would not scale to:** High-dimensional problems (>20D) without modifications like TuRBO trust regions or random embeddings
- **Budget constraint:** The 13-round limit mirrors real-world settings where evaluations are expensive, making the approach directly transferable

### Risks and pitfalls

- **GP overconfidence:** When the model is confident but wrong (as with F1), EI collapses to zero and the search stalls entirely. Users should monitor uncertainty estimates and add fallback strategies.
- **Heteroscedastic outputs:** Functions with extreme output ranges (like F5: 92-7716) violate the GP's constant-noise assumption. Output transforms are essential.
- **Lucky evaluations:** F5's best of 7716 was never replicated, raising the question of whether it was a genuine peak or a lucky noise realisation. Users should not over-interpret single outlier results.
