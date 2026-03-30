# Datasheet: Black-Box Optimization Functions

## Motivation

**Purpose:** This dataset was created for the Imperial College Business School ML capstone project to teach Bayesian optimization under realistic constraints — limited evaluations of expensive black-box functions.

**Creators:** Imperial College Business School, Executive Education programme.

**Funding:** Part of the Professional Certificate in Machine Learning and Artificial Intelligence (PCMLAI) curriculum.

## Composition

**What does the dataset represent?**
Eight synthetic black-box functions that simulate real-world optimization problems (radiation detection, drug discovery, manufacturing, ML hyperparameter tuning, etc.). Each function maps a D-dimensional input to a scalar output.

**Instances:**

| Function | Input Dim | Initial Samples | Domain Analogy |
|----------|-----------|-----------------|----------------|
| F1       | 2         | 10              | Radiation source detection |
| F2       | 2         | 10              | ML model log-likelihood |
| F3       | 3         | 15              | Drug compound side effects |
| F4       | 4         | 30              | Warehouse product placement |
| F5       | 4         | 20              | Chemical process yield |
| F6       | 5         | 20              | Recipe optimization |
| F7       | 6         | 30              | ML hyperparameter tuning |
| F8       | 8         | 40              | Complex 8D optimization |

**Total initial data points:** 175 across all functions.

**Data format:**
- Inputs: NumPy arrays (`.npy`), each row is a D-dimensional point in [0, 1)
- Outputs: NumPy arrays (`.npy`), scalar values per input point

**Labels:** Outputs are the objective function values. All problems are framed as maximization (minimization problems are negated).

**Confidentiality:** No personal or sensitive data. All functions are synthetic.

## Collection Process

**How was the data acquired?** Provided by the course as starter datasets. The underlying functions are hidden — we can only observe input-output pairs.

**Sampling strategy:** Initial data points appear to be drawn from a space-filling design (likely Latin Hypercube or similar) within [0, 1) for each dimension.

**Time period:** Data provided at project start; additional points collected iteratively via portal submissions over the course duration.

## Preprocessing / Cleaning

No preprocessing applied to initial data. All values used as provided.

For submitted round data, inputs and outputs are stored as Python-formatted text files and parsed programmatically.

## Uses

**Intended use:** Training in Bayesian optimization, surrogate modeling, and sequential decision-making under uncertainty.

**Not suitable for:** The functions are synthetic and domain-specific insights (e.g., "best drug compound ratios") should not be taken literally.

## Distribution

Distributed via the PCMLAI course platform. Initial data downloadable as `.npy` files in a ZIP archive.

## Maintenance

Dataset is static (initial points don't change). Additional data points are accumulated through the iterative submission process — up to 13 rounds of 8 new points each.

## Limitations

- **Small sample sizes:** 10–40 initial points per function, growing by 1 per round
- **No ground truth:** The true function formulas are unknown
- **Fixed input domain:** All inputs constrained to [0, 0.999999]
- **Noisy observations:** Some functions (especially F2) have noisy outputs
- **No feature descriptions:** Input dimensions have no meaningful labels beyond the domain analogy
