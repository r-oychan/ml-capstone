# Part 2: Reflection Answers (Module 16 — after Round 5)

## Q1: Hierarchical feature learning & optimisation strategy

Hierarchical feature learning influenced how I layered my optimisation strategy. In early rounds, I used uniform settings across all functions — analogous to early layers learning coarse features — to build a broad understanding of each function's landscape. In later rounds, I built on this foundation with per-function tuning, adjusting exploration parameters and search radii based on observed behaviour. For instance, for one function I first identified which dimensions dominate the output (coarse structure), then refined the remaining dimensions (fine detail). This decomposition — solve gross structure first, then fine-tune — mirrors how deep networks compose simple low-level representations into complex high-level ones.

## Q2: AlexNet/ImageNet breakthroughs vs incremental capstone improvements

Most of my rounds yielded incremental gains — steadily climbing values through small parameter adjustments. But certain rounds produced breakthrough jumps, not from minor tweaks but from strategic pivots: switching from a one-size-fits-all approach to per-function strategies, or discovering that certain dimensions should be pushed to their boundary values. Like AlexNet succeeding by rethinking the approach entirely (deep CNNs plus GPU training) rather than tuning existing methods, my biggest improvements came from fundamentally changing how I framed the problem. The lesson is that sustained incremental work creates conditions for breakthroughs, but the breakthroughs themselves require rethinking assumptions.

## Q3: Depth/complexity/efficiency trade-offs & explore vs exploit

This maps directly to my explore-exploit dilemma. Like choosing network depth — deeper models learn more but risk overfitting and cost more to train — I balanced broad exploration against tight exploitation with a fixed budget of 13 total attempts. For peaked functions, aggressive exploitation with a tiny search radius overfit to a narrow region and missed the true optimum, much like an overparameterised network. For smoother functions, a balanced approach — broad search initially then focused exploitation — worked well, like a right-sized architecture. With limited remaining attempts, allocating my "training budget" wisely across functions mirrors the efficiency constraints of choosing appropriate model complexity.

## Q4: Neural network building blocks & how the GP learns

Each concept maps to my Gaussian Process workflow. **Inputs:** each query point is a training example — the model learns the function landscape from accumulated input-output pairs across rounds. **Loss:** Expected Improvement acts as my objective function, quantifying the expected gain to guide where to query next. **Activations:** the GP posterior mean and variance represent the model's current understanding at each point in the domain. **Weight updates:** each new observation updates the kernel hyperparameters (length scales, noise level), similar to how gradient descent updates network weights. Over successive rounds, the GP learns structural patterns — such as which dimensions most influence the output — that direct future queries.

## Q5: PyTorch vs TensorFlow — rapid prototyping vs production-ready?

My approach is firmly on the rapid prototyping side, closer to PyTorch's philosophy. I use a manually-edited configuration dictionary for per-function strategy, and the GP model is rebuilt from scratch each round with no automated pipeline. This flexibility was essential: I could pivot a function from tight exploitation to full-domain exploration between rounds, or completely restructure a strategy when new observations revealed unexpected patterns. A production-ready pipeline with automated strategy selection and model ensembles would be more robust but too rigid for a setting where each round's strategy depends on the previous round's results. Like PyTorch's eager execution enabling fast experimentation, prototyping agility matters more than scalability here.

## Q6: Deep learning in sport & benchmarking success

Liotta's work on deep learning in sport shows that success metrics must be domain-specific — a model is not useful just because it achieves low loss; it must improve real-world outcomes. This reframes how I benchmark my capstone. Rather than only tracking whether a function's value improved, I consider which strategies work for which function types, whether the surrogate model is well-specified for peaked versus smooth landscapes, and whether my adaptation process is systematic. Like sports analytics where context matters alongside raw performance metrics, the real benchmark is whether my strategy evolution is evidence-driven and responsive to what the data reveals each round, not just the final output values.
