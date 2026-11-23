#!/usr/bin/env python3
"""Benchmark harness for comparing AI PR reviewers on identical changes.

Implements the pre-registered protocol in ../PROTOCOL.md. Standard library
only; the only external tool it shells out to is `gh` (collect) and `git`
(prepare's source validation).

Commands
--------
  plan                 Build bench/manifest.json from bench/config.json.
                       Re-running keeps existing observation states.
  prepare PROVIDER     Write the exact PR title/body files for one provider
                       under bench/runs/<provider>/ and print the operator
                       steps (create run repo, push pilot branches, open PRs).
  mark PROVIDER CASE CONDITION STATUS [--pr URL] [--note TEXT]
                       Record an observation's outcome in the manifest.
  collect PROVIDER     Fetch each recorded PR's reviews + comments via the
                       GitHub API (`gh`) into raw/<provider>/, verbatim.
  blind                Copy raw reviews into grading/ with provider names
                       replaced by random codes (key in bench/private/).
  grade                Build results/coverage.md and results/scores.md from
                       the manifest and bench/grades.csv.
  status               Print coverage counts.

The manifest is the single source of truth for coverage. Every command is
safe to re-run: completed work is never redone silently.
"""

import argparse
import csv
import json
import random
import string
import subprocess
import sys
from pathlib import Path

BENCH = Path(__file__).resolve().parent
ROOT = BENCH.parent
CONFIG = BENCH / "config.json"
MANIFEST = BENCH / "manifest.json"
GRADES = BENCH / "grades.csv"
EXPECTED = BENCH / "expected.json"
RAW = BENCH / "raw"
GRADING = BENCH / "grading"
RESULTS = BENCH / "results"
PRIVATE = BENCH / "private"
RUNS = BENCH / "runs"

CONDITIONS = ("A", "B")
STATUSES = ("unattempted", "in_progress", "completed", "quota_stop", "error")
CLAIM_GRADES = (
    "catch", "partial", "appropriate_uncertainty",
    "false_positive", "unsupported", "unanticipated_valid",
)


def load_config():
    return json.loads(CONFIG.read_text())


def load_manifest():
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text())
    return {"observations": []}


def save_manifest(manifest):
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")


def obs_key(o):
    return (o["provider"], o["case"], o["condition"])


def planned_observations(config):
    planned = []
    for provider in config["providers"]:
        pid = provider["id"]
        for case in config["cases"]:
            planned.append({"provider": pid, "case": case, "condition": "A"})
        for case in config["snapshot_cases"]:
            planned.append({"provider": pid, "case": case, "condition": "B"})
    return planned


def cmd_plan(_args):
    config = load_config()
    manifest = load_manifest()
    existing = {obs_key(o): o for o in manifest["observations"]}
    merged = []
    for planned in planned_observations(config):
        key = obs_key(planned)
        if key in existing:
            merged.append(existing[key])
        else:
            merged.append({
                **planned,
                "base": "pilot/base",
                "head": f"pilot/{planned['case']}",
                "status": "unattempted",
                "pr_url": "",
                "run_id": "",
                "started_at": "",
                "finished_at": "",
                "note": "",
            })
    manifest["observations"] = merged
    manifest["pinned_commit"] = config["pinned_commit"]
    save_manifest(manifest)
    counts = {}
    for o in merged:
        counts[o["status"]] = counts.get(o["status"], 0) + 1
    print(f"manifest: {len(merged)} observations planned; states: {counts}")
    return 0


def pr_body(config, case, condition):
    case_dir = ROOT / "cases" / case
    title = (case_dir / "title.txt").read_text().strip()
    body = (case_dir / "body.md").read_text().strip()
    if condition == "B":
        evidence = (case_dir / "evidence.md").read_text().strip()
        body = f"{body}\n\n---\n\n{evidence}"
    return title, body


def cmd_prepare(args):
    config = load_config()
    provider = next((p for p in config["providers"] if p["id"] == args.provider), None)
    if provider is None:
        print(f"unknown provider: {args.provider}", file=sys.stderr)
        return 2
    out = RUNS / args.provider
    out.mkdir(parents=True, exist_ok=True)
    jobs = []
    for case in config["cases"]:
        jobs.append((case, "A"))
    for case in config["snapshot_cases"]:
        jobs.append((case, "B"))
    for case, condition in jobs:
        title, body = pr_body(config, case, condition)
        (out / f"case-{case}-{condition}.title.txt").write_text(title + "\n")
        (out / f"case-{case}-{condition}.body.md").write_text(body + "\n")
    print(f"wrote {len(jobs)} PR title/body pairs to {out}")
    print()
    print("Operator steps (run-repo phase, see PROTOCOL.md §3):")
    print(f"  1. Create PRIVATE repo {provider['run_repo']} (empty, no template).")
    print("  2. From a clone of the upstream template, fetch the app-only refs:")
    print("       git fetch origin pilot/base pilot/01 ... pilot/08")
    print(f"  3. Push those refs, unchanged, into {provider['run_repo']}.")
    print("  4. Install ONLY this provider on that repo"
          f" ({provider['method']}).")
    print("  5. Open one PR per file pair above: base pilot/base, compare"
          " pilot/<case>, title/body from the matching files.")
    print("     Condition B PRs are opened only after Condition A completes.")
    print("  6. Record each PR with: bench.py mark <provider> <case> <cond>"
          " in_progress --pr <url>")
    return 0


def cmd_mark(args):
    if args.status not in STATUSES:
        print(f"status must be one of {STATUSES}", file=sys.stderr)
        return 2
    manifest = load_manifest()
    for o in manifest["observations"]:
        if obs_key(o) == (args.provider, args.case, args.condition):
            o["status"] = args.status
            if args.pr:
                o["pr_url"] = args.pr
            if args.note:
                o["note"] = args.note
            save_manifest(manifest)
            print(f"marked {args.provider}/{args.case}/{args.condition} -> {args.status}")
            return 0
    print("observation not in manifest; run `bench.py plan` first", file=sys.stderr)
    return 2


def gh_api(path):
    result = subprocess.run(
        ["gh", "api", path], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"gh api {path} failed: {result.stderr.strip()}")
    return json.loads(result.stdout)


def cmd_collect(args):
    manifest = load_manifest()
    mine = [o for o in manifest["observations"]
            if o["provider"] == args.provider and o["pr_url"]]
    if not mine:
        print("no PRs recorded for this provider yet (see `mark`)", file=sys.stderr)
        return 2
    out_dir = RAW / args.provider
    out_dir.mkdir(parents=True, exist_ok=True)
    config = load_config()
    repo = next(p["run_repo"] for p in config["providers"] if p["id"] == args.provider)
    written = 0
    for o in mine:
        pr_number = o["pr_url"].rstrip("/").split("/")[-1]
        reviews = gh_api(f"repos/{repo}/pulls/{pr_number}/reviews")
        comments = gh_api(f"repos/{repo}/issues/{pr_number}/comments")
        review_comments = gh_api(f"repos/{repo}/pulls/{pr_number}/comments")
        target = out_dir / f"case-{o['case']}-{o['condition']}.md"
        if target.exists() and not args.force:
            print(f"skip (exists): {target.name}")
            continue
        lines = [
            f"# Raw review — provider: {o['provider']} · case {o['case']} · "
            f"condition {o['condition']}",
            f"PR: {o['pr_url']} · base {o['base']} · head {o['head']} · "
            f"status {o['status']}",
            "",
            "## Reviews (verbatim, in order received)",
        ]
        for r in reviews:
            lines += ["", f"### review by {r['user']['login']} · {r['submitted_at']} · {r['state']}",
                      "", r.get("body") or "(no body)"]
        for c in review_comments:
            lines += ["", f"### inline comment by {c['user']['login']} · {c['created_at']} · "
                      f"{c['path']}:{c.get('line') or c.get('original_line')}",
                      "", c.get("body") or "(no body)"]
        for c in comments:
            lines += ["", f"### PR comment by {c['user']['login']} · {c['created_at']}",
                      "", c.get("body") or "(no body)"]
        target.write_text("\n".join(lines) + "\n")
        written += 1
        print(f"wrote {target.name}: {len(reviews)} reviews, "
              f"{len(review_comments)} inline, {len(comments)} PR comments")
    print(f"collect done: {written} new file(s)")
    return 0


def blind_key():
    PRIVATE.mkdir(parents=True, exist_ok=True)
    key_file = PRIVATE / "blind-key.json"
    if key_file.exists():
        return json.loads(key_file.read_text())
    config = load_config()
    rng = random.Random()
    codes = set()
    key = {}
    for provider in config["providers"]:
        while True:
            code = "R-" + "".join(rng.choices(string.ascii_uppercase, k=3))
            if code not in codes:
                codes.add(code)
                key[provider["id"]] = code
                break
    key_file.write_text(json.dumps(key, indent=2) + "\n")
    return key


def cmd_blind(_args):
    key = blind_key()
    code_of = {pid: code for pid, code in key.items()}
    count = 0
    for provider_dir in sorted(RAW.iterdir()) if RAW.exists() else []:
        if not provider_dir.is_dir():
            continue
        code = code_of.get(provider_dir.name)
        if code is None:
            continue
        dest = GRADING / code
        dest.mkdir(parents=True, exist_ok=True)
        for raw_file in sorted(provider_dir.glob("*.md")):
            target = dest / raw_file.name
            if target.exists():
                continue
            text = raw_file.read_text()
            text = text.replace(f"provider: {provider_dir.name}", f"provider: {code}")
            target.write_text(text)
            count += 1
    print(f"blind: {count} new grading file(s) under {GRADING} "
          f"(key stays in {PRIVATE}, uncommitted until the report)")
    return 0


def load_grades():
    if not GRADES.exists():
        return []
    with GRADES.open(newline="") as fh:
        return [row for row in csv.DictReader(fh) if row.get("grade")]


def cmd_grade(_args):
    config = load_config()
    manifest = load_manifest()
    key = blind_key() if (PRIVATE / "blind-key.json").exists() else {}
    name_of_code = {code: pid for pid, code in key.items()}
    expected = json.loads(EXPECTED.read_text()) if EXPECTED.exists() else {}
    rows = load_grades()
    RESULTS.mkdir(parents=True, exist_ok=True)

    # ---- coverage table (real provider names; this is operations data) ----
    cov = ["# Coverage", "",
           "Provider-by-case status from the manifest. "
           "A = code-only, B = with deployment snapshot.", ""]
    header = "| Provider | " + " | ".join(
        f"{c}-A" + (f" / {c}-B" if c in config["snapshot_cases"] else "")
        for c in config["cases"]) + " |"
    cov.append(header)
    cov.append("|" + "---|" * (len(config["cases"]) + 1))
    by_key = {obs_key(o): o for o in manifest["observations"]}
    for provider in config["providers"]:
        cells = []
        for case in config["cases"]:
            a = by_key.get((provider["id"], case, "A"), {}).get("status", "—")
            if case in config["snapshot_cases"]:
                b = by_key.get((provider["id"], case, "B"), {}).get("status", "—")
                cells.append(f"{a} / {b}")
            else:
                cells.append(a)
        cov.append(f"| {provider['id']} | " + " | ".join(cells) + " |")
    totals = {}
    for o in manifest["observations"]:
        totals[o["status"]] = totals.get(o["status"], 0) + 1
    cov += ["", f"Totals across {len(manifest['observations'])} planned "
            f"observations: {totals}"]
    (RESULTS / "coverage.md").write_text("\n".join(cov) + "\n")

    # ---- scores (from claim-level grades) ----
    per_provider = {}
    hit_defects = set()  # (provider, case, condition, defect)
    for row in rows:
        provider = name_of_code.get(row["code"], row["code"])
        entry = per_provider.setdefault(provider, {g: 0 for g in CLAIM_GRADES})
        if row["grade"] in entry:
            entry[row["grade"]] += 1
        if row["grade"] in ("catch", "partial") and row.get("defect", "-") not in ("", "-"):
            hit_defects.add((provider, row["case"], row["condition"], row["defect"]))
    misses = {}
    for provider in config["providers"]:
        pid = provider["id"]
        count = 0
        for case, defects in expected.items():
            conditions = ["A"] + (["B"] if case in config["snapshot_cases"] else [])
            for condition in conditions:
                for defect in defects:
                    if (pid, case, condition, defect) not in hit_defects:
                        count += 1
        misses[pid] = count

    sc = ["# Scores", "",
          "Claim-level grades per PROTOCOL.md §4. Rates are always shown "
          "with their denominators.", ""]
    sc.append("| Provider | Catches | Partials | Appr. uncertainty | "
              "False positives | Unsupported | Unanticipated-valid | "
              "Misses (expected defects not hit) | Claims graded | Precision |")
    sc.append("|---|---|---|---|---|---|---|---|---|---|")
    for provider in config["providers"]:
        pid = provider["id"]
        e = per_provider.get(pid, {g: 0 for g in CLAIM_GRADES})
        claims = sum(e.values())
        good = e["catch"] + e["partial"] + e["unanticipated_valid"]
        precision = f"{good}/{claims} = {good / claims:.2f}" if claims else "—"
        sc.append(
            f"| {pid} | {e['catch']} | {e['partial']} | "
            f"{e['appropriate_uncertainty']} | {e['false_positive']} | "
            f"{e['unsupported']} | {e['unanticipated_valid']} | "
            f"{misses.get(pid, 0)} | {claims} | {precision} |")
    total_expected = sum(len(v) for v in expected.values())
    sc += ["", f"Expected defects in the key: {total_expected} across "
           f"{len(expected)} defective cases (conditions counted separately "
           "for snapshot cases in the miss count). Recall per provider = "
           "(catches + ½·partials on expected defects) ÷ expected defects "
           "for the conditions that provider completed — compute it from "
           "grades.csv when writing the report, and state the denominator."]
    (RESULTS / "scores.md").write_text("\n".join(sc) + "\n")
    print(f"grade: wrote {RESULTS / 'coverage.md'} and {RESULTS / 'scores.md'} "
          f"({len(rows)} graded claims)")
    return 0


def cmd_status(_args):
    manifest = load_manifest()
    totals = {}
    for o in manifest["observations"]:
        totals[o["status"]] = totals.get(o["status"], 0) + 1
    print(f"{len(manifest['observations'])} observations: {totals}")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(required=True, dest="command")
    sub.add_parser("plan")
    p = sub.add_parser("prepare")
    p.add_argument("provider")
    p = sub.add_parser("mark")
    p.add_argument("provider")
    p.add_argument("case")
    p.add_argument("condition", choices=CONDITIONS)
    p.add_argument("status")
    p.add_argument("--pr", default="")
    p.add_argument("--note", default="")
    p = sub.add_parser("collect")
    p.add_argument("provider")
    p.add_argument("--force", action="store_true")
    sub.add_parser("blind")
    sub.add_parser("grade")
    sub.add_parser("status")
    args = parser.parse_args()
    return {
        "plan": cmd_plan, "prepare": cmd_prepare, "mark": cmd_mark,
        "collect": cmd_collect, "blind": cmd_blind, "grade": cmd_grade,
        "status": cmd_status,
    }[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
