# Results Tracking

## Best Values Per Function (after 5 rounds)

| Func | Dim | Initial Best | Current Best | Best Round | Improvement |
|------|-----|-------------|-------------|------------|-------------|
| F1   | 2D  | 7.71e-16    | 7.71e-16    | initial    | none        |
| F2   | 2D  | 0.611205    | 0.611205    | initial    | none        |
| F3   | 3D  | -0.034835   | -0.009024   | round 1    | +0.025811   |
| F4   | 4D  | -4.025542   | 0.326836    | round 4    | +4.352378   |
| F5   | 4D  | 1088.860    | 5232.441    | round 5    | +4143.581   |
| F6   | 5D  | -0.714265   | -0.173337   | round 1    | +0.540928   |
| F7   | 6D  | 1.364968    | 1.650970    | round 5    | +0.286002   |
| F8   | 8D  | 9.598482    | 9.904530    | round 1    | +0.306048   |

## Round-by-Round Outputs

Values in **bold** = new best for that function at the time.

### Round 1
| Func | Submitted Point                                    | Output         | Status    |
|------|----------------------------------------------------|----------------|-----------|
| F1   | [0.637, 0.270]                                     | -3.76e-49      | IN BETWEEN |
| F2   | [0.775, 0.935]                                     | 0.150452       | IN BETWEEN |
| F3   | [0.362, 0.330, 0.464]                              | **-0.009024**  | NEW MAX   |
| F4   | [0.407, 0.414, 0.378, 0.455]                       | **-0.227587**  | NEW MAX   |
| F5   | [0.335, 0.767, 0.902, 0.952]                       | **1328.940**   | NEW MAX   |
| F6   | [0.437, 0.384, 0.555, 0.797, 0.137]               | **-0.173337**  | NEW MAX   |
| F7   | [0.181, 0.562, 0.263, 0.092, 0.351, 0.758]        | 1.055929       | IN BETWEEN |
| F8   | [0.025, 0.258, 0.057, 0.319, 0.819, 0.337, 0.182, 0.547] | **9.904530** | NEW MAX |

### Round 2
| Func | Submitted Point                                    | Output         | Status    |
|------|----------------------------------------------------|----------------|-----------|
| F1   | [0.604, 0.276]                                     | 8.24e-39       | no improvement |
| F2   | [0.621, 0.252]                                     | 0.008613       | no improvement |
| F3   | [0.438, 0.186, 0.443]                              | -0.033427      | no improvement |
| F4   | [0.441, 0.396, 0.336, 0.466]                       | -0.742634      | no improvement |
| F5   | [0.432, 0.768, 0.890, 0.993]                       | **1608.097**   | NEW MAX   |
| F6   | [0.216, 0.310, 0.411, 0.872, 0.036]               | -0.611858      | no improvement |
| F7   | [0.113, 0.358, 0.150, 0.147, 0.363, 0.821]        | **1.477402**   | NEW MAX   |
| F8   | [0.043, 0.338, 0.083, 0.141, 0.395, 0.783, 0.035, 0.338] | 9.727961 | no improvement |

### Round 3
| Func | Submitted Point                                    | Output         | Status    |
|------|----------------------------------------------------|----------------|-----------|
| F1   | [0.604, 0.276]                                     | 8.24e-39       | no improvement |
| F2   | [0.621, 0.265]                                     | 0.243274       | no improvement |
| F3   | [0.438, 0.186, 0.443]                              | -0.043132      | no improvement |
| F4   | [0.447, 0.418, 0.338, 0.466]                       | -0.651324      | no improvement |
| F5   | [0.432, 0.768, 0.890, 0.993]                       | **1609.836**   | NEW MAX   |
| F6   | [0.216, 0.310, 0.411, 0.872, 0.036]               | -0.735145      | no improvement |
| F7   | [0.113, 0.378, 0.185, 0.147, 0.384, 0.821]        | 1.404471       | no improvement |
| F8   | [0.057, 0.336, 0.006, 0.327, 0.306, 0.865, 0.060, 0.377] | 9.584803 | no improvement |

### Round 4
| Func | Submitted Point                                    | Output         | Status    |
|------|----------------------------------------------------|----------------|-----------|
| F1   | [0.731, 0.733]                                     | 7.66e-16       | no improvement (initial: 7.71e-16) |
| F2   | [0.656, 1.000]                                     | 0.557494       | no improvement |
| F3   | [0.311, 0.400, 0.429]                              | -0.023862      | no improvement |
| F4   | [0.395, 0.438, 0.401, 0.420]                       | **0.326836**   | NEW MAX   |
| F5   | [0.596, 0.955, 0.996, 0.989]                       | **4120.760**   | NEW MAX   |
| F6   | [0.433, 0.332, 0.627, 0.846, 0.202]               | -0.279341      | no improvement |
| F7   | [0.010, 0.388, 0.184, 0.150, 0.336, 0.763]        | **1.533311**   | NEW MAX   |
| F8   | [0.002, 0.219, 0.144, 0.008, 0.751, 0.463, 0.041, 0.900] | 9.893238 | no improvement |

### Round 5
| Func | Submitted Point                                    | Output         | Status    |
|------|----------------------------------------------------|----------------|-----------|
| F1   | [0.736, 0.738]                                     | 1.18e-17       | no improvement |
| F2   | [0.667, 0.914]                                     | 0.491615       | no improvement |
| F3   | [0.345, 0.279, 0.505]                              | -0.027207      | no improvement |
| F4   | [0.388, 0.453, 0.419, 0.404]                       | -0.172172      | no improvement |
| F5   | [0.676, 0.999999, 0.999999, 0.999999]              | **5232.441**   | NEW MAX   |
| F6   | [0.434, 0.394, 0.633, 0.684, 0.084]               | -0.208775      | no improvement |
| F7   | [0.000, 0.319, 0.161, 0.185, 0.336, 0.804]        | **1.650970**   | NEW MAX   |
| F8   | [0.046, 0.003, 0.046, 0.072, 0.979, 0.469, 0.024, 0.233] | 9.853045 | no improvement |

## Observations

### After 5 rounds (8 remaining)

- **Round 5: 2 new bests** (F5, F7). Consistent improvement on these two functions.
- **F5 jumped again** (4121→5232). Point [0.676, 0.999999, 0.999999, 0.999999] confirms dims 2-4 want to be maxed. Dim 1 trending up (0.335→0.432→0.596→0.676). Continue pushing dim 1 higher.
- **F7 continues climbing** (1.533→1.651). Point [0.0, 0.319, 0.161, 0.185, 0.336, 0.804] — dim 1 went to 0.0 (was 0.010 in R4). Dim 6 near 0.8. Exploit further.
- **F1 went backwards** — R5 [0.736, 0.738] got 1.18e-17, much worse than R4's 7.66e-16 at [0.731, 0.733]. Peak is extremely sharp. Need sub-0.003 radius around original best [0.731024, 0.733000].
- **F2 still stuck** — 0.492 at [0.667, 0.914], worse than initial 0.611 at [0.703, 0.927]. Tighter search near initial best needed.
- **F3 not improving** — broader exploration (R5) got -0.027, worse than R1's -0.009. Back to tight exploitation.
- **F4 regressed** — R5 nearby [0.388, 0.453] got -0.172 vs R4 best +0.327 at [0.395, 0.438]. Very narrow optimum — tighter radius needed.
- **F6 stalled** — broader exploration got -0.209 vs R1 best -0.173. Neither exploitation nor exploration working. Try multi-start.
- **F8 close but no cigar** — 9.853 vs best 9.905. Stick to tight exploitation around R1 best.

### Historical pattern
- F5: Improving every round (1089→1329→1608→1610→4121→5232). Dims 2-4 maxed, dim 1 trending up.
- F7: Steady improvement (1.365→1.477→1.533→1.651). Exploitation working well.
- F4: Breakthrough in R4 (+0.327) but R5 regressed. Very narrow optimum.
- F1, F2: Never beaten initial best in 5 rounds. Extremely peaked functions.
- F3, F6: Best in round 1, never improved despite 4 rounds of different strategies.
- F8: Best in round 1, close attempts but never surpassed.
