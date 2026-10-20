import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("report", ROOT / "scripts/make_report.py")
report = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(report)


class ResearchReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runs, cls.sources = report.load_runs(ROOT / "results")

    def test_recorded_scores_and_delta_rounding(self):
        expected = {report.BASE: "58.79", report.SFT: "57.35",
                    report.SWEEP: "58.90", report.FINAL: "59.23"}
        for name, value in expected.items():
            self.assertEqual(report.display(report.macro6(self.runs[name])), value)
        delta = report.macro6(self.runs[report.FINAL]) - report.macro6(self.runs[report.BASE])
        self.assertEqual(report.display(delta, True), "+0.43")

    def test_complete_sweep_not_replaced_by_final(self):
        sweep = [r for name, r in self.runs.items() if "__soup" in name]
        self.assertEqual(len(sweep), 5)
        self.assertEqual(sum(report.macro6(r) < report.macro6(self.runs[report.BASE])
                             for r in sweep), 3)

    def test_same_path_discrepancy_is_one_task_and_six_net_correct(self):
        a, b = self.runs[report.SWEEP], self.runs[report.FINAL]
        self.assertEqual(a["model"], b["model"])
        changes = report.changed_tasks(a, b)
        self.assertEqual([row[0] for row in changes], ["medbullets_op5"])
        _, left, right = changes[0]
        self.assertEqual(report.inferred_correct(right) - report.inferred_correct(left), 6)

    def test_weighting_sensitivity(self):
        delta = report.family5(self.runs[report.FINAL]) - report.family5(self.runs[report.BASE])
        self.assertEqual(report.display(delta, True), "+0.26")

    def test_nested_and_flat_copies_must_agree(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run = self.runs[report.BASE]
            (root / "summary_base.json").write_text(json.dumps(run))
            (root / "nested").mkdir()
            copy = root / "nested/summary_base.json"
            copy.write_text(json.dumps(run))
            self.assertEqual(len(report.load_runs(root)[0]), 1)
            altered = dict(run, model="different")
            copy.write_text(json.dumps(altered))
            with self.assertRaisesRegex(ValueError, "Conflicting"):
                report.load_runs(root)

    def test_missing_tasks_are_not_zero(self):
        self.assertIsNone(report.macro6({"benchmarks": {}}))

    def test_generated_doc_has_no_superiority_gate(self):
        baselines = json.loads((ROOT / "eval/baselines.json").read_text())
        output = report.render_report(self.runs, self.sources, baselines, ROOT / "results/REPORT.md")
        for misleading in ("beats all", "Win conditions", "statistically indistinguishable",
                           "unbiased estimate", "GATE PASSED"):
            self.assertNotIn(misleading, output)
        self.assertIn("59.23", output)
        self.assertIn("58.90", output)
        self.assertIn("+2.89", output)

    def test_readme_markers_are_required_and_bounded(self):
        start, end = report.MARKERS
        text = "before\n" + start + "\nold\n" + end + "\nafter"
        self.assertEqual(report.updated_readme(text, "new"),
                         "before\n" + start + "\nnew\n" + end + "\nafter")
        with self.assertRaises(ValueError):
            report.updated_readme("no markers", "new")


if __name__ == "__main__":
    unittest.main()
