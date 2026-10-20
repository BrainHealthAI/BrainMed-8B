# Evidence recovery and research plan

Updated 20 October 2026. Tasks below are prospective unless explicitly marked
as supported by committed artifacts. They do not report new model runs.

## Evidence ledger

| Question | Current evidence | Missing artifact / decision |
|---|---|---|
| Did SFT improve the medical base? | Stored scores show a lower Macro6 at epoch 3 | Replicates, fixed independent test, source ablations |
| Did interpolation improve the base? | Five configurations; sweep +0.11 pt, final +0.43 pt | Raw outputs, immutable weights and a test not used for selection |
| Why do sweep and final differ? | Same path; MB-op5 52.92 → 54.87 on n=308 | Both output files, request order, server/runtime versions, hashes |
| Where did training data come from? | MedReason + medical-o1 identified in source documentation and preparation code | Historical corpus revision, row IDs, source mapping, split and token manifest |
| Were repeated-source data responsible for regression? | Prior medical-o1 use by Huatuo makes this plausible | Controlled source-specific ablations; not a proven causal mechanism |
| Were there 1,038 or 1,041 optimizer steps? | Two historical documents disagree | `run_summary.json`, checkpoint metadata and optimizer-step log |
| Can the published p=0.4269 be reconstructed? | Archived discordant counts 651/681 | Per-case outputs and family IDs; test concerns sweep, not final |
| Does a lower loss mean better reasoning? | Epoch selection and task ranking disagree | Clinician-scored justification quality and aligned evaluation |
| Is the application clinically reliable? | No application-task result in these artifacts | JSON/ICD-10, safety, calibration and evidence-link evaluation |

## Priority 1 — recover, do not regenerate history

Recover original artifacts from the run owner / retained RunPod storage / W&B
exports where available. Do not label newly generated outputs as historical.

- Each run's `results/<run>/logs/<run>__<task>.json`, including invalid and empty outputs.
- Case IDs, source IDs, family IDs and frozen references; do not use question text
  as a unique identifier without checking duplicates.
- Model, tokenizer, adapters/interpolations and checkpoint SHA256 manifests.
- `run_summary.json`, complete optimizer-step/validation logs and actual launch command.
- Prepared train/validation/test manifests, source revisions, overlap matches
  and whether each flagged training row was actually removed.
- Inference engine/version, dependency lock, prompts, decoding, batch order,
  request failures, retries, termination reasons and hardware.

Hash files before analysis. Preserve originals and record transformations.
No private patient data or credentials should be committed to these public repositories.

## Priority 2 — a measurement and negative-transfer study

1. Define the case family and the primary endpoint before reanalysis.
2. Freeze a strict answer parser with invalid/abstention categories. Compare it
   with the historical `max(head, tail)` and fuzzy scoring on identical archived outputs.
3. Report all candidates and seeds. Keep selection and final testing separate.
4. Reconcile the two alpha=0.3 evaluations using hashes and paired predictions.
   Six net correct answers inferred from rounded rates are not proof that exactly
   six outputs changed; more errors may have swapped in both directions.
5. Evaluate weighting by row, task and family. The five-task-family sensitivity
   combines MedBullets op4/op5 first; it is not a decontamination procedure.
6. Use paired family-aware uncertainty intervals and prespecified multiplicity
   handling. A nonsignificant test is not proof of equivalence.
7. For a causal claim about re-exposure, control training budget, base checkpoint,
   source mixture and seed. Compare source-exclusive and combined conditions,
   including a no-update control. Do not infer source causality from one run.

The central question is whether adaptation produces a reproducible improvement
over the existing medical base under an independent measurement protocol.
Recovering a loss caused by additional SFT is a useful negative result, not
proof of novelty in weight interpolation.

## Priority 3 — a distinct multilingual evidence study

Build matched EN/FR/darija cases with populated `source_pair_id`, validated
translations, licensed provenance and separation by case family. Test lexical,
answer-length and class-majority baselines before interpreting a model score.
The reported 66% heuristic versus 55% Darija model comparison must not be
published as independently reproduced without code, outputs and a frozen dataset.

For every proposed diagnostic hypothesis, map each decisive argument to an
identified source passage, date, population and support/contradiction status.
No source or inadequate support should permit explicit abstention.

Measure retrieval coverage separately from citation correctness and diagnostic
correctness. Use two independent medical raters, adjudication, agreement, critical
error severity, omissions, calibration where probabilities exist, and performance
by language/specialty. Fix corpus versions; evaluate later updates separately.

## Metrics to report only when the inputs exist

| Metric | Required observations | Interpretation |
|---|---|---|
| Answer accuracy / pass@1 | One prespecified prediction and gold answer per case | Answer correctness, not reasoning fidelity |
| Per-class precision, recall, macro-F1 | Case-level labels and confusion counts | Class performance; no reconstruction from aggregate accuracy |
| Hypothesis / ICD-10 accuracy | Clinician reference and matching rules | Application-specific endpoint |
| Justification error rate | Independent medical annotation | Clinical validity and harmful omissions |
| Citation support and coverage | Claim–passage pairs and annotations | Valid link is not sufficient support |
| Brier / reliability curves | Predictive probabilities and outcomes | High/medium/low text labels alone are not probabilities |
| Risk–coverage | Prespecified abstention scores and outcomes | Quality of retained answers and unhandled cases |
| Paired uncertainty | Predictions, case families and seeds | Separate case uncertainty from training variability |

## Document alignment checklist

- Use the actual revision date, and identify historical experiment dates separately.
- Round task scores and derived descriptive means to two decimals; do not subtract
  already-rounded means. Preserve raw values in machine-readable sources.
- Cite original project ownership plus the maintained fork, not an unrelated account.
- Remove stale figure alt-text identifiers; link directly to the relevant artifact.
- Do not distribute a Word file alone if its source links require a sibling `Pieces/` directory.
- Open with three findings and a short summary; keep limitations grouped and explicit.
- Do not overwrite historical JSON to make it agree with narrative prose.

These checks apply to subsequent dossier revisions; this repository update does
not itself rewrite previously distributed Word/PDF files or external model cards.
