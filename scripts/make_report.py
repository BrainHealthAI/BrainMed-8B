"""Build descriptive research tables from saved summaries; never run inference."""

import argparse
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TABLE4 = ("medbullets_op4", "medbullets_op5", "medxpertqa",
          "medqa_4opt", "medmcqa_val", "pubmedqa_test")
BASE = "base-HuatuoGPT-o1-8B"
SFT = "brainmed-8b-v1__epoch-3"
SWEEP = "brainmed-8b-v1__soup-last-a0.3"
FINAL = "brainmed-8b-final"
MARKERS = ("<!-- research-summary:start -->", "<!-- research-summary:end -->")
SHORT = {
    "medqa_4opt": "MedQA-4opt", "medmcqa_val": "MedMCQA", "pubmedqa_test": "PubMedQA",
    "mmlu_pro_medical": "MMLU-Pro medical", "medbullets_op4": "MedBullets op4",
    "medbullets_op5": "MedBullets op5", "medxpertqa": "MedXpertQA",
    "hle_med": "HLE medical", "gpqa_medical": "GPQA medical", "medqa_5opt": "MedQA-5opt",
}


def number(value):
    result = Decimal(str(value))
    if not result.is_finite():
        raise ValueError("Non-finite numeric value")
    return result


def display(value, signed=False):
    if value is None:
        return "—"
    rounded = number(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return format(rounded, "+.2f" if signed else ".2f")


def mean(values):
    values = list(values)
    return sum(values, Decimal(0)) / len(values) if values else None


def macro6(run):
    benchmarks = run["benchmarks"]
    if not all(k in benchmarks for k in TABLE4):
        return None
    return mean(number(benchmarks[k]["accuracy"]) for k in TABLE4)


def family5(run):
    if macro6(run) is None:
        return None
    scores = [number(run["benchmarks"][k]["accuracy"]) for k in TABLE4]
    return mean([mean(scores[:2]), *scores[2:]])


def load_runs(directory):
    paths = sorted(set(directory.glob("summary_*.json")) |
                   set(directory.glob("*/summary_*.json")))
    runs, sources = {}, {}
    for path in paths:
        run = json.loads(path.read_text(encoding="utf-8"))
        name = run["run"]
        if not isinstance(name, str) or not name:
            raise ValueError(f"Invalid run ID: {path}")
        for task, result in run["benchmarks"].items():
            score = number(result["accuracy"])
            if not 0 <= score <= 100 or not isinstance(result["n"], int) or result["n"] <= 0:
                raise ValueError(f"Invalid result in {path}: {task}")
        if name in runs and runs[name] != run:
            raise ValueError(f"Conflicting summaries for run {name}: {sources[name]} and {path}")
        runs[name] = run
        sources.setdefault(name, []).append(path)
    if not runs:
        raise ValueError(f"No summary_*.json found under {directory}")
    return runs, sources


def table(headers, rows):
    def cell(value):
        return str(value).replace("|", r"\|").replace("\n", " ")
    lines = ["| " + " | ".join(headers) + " |",
             "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(cell(c) for c in row) + " |" for row in rows)
    return "\n".join(lines)


def summary_table(runs):
    base = macro6(runs[BASE]) if BASE in runs else None
    labels = {BASE: "Medical base", SFT: "SFT epoch 3",
              SWEEP: "Interpolation alpha=0.3 — sweep", FINAL: "Same-path final evaluation"}
    rows = []
    for name, label in labels.items():
        if name not in runs:
            continue
        score = macro6(runs[name])
        delta = score - base if score is not None and base is not None else None
        rows.append([label, display(score), display(delta, True)])
    return table(["Historical condition", "Macro6 (%)", "Difference vs base (points)"], rows)


def changed_tasks(a, b):
    return [(k, a["benchmarks"][k], b["benchmarks"][k])
            for k in sorted(a["benchmarks"].keys() & b["benchmarks"].keys())
            if a["benchmarks"][k]["accuracy"] != b["benchmarks"][k]["accuracy"]]


def inferred_correct(result):
    """Infer a count only when one integer uniquely matches the rounded percentage."""
    target = number(result["accuracy"])
    candidates = [k for k in range(result["n"] + 1)
                  if (100 * Decimal(k) / result["n"]).quantize(
                      Decimal("0.01"), rounding=ROUND_HALF_UP) == target]
    return candidates[0] if len(candidates) == 1 else None


def render_report(runs, sources, baselines, output):
    lines = [
        "# BrainMed — descriptive results and measurement limitations", "",
        "Documentation revision: 20 October 2026. Recomputed from stored summaries; "
        "**no new inference, clinical evaluation or independent replication**.", "",
        "## One-page interpretation", "",
        summary_table(runs), "",
        "The historical SFT regresses relative to the already adapted medical base. "
        "Interpolation recovers much of that loss, but selection on these same tasks "
        "and the sweep/final discrepancy prevent a robust superiority claim. The "
        "research priority is reliability of measurement and negative transfer.", "",
        "Macro6 equally weights MedBullets op4/op5, MedXpertQA, MedQA-4opt, MedMCQA "
        "and PubMedQA. All deltas are computed before rounding. Two decimal places "
        "are a display convention, not a confidence interval.", "",
        "## Every archived run", "",
    ]
    base = macro6(runs[BASE]) if BASE in runs else None
    rows = []
    for name, run in sorted(runs.items()):
        score = macro6(run)
        delta = score - base if score is not None and base is not None else None
        rows.append([name, len(run["benchmarks"]), display(score),
                     display(delta, True), display(family5(run))])
    lines += [table(["Run", "Tasks", "Macro6 (%)", "Delta vs base", "Five-family mean (%)"], rows), "",
              "The five-family sensitivity first averages the two MedBullets variants, "
              "then averages that value with the four remaining tasks. It does not "
              "remove training exposure or establish independent cases. Identical "
              "summary aliases are not independent training repetitions.", "",
              "## Complete historical interpolation grid", ""]
    rows = []
    for name, run in sorted(runs.items()):
        if "__soup" not in name:
            continue
        score = macro6(run)
        origin = "last / epoch 3" if "__soup-last-" in name else "best / epoch 2"
        alpha = name.rsplit("a", 1)[-1]
        rows.append([name, origin, alpha, display(score),
                     display(score - base, True) if score is not None and base is not None else "—"])
    lines += [table(["Candidate", "SFT endpoint (naming convention)", "Alpha", "Macro6 (%)", "Delta vs base"], rows), "",
              "These are sweep scores, not replaced by the later final re-evaluation. "
              "Three of the five historical interpolations are below the measured base. "
              "The last-checkpoint alpha=0.3 and alpha=0.7 candidates both display 58.90%; "
              "their tiny difference from rounded task inputs cannot justify a unique optimum. "
              "The grid and checkpoint selection reused the reported tasks.", ""]
    if SWEEP in runs and FINAL in runs:
        a, b = runs[SWEEP], runs[FINAL]
        lines += ["## Sweep versus final re-evaluation", "",
                  f"Recorded model paths: `{a.get('model')}` and `{b.get('model')}`. "
                  "Matching paths do not establish matching weight hashes.", ""]
        rows = []
        for task, left, right in changed_tasks(a, b):
            ca, cb = inferred_correct(left), inferred_correct(right)
            net = cb - ca if ca is not None and cb is not None and left["n"] == right["n"] else "not identifiable"
            rows.append([SHORT.get(task, task), left["n"], right["n"],
                         display(left["accuracy"]), display(right["accuracy"]), net])
        lines += [table(["Changed task", "Sweep n", "Final n", "Sweep (%)", "Final (%)",
                         "Inferred net correct difference"], rows), "",
                  f"Macro6 re-evaluation difference: **{display(macro6(b) - macro6(a), True)} points**. "
                  "For the historical files this is +0.33 points, versus +0.11 for the "
                  "sweep candidate over the base and +0.43 for the final over the base. "
                  "The apparent gain is therefore of the same order as the discrepancy "
                  "between evaluations at the same path. Six net correct answers on "
                  "MB-op5 are compatible with the rounded scores; the number of changed "
                  "outputs and the cause require both prediction files.", ""]
    lines += ["## All tasks, denominators and negative results", ""]
    selected = [n for n in (BASE, SFT, SWEEP, FINAL) if n in runs]
    tasks = sorted({k for run in runs.values() for k in run["benchmarks"]})
    rows = []
    for task in tasks:
        row = [SHORT.get(task, task)]
        for name in selected:
            result = runs[name]["benchmarks"].get(task)
            row.append(f"{display(result['accuracy'])} / n={result['n']}" if result else "not evaluated")
        if BASE in runs and FINAL in runs:
            bv = runs[BASE]["benchmarks"].get(task)
            fv = runs[FINAL]["benchmarks"].get(task)
            row.append(display(number(fv["accuracy"]) - number(bv["accuracy"]), True) if bv and fv else "—")
        rows.append(row)
    headers = ["Task"] + selected
    if BASE in runs and FINAL in runs:
        headers.append("Final − base (points)")
    lines += [table(headers, rows), "",
              "The full final bundle contains 11,822 task rows, not independent patients. "
              "Missing tasks for the quick sweep are not zero scores.", "",
              "## Measured base versus published protocol", ""]
    published = baselines["table4_sota_comparison"]["Huatuo-o1-RL-8B"]
    if BASE in runs:
        gaps, rows = [], []
        for task, value in zip(TABLE4, published[:6]):
            measured = number(runs[BASE]["benchmarks"][task]["accuracy"])
            gap = measured - number(value)
            gaps.append(gap)
            rows.append([SHORT[task], display(value), display(measured), display(gap, True)])
        lines += [table(["Task", "Published (%)", "Measured base (%)", "Gap (points)"], rows), "",
                  f"Mean task-wise gap: **{display(mean(gaps), True)} points**; largest "
                  f"absolute gap: **{display(max(abs(x) for x in gaps))} points**. "
                  "Published values are transcribed in `eval/baselines.json`, not rerun. "
                  "This is a protocol discrepancy, not a causal estimate of one scorer "
                  "effect or a correction factor transferable to other models.", ""]
    lines += ["## Overlap-filtered subsets and format diagnostics", "",
              "Historical summaries record that overlapping training rows were retained. "
              "`accuracy_clean` excludes flagged evaluation rows only; it is not proof "
              "of decontaminated training or an unbiased final test.", ""]
    rows = []
    for name in (BASE, FINAL):
        if name not in runs:
            continue
        for task, result in sorted(runs[name]["benchmarks"].items()):
            rows.append([name, SHORT.get(task, task), result["n"],
                         result.get("n_contaminated", "not recorded"),
                         display(result["accuracy"]), display(result.get("accuracy_clean")),
                         display(result.get("format_compliance")),
                         result.get("empty_outputs", "not recorded")])
    lines += [table(["Run", "Task", "n", "Flagged rows", "Raw (%)", "Filtered (%)",
                     "Strict-format (%)", "Empty"], rows), "",
              "Strict-format compliance measures extraction format, not clinical correctness.", "",
              "## Statistical interpretation and missing evidence", "",
              "The archived [SIGNIFICANCE.md](SIGNIFICANCE.md) reports pooled discordant "
              "counts 651/681 and p=0.4269 for the **sweep candidate**, not the final. "
              "It uses head-answer scoring and deduplicates by question text (298 "
              "MedBullets questions versus 308 rows in summaries). The nonsignificant "
              "result does not prove equivalence. Pooled tasks are dependent; candidate "
              "selection and multiplicity remain unresolved.", "",
              "Recover per-question outputs, case-family IDs, hashes and training logs "
              "before testing significance, F1, calibration or clinical justification. "
              "See [the evidence plan](../docs/RESEARCH_PLAN.md).", "",
              "## Input provenance", "",
              "Every input below is unchanged by this generator. Hashes identify bytes; "
              "they do not independently validate the original experiment.", ""]
    rows = []
    for name, paths in sorted(sources.items()):
        for path in paths:
            relative = os.path.relpath(path, output.parent).replace(os.sep, "/")
            rows.append([name, f"[JSON]({relative})", hashlib.sha256(path.read_bytes()).hexdigest()])
    lines += [table(["Run", "Summary", "SHA256"], rows), ""]
    return "\n".join(lines)


def updated_readme(text, block):
    if any(text.count(marker) != 1 for marker in MARKERS):
        raise ValueError("README must contain exactly one research-summary marker pair")
    pattern = re.escape(MARKERS[0]) + r".*?" + re.escape(MARKERS[1])
    return re.sub(pattern, lambda _: MARKERS[0] + "\n" + block + "\n" + MARKERS[1],
                  text, flags=re.S)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results_dir", type=Path, default=ROOT / "results")
    parser.add_argument("--baselines", type=Path, default=ROOT / "eval/baselines.json")
    parser.add_argument("--out", type=Path, default=ROOT / "results/REPORT.md")
    parser.add_argument("--readme", type=Path, default=ROOT / "README.md")
    parser.add_argument("--check", action="store_true", help="fail if generated documentation is stale")
    args = parser.parse_args()
    try:
        runs, sources = load_runs(args.results_dir.resolve())
        baselines = json.loads(args.baselines.read_text(encoding="utf-8"))
        outputs = {
            args.out: render_report(runs, sources, baselines, args.out.resolve()),
            args.readme: updated_readme(args.readme.read_text(encoding="utf-8"), summary_table(runs)),
        }
        stale = [str(path) for path, content in outputs.items()
                 if not path.exists() or path.read_text(encoding="utf-8") != content]
        if args.check and stale:
            raise ValueError("Stale generated documentation: " + ", ".join(stale))
        if not args.check:
            for path, content in outputs.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
        print(f"{len(runs)} saved runs checked; no inference executed; documentation "
              + ("is current." if args.check else "written."))
    except (ValueError, KeyError, OSError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
