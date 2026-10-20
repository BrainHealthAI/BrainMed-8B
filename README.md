# BrainMed-8B — medical-model adaptation and evaluation research

Documentation reviewed on **20 October 2026**. This revision aligns the research claims
with the archived evidence while preserving the original code, authorship and historical
result files. It is not a new training run.

## Research summary

1. **Continued supervised fine-tuning regressed on the historical six-task mean.**
   The measured HuatuoGPT-o1-8B base scores 58.79%, versus 57.35% for epoch 3.
2. **Interpolation largely recovers the base level; a robust improvement is not established.**
   The selected sweep candidate scores 58.90%. Its later `final` evaluation scores
   59.23%, with the difference confined to one task. Selection used the reported
   evaluation tasks rather than an independent final test.
3. **The useful research question is measurement reliability and negative transfer.**
   Scoring, task weighting, repeated evaluation, previous data exposure and
   checkpoint selection must be disentangled before attributing a gain to training.

These are medical question-answering results, not patient diagnostic accuracy,
validated clinical reasoning, or calibrated probabilities. No new F1, clinical
evaluation or model inference was performed for this documentation revision.

### Recomputed historical results

Macro6 is the unweighted mean of MedBullets op4/op5, MedXpertQA, MedQA-4opt,
MedMCQA and PubMedQA. Scores and differences below are computed from the stored
two-decimal task scores, then rounded once for display. They are descriptive.

<!-- research-summary:start -->
| Historical condition | Macro6 (%) | Difference vs base (points) |
| --- | --- | --- |
| Medical base | 58.79 | +0.00 |
| SFT epoch 3 | 57.35 | -1.45 |
| Interpolation alpha=0.3 — sweep | 58.90 | +0.11 |
| Same-path final evaluation | 59.23 | +0.43 |
<!-- research-summary:end -->

The complete five-interpolation grid, every archived run, all ten task results,
re-evaluation discrepancy and published-protocol offset are in
[the reproducible results report](results/REPORT.md). No cross-paper ranking is
used as evidence that BrainMed outperforms other models.

## Model and data lineage

`Llama-3.1` is the underlying architecture family. The directly adapted checkpoint
is [FreedomIntelligence/HuatuoGPT-o1-8B](https://huggingface.co/FreedomIntelligence/HuatuoGPT-o1-8B),
already medically adapted through SFT and reinforcement learning.
**BrainMed-8B-SFT** names the project's continued full-parameter SFT derivative;
**BrainMed-8B** names its interpolation with that medical base. They are not new
foundation-model architectures.

The historical corpus is reported as **44,351 training traces and 923 validation
rows**, combining [MedReason](https://huggingface.co/datasets/UCSC-VLAA/MedReason)
and [medical-o1-reasoning-SFT](https://huggingface.co/datasets/FreedomIntelligence/medical-o1-reasoning-SFT)
through [MedReason-MedO1-Reasoning-46K](https://huggingface.co/datasets/Williamsanderson/MedReason-MedO1-Reasoning-46K).
The source identity is known; the exact historical prepared-data manifest and
row-level revision mapping are not committed here. Those are different claims.

Huatuo's own [training documentation](https://github.com/FreedomIntelligence/HuatuoGPT-o1)
identifies medical-o1 as part of its training pipeline. Re-exposure to this source,
and SFT after RL, are plausible explanations for negative transfer. The fraction
of identical rows seen by the exact base checkpoint and their causal contribution
have **not** been established by a controlled ablation.

[Data preparation](data/prepare_data.py) checks preservation of question/reasoning
text and can append an answer-format suffix. This is a transformation check, not
physician validation of the traces. Overlap scanning and removal are separate:
removal requires `--decontaminate`, and the historical summaries explicitly record
`training_kept_contaminated_rows: true`.

### Historical configuration and remaining provenance gaps

| Component | Recorded recipe / evidence |
|---|---|
| Adaptation | Full-parameter SFT; not LoRA |
| Base | HuatuoGPT-o1-8B; exact loaded weights/tokenizer hashes still needed |
| Context / schedule | 4,096 tokens, 3 epochs, learning rate 5e-6 |
| Effective batch | 128 (4 × 8 accumulation × 4 GPUs), reported recipe |
| Infrastructure | BF16, DeepSpeed ZeRO-3, reported 4 × H100 80 GB |
| Optimizer steps | Historical README: 1,038; research dossier: 1,041. Unresolved without `run_summary.json` / optimizer logs |
| Checkpoint selection | Lowest validation loss identified epoch 2; later selection also inspected evaluation scores |
| Interpolation | `theta = (1-alpha)*base + alpha*SFT`; alpha 0.3 selected historically |

Shared ancestry alone does not prove a flat loss basin, robustness or a
beneficial interpolation path. [WiSE-FT](https://arxiv.org/abs/2109.01903) supplies
methodological context, not evidence of a new contribution or clinical benefit here.

## Limitations

- **Test reuse and multiplicity:** epochs and five interpolation configurations
  were evaluated on the same tasks. The selected score is exploratory.
- **Repeatability:** sweep and final reference the same local model path but have
  different scores. A path is not a weight hash; neither identity nor the cause
  of the discrepancy can be settled from aggregates.
- **Scoring:** [the scorer](eval/scorer.py) reports the larger of aggregate
  head/tail accuracy and has option-text/fuzzy fallbacks. The historical
  significance script uses head answers and keys records by question text,
  collapsing duplicates. It is not the same endpoint as Macro6.
- **Dependence:** the 11,822 task rows are not 11,822 independent patients or
  unique cases. MedBullets and MedQA variants need family-level handling.
- **Exposure:** flagged training/evaluation overlap was retained. A filtered
  evaluation subset cannot undo previous training exposure, unknown base
  exposure or selection on the evaluation tasks.
- **Cross-paper comparisons:** the measured base differs from its published
  task values by +2.89 points on average, up to +5.33 on MedQA. This descriptive
  protocol gap is not a universal correction factor.
- **Missing evidence:** raw per-question predictions, checkpoint hashes, exact
  prepared-data manifest, complete training logs and independent repeats are
  required. The historical p-value does not prove equivalence or that an
  observed difference is only noise.
- **Clinical scope:** QCM answer accuracy does not establish sound justification,
  F1 by diagnosis, safety, calibration or performance on the application's
  structured diagnostic JSON and ICD-10 task.

## Two separate research directions

**Near term — measurement and negative results.** Recover archived predictions,
reconcile repeated evaluations of the same candidate, compare frozen extraction
rules and case-family weighting on those outputs, then test an independently
selected candidate on untouched cases. The primary question is whether an
improvement over the **medical base** survives those controls. Recovery relative
to a regressed SFT checkpoint alone is not a novel finding.

**Medium term — paired EN/FR/darija and evidence-grounded hypotheses.** Build
traceable case families, obtain independent medical annotation, and evaluate
diagnostic claims plus the source passages that support each argument. This is
a separate study, not a result already delivered by the current pipeline.

See the [evidence recovery and publication checklist](docs/RESEARCH_PLAN.md).
The related [HELIX training repository](https://github.com/BrainHealthAI/BRAIN-train/tree/Training_v2)
and [consultation application](https://github.com/zadbox/helix-brain-health)
have distinct model lineages and evaluation tasks; their scores must not be pooled.

## Reproduce the documentation without a GPU

Python 3.10+ standard library only; no network calls, model download or upload:

```bash
python scripts/make_report.py
python scripts/make_report.py --check
python -m unittest discover -s tests -v
```

The generator reads both committed flat summaries and the pipeline's nested
summary layout. Conflicting copies of a run fail explicitly. It preserves the
input JSON and updates `results/REPORT.md` plus the bounded summary above.

## Training and inference tooling

The original pipeline is preserved for reproducibility:

```text
data/prepare_data.py       corpus checks, overlap scan, optional removal, output manifest
eval/build_benchmarks.py   task bundle and hashes
eval/eval.py, scorer.py    historical inference and scoring
train/sft.py               SFT, per-source validation and checkpoint summaries
scripts/weight_soup.py     weight interpolation
scripts/sweep_candidates.sh exploratory evaluation of multiple candidates
scripts/significance.py   historical head-answer paired-count analysis
```

GPU execution requires the original model/data access, pinned dependencies and
run configuration. `scripts/run_pipeline.sh` includes training and Hugging Face
publication stages: inspect its stages and destination before use. It is **not**
the command for the CPU-only verification above.

The weight repositories remain [BrainHealthAI/BrainMed-8B](https://huggingface.co/BrainHealthAI/BrainMed-8B)
and [BrainHealthAI/BrainMed-8B-SFT](https://huggingface.co/BrainHealthAI/BrainMed-8B-SFT).
This GitHub documentation update does not change their cards, weights or live
deployments. Legacy comparison figures are [archived with a status notice](results/figures/README.md)
and are not the current research summary.

## Attribution and license

Original project: [BrainHealthAI/BrainMed-8B](https://github.com/BrainHealthAI/BrainMed-8B),
historical evidence revision
[`133424d`](https://github.com/BrainHealthAI/BrainMed-8B/tree/133424da08a4f14d426890a8e36f532eaaf693d2).
The 20 October 2026 documentation revision was prepared in [zadbox/BrainMed-8B](https://github.com/zadbox/BrainMed-8B) and merged here.

```bibtex
@software{brainmed8b2026,
  title = {BrainMed-8B: medical reasoning adaptation and evaluation pipeline},
  author = {BrainResearch},
  year = {2026},
  url = {https://github.com/BrainHealthAI/BrainMed-8B}
}
```

[Apache-2.0](LICENSE) applies to this repository; upstream model and dataset terms
must also be checked. Research artifact only; no clinical validation is claimed.
