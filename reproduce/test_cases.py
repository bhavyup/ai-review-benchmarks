"""Executable ground truth for the benchmark cases.

Each test builds two variants of the sample application in a temp directory:
the pinned baseline, and the baseline with one case patch applied
(`git apply -p0`, the same way the case guide describes). It then asserts the
behaviour that makes the case defective — or correct — on BOTH variants, so
the file proves the ground truth instead of merely noting a difference.

Run from the repository root:

    python3 -m unittest discover -s reproduce -v

Standard library only. Requires `git` on PATH (for `git apply`).
"""

import csv
import importlib.util
import io
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP_FILES = ["reports.py", "console.py"]
APP_DIRS = ["migrations"]


def build_variant(case: str | None) -> Path:
    """Copy the app into a temp dir, optionally applying cases/<case>/change.patch."""
    tmp = Path(tempfile.mkdtemp(prefix=f"bench-{case or 'base'}-"))
    for name in APP_FILES:
        shutil.copy(ROOT / name, tmp / name)
    for name in APP_DIRS:
        shutil.copytree(ROOT / name, tmp / name)
    if case is not None:
        patch = ROOT / "cases" / case / "change.patch"
        result = subprocess.run(
            ["git", "apply", "-p0", str(patch)],
            cwd=tmp, capture_output=True, text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"applying case {case} failed: {result.stderr}")
    return tmp


def load_reports(variant: Path, tag: str):
    spec = importlib.util.spec_from_file_location(f"reports_{tag}", variant / "reports.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def fresh_db(reports) -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    reports.migrate(db)
    return db


class VariantTest(unittest.TestCase):
    case = None  # subclasses set the case they exercise

    @classmethod
    def setUpClass(cls):
        cls.base_dir = build_variant(None)
        cls.base = load_reports(cls.base_dir, f"base_{cls.__name__}")
        if cls.case is not None:
            cls.case_dir = build_variant(cls.case)
            cls.patched = load_reports(cls.case_dir, f"case{cls.case}_{cls.__name__}")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.base_dir, ignore_errors=True)
        if cls.case is not None:
            shutil.rmtree(cls.case_dir, ignore_errors=True)


class TestBaselineSanity(VariantTest):
    def test_deliver_and_summary(self):
        db = fresh_db(self.base)
        for i in range(3):
            self.base.schedule(db, f"r{i}", 1000)
        self.assertEqual(self.base.deliver_due(db, "reports", 2000), 3)
        self.assertEqual(self.base.summary(db), {"delivered": 3, "pending": 0})


class TestCase01HistoryPaging(VariantTest):
    """01 pages history by scheduled time. The service contract allows several
    reports in the same second (docs/report-service.md), so a cursor keyed on
    scheduled_at alone must lose rows that share a timestamp."""

    case = "01"

    def page_all(self, reports, limit=2):
        db = fresh_db(reports)
        for i in range(5):
            reports.schedule(db, f"r{i}", 1000)  # all in the same second
        seen, cursor = [], None
        for _ in range(6):
            page = reports.history(db, limit, cursor)
            seen += [row[1] for row in page.rows]
            cursor = page.next_cursor
            if cursor is None:
                break
        return seen

    def test_baseline_pages_every_row(self):
        self.assertEqual(sorted(self.page_all(self.base)), [f"r{i}" for i in range(5)])

    def test_patched_loses_rows_sharing_a_timestamp(self):
        seen = self.page_all(self.patched)
        self.assertEqual(len(seen), 2)  # only the first page is ever reachable
        self.assertEqual(set(f"r{i}" for i in range(5)) - set(seen), {"r0", "r1", "r2"})


class TestCase02StreamExport(VariantTest):
    """02 streams the export but drops the CSV writer, so values containing
    commas or quotes are no longer escaped."""

    case = "02"

    def export_rows(self, reports):
        db = fresh_db(reports)
        reports.schedule(db, 'Weekly, "special" orders', 1000)
        out = io.StringIO()
        reports.write_export(db, out)
        return list(csv.reader(io.StringIO(out.getvalue())))

    def test_baseline_escapes_commas_and_quotes(self):
        rows = self.export_rows(self.base)
        self.assertEqual(rows[1], ["1", 'Weekly, "special" orders', "1000"])

    def test_patched_corrupts_the_row(self):
        rows = self.export_rows(self.patched)
        self.assertEqual(len(rows[1]), 4)  # one field split into two: corrupt CSV


class TestCase03BatchDeliveries(VariantTest):
    """03 batches delivery in groups of twenty and drops the remainder."""

    case = "03"

    def deliver(self, reports, n):
        db = fresh_db(reports)
        for i in range(n):
            reports.schedule(db, f"r{i}", 1000)
        return reports.deliver_due(db, "reports", 2000)

    def test_baseline_delivers_every_due_job(self):
        self.assertEqual(self.deliver(self.base, 25), 25)
        self.assertEqual(self.deliver(self.base, 7), 7)

    def test_patched_drops_the_remainder_batch(self):
        self.assertEqual(self.deliver(self.patched, 25), 20)  # 5 left pending
        self.assertEqual(self.deliver(self.patched, 7), 0)    # a short queue delivers nothing


class TestCase07IndexPending(VariantTest):
    """07 is a correct change: the partial index it adds matches the worker
    query (queue + scheduled_at, delivered_at IS NULL). Control case."""

    case = "07"

    def index_names(self, reports):
        db = fresh_db(reports)
        return {row[0] for row in db.execute(
            "SELECT name FROM sqlite_master WHERE type='index'")}

    def test_baseline_has_no_such_index(self):
        self.assertNotIn("deliveries_due_by_queue", self.index_names(self.base))

    def test_patched_adds_the_index_and_app_still_works(self):
        self.assertIn("deliveries_due_by_queue", self.index_names(self.patched))
        db = fresh_db(self.patched)
        self.patched.schedule(db, "r0", 1000)
        self.assertEqual(self.patched.deliver_due(db, "reports", 2000), 1)


class TestCase08SummaryTotal(VariantTest):
    """08 is a correct change: total = delivered + pending = row count.
    Control case."""

    case = "08"

    def test_patched_total_is_correct(self):
        db = fresh_db(self.patched)
        for i in range(3):
            self.patched.schedule(db, f"r{i}", 1000)
        self.patched.deliver_due(db, "reports", 2000)
        self.patched.schedule(db, "late", 3000)
        self.assertEqual(
            self.patched.summary(db),
            {"delivered": 3, "pending": 1, "total": 4},
        )


if __name__ == "__main__":
    unittest.main()
