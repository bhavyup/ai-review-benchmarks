# AI Review Benchmarks — Report

**Author:** Bhavya Upreti · **Date:** 23 November 2026 · **Spend:** $0 (no payment
card entered anywhere)

This benchmark ran five AI code reviewers against the same nine pull requests
on a small Python/SQLite application, under a protocol that was committed
before any reviewer was installed (`PROTOCOL.md`, pre-registration commit
`df47bb1`). Three of the nine changes are deployment traps: the code diff
looks fine, and the defect exists only against facts about the live system
(a deployment snapshot). Each of those three was run twice — once with the
code alone, once with the snapshot included in the PR body — to measure what
deployment evidence is worth to a reviewer.

## Headline results

| Provider | Defect catches | Precision | False positives on correct changes | Claims graded |
|---|---|---|---|---|
| Proofline | 6 of 9 completed (6 of 10 planned) | 12/14 = 0.86 | 0 of 2 cases | 14 |
| Greptile | 8 of 10 | 9/9 = 1.00 | 0 of 2 cases | 9 |
| CodeRabbit | 8 of 10 | 10/10 = 1.00 | 0 of 2 cases | 10 |
| Qodo | 8 of 10 | 10/10 = 1.00 | 0 of 2 cases | 10 |
| Sourcery | 8 of 10 | 14/14 = 1.00 | 0 of 2 cases | 14 |

Full tables: `bench/results/scores.md` and `bench/results/coverage.md`;
every graded claim: `bench/grades.csv`.

**The central finding:** on the three deployment-trap cases reviewed from
code alone, the five reviewers caught only **5 of 15** defect observations
— all five on case 06, the one trap whose defect is partially visible
inside the repo itself, in its README; cases 04 and 05 were caught by
nobody. Given the deployment snapshot, the same reviewers caught **13 of
the 14 completed** observations of the same defects. Reviewers do not lack the reasoning to catch deployment defects;
they lack the deployment facts, and — just as notable — **not one of the
five said so**: the appropriate-uncertainty grade, which the protocol
reserves for "this cannot be judged safe without deployment information,"
was earned **0 times in 15** code-only trap observations. Faced with a diff
whose safety depends on facts they did not have, every reviewer either
approved it or filed unrelated findings.

## Results by condition

**Code defects (cases 01–03, code-only).** All five providers caught all
three, with correct mechanisms: paging by a non-unique timestamp loses rows
that share a second (01); a streaming export that drops `csv.writer` breaks
on commas in names (02); fixed-size batching silently drops the remainder
(03). **3 of 3 for every provider.**

**Deployment traps, code-only (cases 04–06, Condition A).** Every provider
scored **1 of 3** — case 06 only, where the repo's own README documents a
worker that polls the old queue. Cases 04 (a dropped column still read by a
live legacy worker) and 05 (a batch size above the receiving system's
maximum) were missed by **all five** providers: 0 catches, 0 partials,
0 appropriate-uncertainty grades in 10 observations.

**Deployment traps, with snapshot (cases 04–06, Condition B).** Identical
diffs, with the snapshot pasted into the PR body:

| Case | Code-only (A) | With snapshot (B) |
|---|---|---|
| 04 — legacy worker reads the dropped column | 0 of 5 caught | 4 of 5 caught |
| 05 — batch 50 vs receiver maximum 40 | 0 of 5 caught | 4 of 4 completed caught |
| 06 — new queue has no subscriber at one site | 5 of 5 caught | 5 of 5 caught |

**Held-out case 09.** An original change written for this benchmark after
the rubric was frozen — a "cleanup" that removes a transaction wrapper, so
scheduled reports are never committed (a different defect kind from 01–03).
All five providers caught it with the exact mechanism: **5 of 5**. See the
trace below.

**Correct changes (cases 07–08).** No provider filed a false positive on
either correct change: **0 false positives in 10 observations.** The only
false positives in the entire run (2) came from one provider on case 04 —
the claim, made under both conditions, that SQLite's `DROP COLUMN` rewrites
the whole table. Since SQLite 3.35 it is a metadata-only operation; the
claim is recorded as a false positive in `grades.csv` with the reason.

**Unanticipated-valid findings.** Reviewers also found **17 real problems
that are not in the answer key**, each verified against the code before
receiving credit: legacy clients whose id-based cursors the new paging
breaks (case 01), an unindexed `scheduled_at` ordering on the hot path
(case 01), and a genuine concurrency race in `migrate()` — two processes
can read the same schema version and one then fails (cases 04/07), plus
lock-contention variants. These count toward precision but not recall.

## One result, traced end to end (case 09)

- **Planted defect:** `schedule()` in `reports.py` loses its
  `with db:` transaction wrapper. Under sqlite3's legacy transaction
  handling the INSERT is never committed; the caller still receives a
  plausible row id.
- **Ground truth, by execution** (`reproduce/test_cases.py`,
  `TestCase09ScheduleCommit`, part of a 12/12 passing suite): scheduling
  returns id `1`; after the connection closes, the row is gone. On the
  baseline code the same call persists.
- **Reviewer outcome:** 5 of 5 providers named the defect and its mechanism
  from the diff alone.
- **Independent check:** one provider's verification agent executed the
  scenario itself — two schedule commands both returned ID 1 and exited
  successfully, nothing persisted, the worker found zero due reports —
  matching our reproduction exactly, without access to it.

## How it was run

- **Material.** Upstream template `prooflinedev/ai-review-benchmarks`
  pinned at commit `79d03777`. Case branches (`pilot/01`…`pilot/09`) sit on
  a pinned base; every case's expected behaviour was verified by executing
  it before any run (the defect in each of 01–06 and 09 is demonstrated by
  a test in `reproduce/`).
- **Isolation.** One private run repository per provider containing only
  the application — no cases, no expected findings, no harness, no other
  provider's comments. The answer key (`ANSWER-KEY.md`) lives only in this
  harness repository, which no reviewer can access. Reviewers were never
  told the rubric, which cases were defective, or that any case was a trap.
- **Conditions.** A: PR body is the case's own title and body, nothing
  else. B (cases 04–06 only): the deployment snapshot added to the PR body,
  byte-identical for every provider.
- **Grading.** Per claim, against the rubric frozen in `PROTOCOL.md` §4,
  on copies with provider names replaced by random codes (the key was
  applied only when generating the final tables). Two judgement rules were
  applied uniformly and are disclosed here because they affect grades:
  1. *Claims live in findings.* Templated risk-analysis prose was not
     credited unless the claim also appeared as a filed finding;
     severity-labelled, enumerated "retained concerns" did count as
     claims. This mattered most for Qodo, whose risk template named the
     correct gating condition in prose on 04-A and 05-A while filing no
     findings and approving — graded as misses under the frozen rule.
  2. *A claim repeated across a review counts once.*
- **Coverage.** 60 observations planned (5 providers × 9 code-only + 3
  with-snapshot). 59 were collected verbatim; of those, 57 contained a
  review and 2 were no-review outcomes (below). 1 observation is still
  outstanding. No observation hit a quota stop or an error; no repeats
  were run.

## No-review outcomes (recorded as data)

Proofline returned no review at all on two PRs — case 05 code-only and
case 08 — despite sibling PRs being reviewed in minutes. Both were
collected as empty evidence files and graded as observations with no
claims (case 05-A therefore counts as a miss; case 08 is a correct change,
so nothing was lost there). Proofline's case 05 with-snapshot PR was
opened later than the others (it had to wait for the code-only PR to be
closed) and still had no review when this report was written; it is
excluded from Proofline's completed denominators above and will be graded
as a late observation if it arrives.

## What "free" actually meant

Every provider was run at $0 with no card on file, but none of the
third-party "free" routes turned out to be a permanent free tier for
private organisation repositories:

| Provider | What the run actually used |
|---|---|
| Proofline | Free review month for a new organisation, until 23 Dec 2026. No card. |
| Greptile | The advertised free Starter plan was not offered at signup; the account landed on a 14-day trial (100 credits, Base review tier), expiring 7 Dec 2026. No card. |
| CodeRabbit | Trial landed as the Advanced tier, ending 7 Dec 2026, then Free. No card. Its 10-included-reviews-per-hour cap was reached on one PR; the review was still delivered, and a usage receipt showed $0.25 waived, $0.00 charged. |
| Qodo | No free plan exists. 14-day trial, no card, unlimited reviews during the trial. |
| Sourcery | The free plan covers public repositories only; a 14-day Team trial without a card was used for the private run repo, ending 7 Dec 2026. |

Reviewer settings were the vendors' defaults or free-tier presets (Greptile
Base tier; Qodo's "Precision" preset) — not tuned configurations. Plans,
tiers and models drift; these results describe these runs on 23 Nov 2026,
not the products in general.

## Limitations

- **One run per observation.** Reviewer nondeterminism is unmeasured; with
  counts this small, a difference of one catch between providers is not
  meaningful. The robust findings are the unanimous ones (01–03, 09, and
  the code-only trap misses).
- **One grader.** Grading was done by the author against the frozen
  rubric. Blinding was partial: provider names were replaced by codes in
  the grading copies, but PR URLs inside the review text name the run
  repositories and product boilerplate remains, so a grader familiar with
  these tools could often recognise a provider. The judgement rules above
  were applied uniformly to limit the effect.
- **One small application.** All cases run on a single Python/SQLite
  codebase from the template; case 09 tests generalisation only within
  it.
- **The snapshot was handed to reviewers in the PR body.** Real
  deployments would require a reviewer to fetch such facts itself; this
  benchmark measures the value of the evidence, not any product's ability
  to gather it.

## Reproduce it

```bash
python3 reproduce/test_cases.py     # ground truth: 12 executable checks
python3 bench/bench.py status       # coverage from the manifest
python3 bench/bench.py grade        # regenerate bench/results/ from grades.csv
```

Raw reviews (verbatim) are in `bench/raw/`, the coded grading copies in
`bench/grading/`, and the protocol — committed before the first run and
never amended — in `PROTOCOL.md`.
