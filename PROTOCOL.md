# Benchmark Protocol — pre-registered before any reviewer run

**Committed on its own, before any provider was installed and before any review
output existed.** Any later change to this file is an amendment: it must be
dated, explained, and listed at the bottom. The scoring rules in §4 do not
change after the first run.

- Upstream template: `prooflinedev/ai-review-benchmarks`
- Pinned upstream commit: `79d03777827b88aa23ee9309ebefab5f9766cd09`
- Cases: 01–08 from the template, plus one original held-out case (09) written
  after this protocol was committed (see §5).
- This repository is the harness. It holds the benchmark code, this protocol,
  the answer key, grades and the report. **No AI reviewer is installed here.**
  Reviewers only ever see separate, app-only run repositories (§3).

## 1. Unit of observation

One observation = one provider × one case × one context condition × one pinned
base/head commit pair. For each observation we record: provider, plan/model
when visible, settings, trigger method, timestamps, terminal outcome
(completed / quota-stop / error / unattempted), and the provider's **first**
review, captured verbatim.

A duplicate delivery of the same review (e.g. a repeated webhook) is one
observation. An intentional second review of the same pair is a *repeat*:
recorded as such, reported separately, and never silently substituted for the
first.

## 2. Context conditions

- **Condition A — code-only (primary).** All 8 cases. The PR title and body are
  exactly the case's own `title.txt` and `body.md`. Nothing else.
- **Condition B — with-snapshot (secondary).** Cases 04–06 only. The case's
  `evidence.md` is included in the PR body, byte-identical for every provider.
  Results are compared against the same provider's Condition A result on the
  same case.

Every provider starts on the same batch (Condition A, cases in order 01–08) so
partial runs still overlap and stay comparable. Condition B runs only after a
provider finishes Condition A.

The review window for a run is: from PR creation until the provider's first
review is complete, or a documented quota stop / error, or 60 minutes —
whichever comes first. Anything arriving later is recorded as late and does
not replace the first review.

## 3. Isolation

- One private run repository per provider, containing only the application:
  upstream `pilot/base` plus one branch per case (`pilot/01` … `pilot/08`,
  later `pilot/09`). No cases folder, no expected findings, no harness code,
  no grades, and no other provider's comments.
- The answer key lives only in this harness repository, which no reviewer can
  access.
- Where a provider offers controls for cross-repository learning or indexing,
  they are turned off where the plan allows; anything that cannot be
  controlled is written down in the report as residual uncertainty.
- Providers are never told the scoring rubric, the expected findings, or that
  any particular case is defective or correct.

## 4. Scoring — frozen

Grading is **per claim**, not per comment. Each review is split into its
individual claims; a repeated claim counts once.

| Grade | Meaning |
|---|---|
| **Catch** | Names a real defect **and** its correct mechanism — why it breaks, and under what input or condition. |
| **Partial** | Right area, but the mechanism is wrong, missing, or too vague to act on. Half credit. |
| **Appropriate uncertainty** | Cases 04–06 under Condition A only: states the change cannot be judged safe without deployment information, and names roughly what information is needed. Neither a catch nor a miss. A conditional warning that names the *correct* condition (e.g. "breaks if any live worker still reads this column") grades as a Catch. |
| **Miss** | An expected defect (cases 01–06) appears in no claim. |
| **False positive** | Claims a defect that is not real, disproven against the code or by execution. Any claimed defect on a correct case (07, 08) is a false positive unless verified as an unanticipated-valid finding. |
| **Unsupported** | A warning with no checkable mechanism. Counted; earns nothing. |
| **Unanticipated-valid** | A real problem outside the answer key, verified by us against the code or by execution before any credit. Recorded separately. |

**Reported per provider, always with denominators, never rates alone:**

- Recall on defective cases: catches (+ ½ partials) out of 6 expected defects;
  for cases 04–06, Conditions A and B are reported separately.
- Precision: (catches + partials + unanticipated-valid) ÷ all claims made.
- False positives on the correct cases (07, 08), as a headline number.
- Appropriate-uncertainty count on cases 04–06, Condition A.
- Snapshot uplift on cases 04–06: grade movement from Condition A to B.
- Coverage: completed / quota-stopped / errored / unattempted pairs,
  distinct providers, distinct cases, completed pairs and repeats — each
  reported as its own number.

**Blind grading.** Raw reviews are copied into grading files with provider
names replaced by random codes. Grading happens on the coded files. The code
key is applied only when the final tables are generated.

**Checking disputed findings.** Every disputed or surprising grade gets a
written check. For code defects, the check is an executable reproduction in
`reproduce/` that demonstrates the behaviour on the baseline and on the
patched code. For snapshot cases, the check is a line-by-line trace against
the snapshot data.

## 5. Held-out case 09

After this protocol is committed and Condition A is under way, we write one
original change to the same application containing one known defect of a
different kind from cases 01–03, proven by an executable reproduction before
it is run. Case 09 is run under Condition A on every provider and graded with
exactly the rules in §4. Its purpose is to test whether reviewers are reading
the code in front of them, and whether this harness generalises beyond the
published cases.

## 6. Providers and the $0 rule

An integration counts toward coverage only when it produces an actual review
on a private PR. Priority order (free-allowance reliability for private
repositories, checked 2026-11-23 and re-verified at install time):

1. Proofline (hosted review credit for new organisations)
2. Greptile (free Starter credits; **Base review tier only**, for comparability
   and to stay within the free allowance)
3. CodeRabbit (free trial; the trial starts only when its batch is ready)
4. Qodo (free plan, or self-hosted PR-Agent with a pinned model — one method,
   chosen at install time and labelled honestly in the report)
5. Sourcery (free plan; fallback: a pinned CLI-agent reviewer with a fixed
   prompt, labelled as such)

Minimum to write the report: **3 distinct providers completing Condition A.**
Target: 5 providers × 8 cases = 40 Condition A observations, up to 15
Condition B observations, and 5 held-out observations.

Hard rules: $0 out of pocket. No payment card is entered anywhere. If a
provider requires a card, a public repository, or excludes private PR reviews
from its free tier, it is recorded as *unattempted — reason* and we move on.
Every quota stop is recorded as data.

## 7. Deployment trace

Separately from the review runs, one pinned commit of the sample application
is traced from GitHub PR → CI checks → deployment to our own AWS account →
verified invocation, with the workflow link and invocation receipt saved as
evidence, and the stack deleted afterwards. Local packaging/smoke results are
labelled as local and are never presented as a live deployment. Facts from the
live deployment and facts from the supplied case snapshots are labelled by
source wherever they are used.

## Amendments

_(None. Amendments are appended here, dated, with the reason. §4 cannot be
amended after the first run.)_
