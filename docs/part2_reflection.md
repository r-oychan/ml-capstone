# Part 2: Reflect on Your Strategy

**1. In your function evaluations, which inputs seemed to act like support vectors — points near a decision boundary or region of rapid change? How might recognising them guide your next query?**

For Function 1, the point [0.731, 0.733] yielding 7.71e-16 defines an extremely narrow peak — output drops by ~30 orders of magnitude within a tiny neighbourhood. For Function 5, the jump from 1610 to 4121 at [0.596, 0.955, 0.996, 0.989] revealed a steep gradient as dimensions 2–4 approach 1.0. For Function 4, three rounds of negative outputs followed by a breakthrough to +0.327 pinpointed a transition from a poor region to a promising one. Concentrating future queries near such rapid-change regions should yield the most informative evaluations.

**2. If you trained a neural network or another surrogate model, did you explore how outputs change in response to inputs? If not, explain why you chose not to.**

We used a Gaussian Process (GP) with a Matérn 2.5 kernel, deliberately avoiding neural networks. With at most 44 observations per function, a neural network would severely overfit. The GP provides principled uncertainty quantification with minimal data, and its posterior variance feeds directly into Expected Improvement for calibrated confidence intervals. A neural network would need additional machinery (MC dropout or ensembles) to approximate this. The GP's differentiable kernel implicitly captures gradient information: when it predicts steep increases, EI naturally directs search there.

**3. Imagine framing your BBO project as a classification task ('good' vs 'bad' outputs). How could logistic regression, SVMs or neural networks capture this decision boundary? What trade-offs would you face between misclassification and exploration?**

An SVM with an RBF kernel would identify support vectors at the transition between high and low output. Logistic regression would provide smooth probabilities but might underfit non-linear boundaries in multi-modal functions like F2 or F4. The key trade-off: a classifier optimised for accuracy labels uncertain regions as "bad," discouraging exploration. With only 13 attempts, this is dangerous — we need to query uncertain points that could yield breakthroughs.

**4. Which type of model felt most appropriate for guiding your search? How did you balance interpretability against flexibility?**

The GP was most appropriate — flexible enough to capture non-linear patterns through its kernel, yet interpretable via mean and variance predictions. Inspecting fitted length scales revealed per-dimension sensitivity (e.g., short length scales in F1 confirmed its peaked nature). A linear model would be too rigid; a neural network too opaque and data-hungry. The GP's calibrated uncertainty was the most valuable asset for sequential decision-making under a strict budget.

**5. Which input variables showed the steepest gradients or greatest influence on predictions? How might you use this to prioritise next experiments?**

The GP's fitted length scales serve as a gradient analogue. For F5, shorter length scales on dimensions 2–4 indicated greatest influence, consistent with the best point pushing those dimensions toward 1.0. For F8 (8D), longer length scales on certain dimensions suggested they contribute less, allowing us to focus search along influential dimensions and reduce effective dimensionality.

**6. When framing as classification, how effectively did your neural network approximate the decision boundary? How did backpropagation help interpret or visualise this boundary?**

Since we used a GP, we did not use backpropagation directly. However, the GP's predictive variance effectively delineates the decision boundary — high-variance regions correspond to uncertain classification. The GP's analytical gradients achieve a similar interpretive role: they reveal which input directions most change the predicted output, helping visualise where the "good/bad" boundary lies without training a neural network.

**7. Compared to simpler models such as linear or logistic regression, how well did your neural network capture non-linear patterns in the function? Was the added flexibility worth the extra complexity in tuning and interpretation?**

The GP captured non-linear patterns effectively — F5's exponential growth, F4's local optima, and F1's sharp peak were all modelled well. A linear or logistic model would miss these structures entirely. A neural network might capture them too, but would overfit on our small datasets and lose the uncertainty estimates critical for acquisition function guidance. The GP's combination of non-linear flexibility, data efficiency, and built-in uncertainty made additional complexity unnecessary.
