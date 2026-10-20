# Paired significance: `brainmed-8b-v1__soup-last-a0.3` vs `base-HuatuoGPT-o1-8B`

McNemar's exact test on the items both runs answered. `only B` counts items the
candidate gets right and the baseline gets wrong; `only A` the reverse. Items both
get right or both get wrong are uninformative about which model is better.

| Benchmark | n | base-HuatuoGPT-o1-8B | brainmed-8b-v1__soup-last-a0.3 | Delta | only A | only B | p | verdict (a=0.05) |
|---|---|---|---|---|---|---|---|---|
| MB-op4 | 298 | 59.73 | 62.42 | +2.68 | 30 | 38 | 0.396 | not rejected |
| MB-op5 | 298 | 55.37 | 53.36 | -2.01 | 37 | 31 | 0.545 | not rejected |
| MedMCQA | 4183 | 63.28 | 64.04 | +0.77 | 358 | 390 | 0.257 | not rejected |
| MedQA | 1273 | 77.93 | 76.59 | -1.34 | 103 | 86 | 0.244 | not rejected |
| MedXpert | 1449 | 16.98 | 18.63 | +1.66 | 93 | 117 | 0.112 | not rejected |
| PubMedQA | 1000 | 80.2 | 79.1 | -1.10 | 30 | 19 | 0.152 | not rejected |

## Pooled across benchmarks

- items only `base-HuatuoGPT-o1-8B` gets right: **651**
- items only `brainmed-8b-v1__soup-last-a0.3` gets right: **681**
- McNemar exact p = **0.4269**

The archived pooled test does not reject its null hypothesis (p = 0.427).
This does not establish equivalence, absence of a meaningful effect, or that all
observed differences are sampling noise. This comparison concerns the sweep
candidate, not `brainmed-8b-final`.

Per benchmark: no nominal rejection at 0.05 in any of the six comparisons.
Candidate selection, multiplicity and case-family dependence are not resolved.

Pooling treats benchmarks as one sample and so weights them by size; read it
alongside the per-benchmark rows, not instead of them.

Documentation correction, 20 October 2026: the counts and p-values above are
preserved from the historical artifact. Per-question logs are not committed,
so the paired observations have not been independently reconstructed. The
historical script uses head answers and question-text keys; duplicate text
collapses, explaining why denominators differ from the task-row summaries.
This is not the same estimand as the Macro6 `max(head, tail)` accuracy.
