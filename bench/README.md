# Operating the benchmark

Everything here implements `../PROTOCOL.md` (pre-registered — read it first).
Standard library only. Run from the repository root:

```sh
python3 bench/bench.py <command>
```

## Add the next provider

1. Add an entry to `bench/config.json` (`id`, `run_repo`, `method`).
2. `python3 bench/bench.py plan` — the manifest gains that provider's
   observations as `unattempted`, keeping everyone else's state.
3. `python3 bench/bench.py prepare <provider>` — writes the exact PR
   title/body files under `bench/runs/<provider>/` and prints the run-repo
   steps. Follow them: one **private** run repo, app-only refs
   (`pilot/base`, `pilot/01`…`pilot/08`), only this provider installed,
   one PR per case.
4. As each PR opens: `bench.py mark <provider> <case> A in_progress --pr <url>`.
   When its first review lands (or it stops): `mark ... completed`
   (or `quota_stop` / `error`, with `--note` saying what happened).
5. Condition B (snapshot PRs for cases 04–06) starts only after that
   provider's Condition A is complete.

## Run the same cases again / recover from an interrupted run

The manifest (`bench/manifest.json`) is the source of truth. `collect`
skips raw files that already exist; `mark` only moves the observation you
name; `plan` never resets a recorded state. If a run is interrupted, read
`bench.py status`, then continue from the first non-`completed`
observation. An intentional re-review is a *repeat*: note it in the
manifest entry's `note` field — never overwrite the first review.

## Collect and grade

```sh
python3 bench/bench.py collect <provider>   # needs `gh` authenticated
python3 bench/bench.py blind                # raw/ -> grading/ under codes
# grade claims in bench/grades.csv: one row per claim —
#   code, case, condition, defect (from bench/expected.json, or -),
#   grade (catch|partial|appropriate_uncertainty|false_positive|
#          unsupported|unanticipated_valid), note
python3 bench/bench.py grade                # -> bench/results/*.md
```

The blind key lives in `bench/private/` and is **not committed** until the
final report, when it is published alongside the tables so any reader can
trace every score back to the original review in `bench/raw/`.

## Trace a score back to the original review

`results/scores.md` (provider, counts) → `grades.csv` (the claim and its
grade) → `grading/<code>/case-<case>-<condition>.md` (the graded text) →
`raw/<provider>/case-<case>-<condition>.md` (the verbatim review, with the
PR link) → the PR itself. Ground truth for every code defect is executable:
`python3 -m unittest discover -s reproduce -v`.
