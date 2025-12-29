# Capstone Project - Bayesian Optimization

## Overview
This project focuses on using Bayesian Optimization to find the maximum values of unknown "black-box" functions. We are provided with initial datasets for 8 different functions and are tasked with iteratively querying these functions to converge on the global maximum.

## Notebook: `3.ipynb`

The main work is contained in the Jupyter Notebook `3.ipynb`. This notebook performs the following tasks:

1.  **Data Loading & Merging**:
    -   Loads initial training data from `.npy` files located in `initial_data/function_X/`.
    -   Parses and loads historical submission data from `inputs.txt`, `inputs2.txt`, `outputs.txt`, and `outputs2.txt`.
    -   Merges these datasets to create a comprehensive history of all known points for each function.

2.  **Gaussian Process Regression (GPR)**:
    -   Models the objective function using a Gaussian Process with a Matern kernel.
    -   This provides both a mean prediction and an uncertainty estimate (standard deviation) across the search space.

3.  **Acquisition Function**:
    -   Uses **Expected Improvement (EI)** to balance exploration (searching high-uncertainty areas) and exploitation (refining around known high-value areas).
    -   Optimizes the EI function to propose the next best point to query.

4.  **Visualization**:
    -   Includes 3D scatter plots to visualize the spatial distribution of sampled points and their values.

## How to Run

1.  **Prerequisites**:
    Ensure you have the following Python libraries installed:
    ```bash
    pip install numpy scipy matplotlib scikit-learn
    ```

2.  **Execution**:
    -   Open `3.ipynb` in VS Code or Jupyter Lab.
    -   Run the cells sequentially.
    -   **Cell 1**: Loads and merges the data for Function 1.
    -   **Subsequent Cells**: Define the GP model, acquisition function, and generate proposals for Functions 1 through 8.
    -   The notebook will output the "Next point to sample" and the "EI" value for that point.

## Methodology & Progress

We have been following an iterative optimization loop:

1.  **Analyze Current Data**: We start with the provided initial samples.
2.  **Model**: We fit a Gaussian Process to the available data $(X, y)$.
3.  **Propose**: We maximize the Expected Improvement acquisition function to find the next query point $x_{new}$.
4.  **Submit & Update**: We submit these points (simulated here by reading from `inputs.txt`/`outputs.txt`), receive the true function values, and append them to our dataset.
5.  **Repeat**: We re-fit the GP model with the updated dataset and repeat the process to refine our search for the global maximum.

Recent updates to the code include robust parsing logic to handle multi-line array formats in the text files, ensuring all historical data is correctly utilized for the next prediction.
