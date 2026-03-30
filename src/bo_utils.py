"""
Bayesian Optimization utilities for the Black-Box Optimization challenge.

Core functions for GP fitting, acquisition, data loading, and result tracking.
"""

import numpy as np
import os
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel
from scipy.stats import norm


# ── Function metadata ──────────────────────────────────────────────────────

FUNCTIONS = {
    1: {"dim": 2, "n_initial": 10, "desc": "Radiation source detection (peaked)"},
    2: {"dim": 2, "n_initial": 10, "desc": "ML log-likelihood (noisy, multi-modal)"},
    3: {"dim": 3, "n_initial": 15, "desc": "Drug discovery (minimize side effects)"},
    4: {"dim": 4, "n_initial": 30, "desc": "Warehouse placement (dynamic, local optima)"},
    5: {"dim": 4, "n_initial": 20, "desc": "Chemical yield (unimodal)"},
    6: {"dim": 5, "n_initial": 20, "desc": "Cake recipe (negative scores)"},
    7: {"dim": 6, "n_initial": 30, "desc": "ML hyperparameter tuning (6 params)"},
    8: {"dim": 8, "n_initial": 40, "desc": "Complex 8D black-box"},
}


# ── Data loading ───────────────────────────────────────────────────────────

def load_initial_data(func_num, data_dir="data/initial"):
    """Load the initial .npy data for a function."""
    X = np.load(os.path.join(data_dir, f"function_{func_num}", "initial_inputs.npy"))
    y = np.load(os.path.join(data_dir, f"function_{func_num}", "initial_outputs.npy"))
    return X, y


def parse_submission_line(line):
    """Parse a single submission line: [array([...]), array([...]), ...]"""
    line = line.strip()
    if not line:
        return []
    line = line.replace("array(", "np.array(")
    return eval(line, {"np": np})


def parse_output_line(line):
    """Parse a single output line: [np.float64(...), np.float64(...), ...]"""
    import ast
    line = line.strip()
    if not line:
        return []
    line = line.replace("np.float64(", "").replace(")", "")
    return ast.literal_eval(line)


def load_round_data(round_num, submissions_dir="data/submissions"):
    """Load inputs and outputs for a specific round."""
    round_dir = os.path.join(submissions_dir, f"round_{round_num:02d}")
    inputs_path = os.path.join(round_dir, "inputs.txt")
    outputs_path = os.path.join(round_dir, "outputs.txt")

    if not os.path.exists(inputs_path) or not os.path.exists(outputs_path):
        return None, None

    with open(inputs_path, "r") as f:
        inputs = parse_submission_line(f.read())
    with open(outputs_path, "r") as f:
        outputs = parse_output_line(f.read())

    return inputs, outputs


def load_all_data(func_num, data_dir="data/initial", submissions_dir="data/submissions"):
    """
    Load initial data + all submitted rounds for a function.
    Returns merged (X, y) arrays.
    """
    X, y = load_initial_data(func_num, data_dir)

    round_num = 1
    while True:
        inputs, outputs = load_round_data(round_num, submissions_dir)
        if inputs is None:
            break
        # Extract this function's data (0-indexed)
        new_x = inputs[func_num - 1].reshape(1, -1)
        new_y = np.array([outputs[func_num - 1]])
        X = np.vstack([X, new_x])
        y = np.concatenate([y, new_y])
        round_num += 1

    return X, y


def get_completed_rounds(submissions_dir="data/submissions"):
    """Count how many rounds have been completed."""
    round_num = 0
    while os.path.exists(os.path.join(submissions_dir, f"round_{round_num + 1:02d}", "outputs.txt")):
        round_num += 1
    return round_num


# ── GP model ───────────────────────────────────────────────────────────────

def fit_gp_model(X, y, random_state=0):
    """Fit a Gaussian Process with Matern kernel."""
    kernel = (
        ConstantKernel(1.0, (0.1, 10.0))
        * Matern(length_scale=0.5, nu=2.5)
        + WhiteKernel(noise_level=1e-5, noise_level_bounds=(1e-8, 1e-1))
    )
    gp = GaussianProcessRegressor(
        kernel=kernel,
        n_restarts_optimizer=5,
        normalize_y=True,
        random_state=random_state,
    )
    gp.fit(X, y)
    return gp


# ── Acquisition functions ──────────────────────────────────────────────────

def expected_improvement(X_candidates, gp, y_best, xi=0.01):
    """Expected Improvement acquisition function."""
    mu, sigma = gp.predict(X_candidates, return_std=True)
    mu = mu.reshape(-1, 1)
    sigma = sigma.reshape(-1, 1)
    sigma = np.maximum(sigma, 1e-9)

    improvement = mu - y_best - xi
    Z = improvement / sigma
    ei = improvement * norm.cdf(Z) + sigma * norm.pdf(Z)
    ei[sigma == 0.0] = 0.0
    return ei.ravel()


# ── Search space ───────────────────────────────────────────────────────────

INPUT_MIN = 0.0
INPUT_MAX = 0.999999


def infer_bounds_from_data(X, pad_ratio=0.05):
    """Infer bounds from data with padding, clamped to [0, 0.999999]."""
    X = np.asarray(X)
    mins = X.min(axis=0)
    maxs = X.max(axis=0)
    padding = (maxs - mins) * pad_ratio
    mins -= padding
    maxs += padding
    mins = np.maximum(mins, INPUT_MIN)
    maxs = np.minimum(maxs, INPUT_MAX)
    return np.vstack([mins, maxs]).T


def sample_random_points(bounds, n_points, random_state=None):
    """Sample uniformly inside the hyper-rectangle defined by bounds."""
    rng = np.random.default_rng(random_state)
    D = bounds.shape[0]
    return rng.uniform(bounds[:, 0], bounds[:, 1], size=(n_points, D))


# ── Proposal ───────────────────────────────────────────────────────────────

def propose_next_point(X, y, bounds, n_candidates=10000, xi=0.01, random_state=0):
    """Propose next point by maximizing Expected Improvement."""
    X = np.asarray(X)
    y = np.asarray(y).ravel()

    gp = fit_gp_model(X, y, random_state=random_state)
    y_best = y.max()

    X_candidates = sample_random_points(bounds, n_candidates, random_state=random_state)
    ei = expected_improvement(X_candidates, gp, y_best, xi=xi)
    best_idx = np.argmax(ei)

    x_next = np.clip(X_candidates[best_idx], INPUT_MIN, INPUT_MAX)
    return x_next, ei[best_idx], gp


# ── Submission formatting ──────────────────────────────────────────────────

def format_submission(point):
    """
    Format a point for portal submission.
    Rules: each value starts with 0, exactly 6 decimals, hyphen-separated, no spaces.
    """
    point = np.clip(np.asarray(point), INPUT_MIN, INPUT_MAX)
    return "-".join(f"{v:.6f}" for v in point)


def format_all_submissions(points):
    """Format all 8 function points for submission. Prints portal-ready strings."""
    for i, pt in enumerate(points):
        print(f"Function {i+1}: {format_submission(pt)}")


# ── Results tracking ───────────────────────────────────────────────────────

def get_best_per_function(data_dir="data/initial", submissions_dir="data/submissions"):
    """Get the best output value found so far for each function."""
    results = {}
    for func_num in range(1, 9):
        X, y = load_all_data(func_num, data_dir, submissions_dir)
        best_idx = np.argmax(y)
        results[func_num] = {
            "best_value": y[best_idx],
            "best_point": X[best_idx],
            "n_samples": len(y),
        }
    return results


def print_status_report(data_dir="data/initial", submissions_dir="data/submissions"):
    """Print a summary of current optimization status."""
    n_rounds = get_completed_rounds(submissions_dir)
    results = get_best_per_function(data_dir, submissions_dir)

    print(f"Completed rounds: {n_rounds}/13")
    print(f"Remaining attempts: {13 - n_rounds}")
    print("=" * 70)
    print(f"{'Func':>4} {'Dim':>3} {'Samples':>7} {'Best Value':>14} {'Best Point'}")
    print("-" * 70)
    for func_num in range(1, 9):
        r = results[func_num]
        dim = FUNCTIONS[func_num]["dim"]
        pt_str = np.array2string(r["best_point"], precision=4, separator=", ")
        print(f"  F{func_num}  {dim}D  {r['n_samples']:>5}   {r['best_value']:>14.6f}  {pt_str}")
    print("=" * 70)
