# BrainMed — descriptive results and measurement limitations

Documentation revision: 20 October 2026. Recomputed from stored summaries; **no new inference, clinical evaluation or independent replication**.

## One-page interpretation

| Historical condition | Macro6 (%) | Difference vs base (points) |
| --- | --- | --- |
| Medical base | 58.79 | +0.00 |
| SFT epoch 3 | 57.35 | -1.45 |
| Interpolation alpha=0.3 — sweep | 58.90 | +0.11 |
| Same-path final evaluation | 59.23 | +0.43 |

The historical SFT regresses relative to the already adapted medical base. Interpolation recovers much of that loss, but selection on these same tasks and the sweep/final discrepancy prevent a robust superiority claim. The research priority is reliability of measurement and negative transfer.

Macro6 equally weights MedBullets op4/op5, MedXpertQA, MedQA-4opt, MedMCQA and PubMedQA. All deltas are computed before rounding. Two decimal places are a display convention, not a confidence interval.

## Every archived run

| Run | Tasks | Macro6 (%) | Delta vs base | Five-family mean (%) |
| --- | --- | --- | --- | --- |
| base-HuatuoGPT-o1-8B | 10 | 58.79 | +0.00 | 59.12 |
| brainmed-8b-final | 10 | 59.23 | +0.43 | 59.38 |
| brainmed-8b-v1 | 10 | 55.91 | -2.89 | 56.38 |
| brainmed-8b-v1__best | 6 | 55.91 | -2.89 | 56.38 |
| brainmed-8b-v1__epoch-1 | 6 | 54.88 | -3.91 | 55.30 |
| brainmed-8b-v1__epoch-2 | 6 | 55.91 | -2.89 | 56.38 |
| brainmed-8b-v1__epoch-3 | 6 | 57.35 | -1.45 | 57.26 |
| brainmed-8b-v1__last | 6 | 57.35 | -1.45 | 57.26 |
| brainmed-8b-v1__soup-a0.15 | 6 | 58.23 | -0.57 | 58.77 |
| brainmed-8b-v1__soup-a0.3 | 6 | 58.26 | -0.54 | 58.48 |
| brainmed-8b-v1__soup-last-a0.3 | 6 | 58.90 | +0.11 | 59.19 |
| brainmed-8b-v1__soup-last-a0.5 | 6 | 58.73 | -0.06 | 59.15 |
| brainmed-8b-v1__soup-last-a0.7 | 6 | 58.90 | +0.11 | 58.96 |

The five-family sensitivity first averages the two MedBullets variants, then averages that value with the four remaining tasks. It does not remove training exposure or establish independent cases. Identical summary aliases are not independent training repetitions.

## Complete historical interpolation grid

| Candidate | SFT endpoint (naming convention) | Alpha | Macro6 (%) | Delta vs base |
| --- | --- | --- | --- | --- |
| brainmed-8b-v1__soup-a0.15 | best / epoch 2 | 0.15 | 58.23 | -0.57 |
| brainmed-8b-v1__soup-a0.3 | best / epoch 2 | 0.3 | 58.26 | -0.54 |
| brainmed-8b-v1__soup-last-a0.3 | last / epoch 3 | 0.3 | 58.90 | +0.11 |
| brainmed-8b-v1__soup-last-a0.5 | last / epoch 3 | 0.5 | 58.73 | -0.06 |
| brainmed-8b-v1__soup-last-a0.7 | last / epoch 3 | 0.7 | 58.90 | +0.11 |

These are sweep scores, not replaced by the later final re-evaluation. Three of the five historical interpolations are below the measured base. The last-checkpoint alpha=0.3 and alpha=0.7 candidates both display 58.90%; their tiny difference from rounded task inputs cannot justify a unique optimum. The grid and checkpoint selection reused the reported tasks.

## Sweep versus final re-evaluation

Recorded model paths: `./ckpts/brainmed-8b-v1/soup-last-a0.3` and `./ckpts/brainmed-8b-v1/soup-last-a0.3`. Matching paths do not establish matching weight hashes.

| Changed task | Sweep n | Final n | Sweep (%) | Final (%) | Inferred net correct difference |
| --- | --- | --- | --- | --- | --- |
| MedBullets op5 | 308 | 308 | 52.92 | 54.87 | 6 |

Macro6 re-evaluation difference: **+0.33 points**. For the historical files this is +0.33 points, versus +0.11 for the sweep candidate over the base and +0.43 for the final over the base. The apparent gain is therefore of the same order as the discrepancy between evaluations at the same path. Six net correct answers on MB-op5 are compatible with the rounded scores; the number of changed outputs and the cause require both prediction files.

## All tasks, denominators and negative results

| Task | base-HuatuoGPT-o1-8B | brainmed-8b-v1__epoch-3 | brainmed-8b-v1__soup-last-a0.3 | brainmed-8b-final | Final − base (points) |
| --- | --- | --- | --- | --- | --- |
| GPQA medical | 49.74 / n=390 | not evaluated | not evaluated | 59.74 / n=390 | +10.00 |
| HLE medical | 11.65 / n=103 | not evaluated | not evaluated | 10.68 / n=103 | -0.97 |
| MedBullets op4 | 59.09 / n=308 | 58.77 / n=308 | 62.01 / n=308 | 62.01 / n=308 | +2.92 |
| MedBullets op5 | 55.19 / n=308 | 56.82 / n=308 | 52.92 / n=308 | 54.87 / n=308 | -0.32 |
| MedMCQA | 63.30 / n=4183 | 61.20 / n=4183 | 64.07 / n=4183 | 64.07 / n=4183 | +0.77 |
| MedQA-4opt | 77.93 / n=1273 | 72.11 / n=1273 | 76.67 / n=1273 | 76.67 / n=1273 | -1.26 |
| MedQA-5opt | 72.82 / n=1273 | not evaluated | not evaluated | 73.68 / n=1273 | +0.86 |
| MedXpertQA | 17.05 / n=1449 | 18.08 / n=1449 | 18.63 / n=1449 | 18.63 / n=1449 | +1.58 |
| MMLU-Pro medical | 64.56 / n=1535 | not evaluated | not evaluated | 65.73 / n=1535 | +1.17 |
| PubMedQA | 80.20 / n=1000 | 77.10 / n=1000 | 79.10 / n=1000 | 79.10 / n=1000 | -1.10 |

The full final bundle contains 11,822 task rows, not independent patients. Missing tasks for the quick sweep are not zero scores.

## Measured base versus published protocol

| Task | Published (%) | Measured base (%) | Gap (points) |
| --- | --- | --- | --- |
| MedBullets op4 | 55.20 | 59.09 | +3.89 |
| MedBullets op5 | 51.30 | 55.19 | +3.89 |
| MedXpertQA | 16.70 | 17.05 | +0.35 |
| MedQA-4opt | 72.60 | 77.93 | +5.33 |
| MedMCQA | 60.40 | 63.30 | +2.90 |
| PubMedQA | 79.20 | 80.20 | +1.00 |

Mean task-wise gap: **+2.89 points**; largest absolute gap: **5.33 points**. Published values are transcribed in `eval/baselines.json`, not rerun. This is a protocol discrepancy, not a causal estimate of one scorer effect or a correction factor transferable to other models.

## Overlap-filtered subsets and format diagnostics

Historical summaries record that overlapping training rows were retained. `accuracy_clean` excludes flagged evaluation rows only; it is not proof of decontaminated training or an unbiased final test.

| Run | Task | n | Flagged rows | Raw (%) | Filtered (%) | Strict-format (%) | Empty |
| --- | --- | --- | --- | --- | --- | --- | --- |
| base-HuatuoGPT-o1-8B | GPQA medical | 390 | 0 | 49.74 | 49.74 | 98.21 | 0 |
| base-HuatuoGPT-o1-8B | HLE medical | 103 | 30 | 11.65 | 8.22 | 96.12 | 0 |
| base-HuatuoGPT-o1-8B | MedBullets op4 | 308 | 35 | 59.09 | 58.97 | 100.00 | 0 |
| base-HuatuoGPT-o1-8B | MedBullets op5 | 308 | 35 | 55.19 | 53.48 | 99.68 | 0 |
| base-HuatuoGPT-o1-8B | MedMCQA | 4183 | 0 | 63.30 | 63.30 | 99.81 | 0 |
| base-HuatuoGPT-o1-8B | MedQA-4opt | 1273 | 1 | 77.93 | 77.99 | 99.84 | 0 |
| base-HuatuoGPT-o1-8B | MedQA-5opt | 1273 | 1 | 72.82 | 72.88 | 99.76 | 0 |
| base-HuatuoGPT-o1-8B | MedXpertQA | 1449 | 15 | 17.05 | 16.88 | 96.27 | 0 |
| base-HuatuoGPT-o1-8B | MMLU-Pro medical | 1535 | 340 | 64.56 | 64.52 | 99.15 | 0 |
| base-HuatuoGPT-o1-8B | PubMedQA | 1000 | 0 | 80.20 | 80.20 | 100.00 | 0 |
| brainmed-8b-final | GPQA medical | 390 | 0 | 59.74 | 59.74 | 98.46 | 0 |
| brainmed-8b-final | HLE medical | 103 | 30 | 10.68 | 6.85 | 97.09 | 0 |
| brainmed-8b-final | MedBullets op4 | 308 | 35 | 62.01 | 62.64 | 99.68 | 0 |
| brainmed-8b-final | MedBullets op5 | 308 | 35 | 54.87 | 54.21 | 99.35 | 0 |
| brainmed-8b-final | MedMCQA | 4183 | 0 | 64.07 | 64.07 | 99.83 | 0 |
| brainmed-8b-final | MedQA-4opt | 1273 | 1 | 76.67 | 76.73 | 99.14 | 0 |
| brainmed-8b-final | MedQA-5opt | 1273 | 1 | 73.68 | 73.66 | 98.90 | 0 |
| brainmed-8b-final | MedXpertQA | 1449 | 15 | 18.63 | 18.34 | 99.24 | 0 |
| brainmed-8b-final | MMLU-Pro medical | 1535 | 340 | 65.73 | 65.44 | 99.48 | 0 |
| brainmed-8b-final | PubMedQA | 1000 | 0 | 79.10 | 79.10 | 99.90 | 0 |

Strict-format compliance measures extraction format, not clinical correctness.

## Statistical interpretation and missing evidence

The archived [SIGNIFICANCE.md](SIGNIFICANCE.md) reports pooled discordant counts 651/681 and p=0.4269 for the **sweep candidate**, not the final. It uses head-answer scoring and deduplicates by question text (298 MedBullets questions versus 308 rows in summaries). The nonsignificant result does not prove equivalence. Pooled tasks are dependent; candidate selection and multiplicity remain unresolved.

Recover per-question outputs, case-family IDs, hashes and training logs before testing significance, F1, calibration or clinical justification. See [the evidence plan](../docs/RESEARCH_PLAN.md).

## Input provenance

Every input below is unchanged by this generator. Hashes identify bytes; they do not independently validate the original experiment.

| Run | Summary | SHA256 |
| --- | --- | --- |
| base-HuatuoGPT-o1-8B | [JSON](summary_base-HuatuoGPT-o1-8B.json) | 0867b46a069716812277b62e9c4fbaf379991df2b554db586d62be80aafbd69a |
| brainmed-8b-final | [JSON](summary_brainmed-8b-final.json) | 9de88d8ee8b4623575fa1ee79ded51f1286d83dea5390786240fa3d2cc8b7aa6 |
| brainmed-8b-v1 | [JSON](summary_brainmed-8b-v1.json) | 3bba798ed4750f591f38565cecf383f21cf9756085d1c5fc0db4758c7b25b275 |
| brainmed-8b-v1__best | [JSON](summary_brainmed-8b-v1__best.json) | 49ea94f8343651786cef0508b01f07988030903101e02ced8b3c973f601adf4a |
| brainmed-8b-v1__epoch-1 | [JSON](summary_brainmed-8b-v1__epoch-1.json) | ed9b6b5c65b6cd1433eaded099f0bad19e3d548e5577c7bb2c5595b07e199e7f |
| brainmed-8b-v1__epoch-2 | [JSON](summary_brainmed-8b-v1__epoch-2.json) | 8c29d957cf61039431986cc42b3f44447871253e3e09c84deb2adbd3c67d17a3 |
| brainmed-8b-v1__epoch-3 | [JSON](summary_brainmed-8b-v1__epoch-3.json) | f36647590de8d46e78d80f47182ac10c82efac1763c624fa67bff0b54d7d898e |
| brainmed-8b-v1__last | [JSON](summary_brainmed-8b-v1__last.json) | 8e43ad131948fe5cd98f10f28953ced4e2ff24ec1371d2a519248749bdc1f45d |
| brainmed-8b-v1__soup-a0.15 | [JSON](summary_brainmed-8b-v1__soup-a0.15.json) | faba9d56aad39f5accba86fef4475d65697132ca9859a8af25590e783bab4be8 |
| brainmed-8b-v1__soup-a0.3 | [JSON](summary_brainmed-8b-v1__soup-a0.3.json) | bc38615872419256baae0433ccca0d322361a249a0195fc2aeff2c9f41aa1a00 |
| brainmed-8b-v1__soup-last-a0.3 | [JSON](summary_brainmed-8b-v1__soup-last-a0.3.json) | 4e8f69f7f9d2bd4ddc9675a38f07d80b032d79248601bcc52e225ad89e46d197 |
| brainmed-8b-v1__soup-last-a0.5 | [JSON](summary_brainmed-8b-v1__soup-last-a0.5.json) | 30d4b02db47e58601af0c17b0946f2316177891617689a765619bc80d695d394 |
| brainmed-8b-v1__soup-last-a0.7 | [JSON](summary_brainmed-8b-v1__soup-last-a0.7.json) | 42dababc2bcb6317c888c97de7f009b840408fd6f9b63926d85a7e6e1327c08c |
