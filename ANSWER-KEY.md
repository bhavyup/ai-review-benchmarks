# Answer key — PRIVATE to this harness repository

**Never copy this file, its contents, or paraphrases of it into a run
repository, a PR body, or anywhere a reviewer can reach.** Reviewers are
installed only on app-only run repos (PROTOCOL.md §3); this file is why the
harness repo must stay private and reviewer-free.

Committed after the protocol pre-registration (`df47bb1`) and before the
first reviewer run. Defect IDs match `bench/expected.json`.

## Cases 01–03 — code defects (proven by execution, `reproduce/test_cases.py`)

| Case | Defect ID | Expected finding |
|---|---|---|
| 01 | `history-cursor-skips-shared-timestamps` | Paging history by `scheduled_at` loses rows: the cursor is a timestamp, and the service allows several reports in the same second, so rows sharing the page-boundary timestamp are never returned. Proven: 5 rows at one timestamp, page size 2 → only 2 rows reachable, 3 lost. A catch must name the shared-timestamp mechanism, not just "paging looks off". |
| 02 | `csv-escaping-lost` | The streaming rewrite drops `csv.writer` and joins fields with commas, so report names containing commas/quotes/newlines corrupt the export. Proven: `Weekly, "special" orders` exports as 4 fields instead of 3. Streaming itself is fine; the defect is the lost escaping. |
| 03 | `batch-remainder-dropped` | The batch loop `range(0, len(jobs) - 20 + 1, 20)` never processes the final partial batch. Proven: 25 due jobs → 20 delivered; 7 due jobs → 0 delivered. A catch must name the dropped remainder (or the short-queue case), not just "batching is risky". |

## Cases 04–06 — deployment-dependent (the snapshot is the evidence)

Under Condition A (code-only), the correct behaviour is *appropriate
uncertainty* (PROTOCOL.md §4) unless the reviewer names the exact condition
that would break — that grades as a catch. Under Condition B, the snapshot
contains everything needed for a catch.

| Case | Defect ID | Expected finding |
|---|---|---|
| 04 | `legacy-column-still-read-by-live-workers` | Snapshot `inventory-204`: site **elm** still runs `workers-17` (2 replicas) polling `SELECT id, legacy_format FROM deliveries …` while the migration drops `legacy_format` online → those workers break. Cedar and elm's `workers-18` are unaffected. |
| 05 | `batch-size-exceeds-receiver-limit` | Snapshot `archive-318`: batch size rises to 50, but site **cedar**'s receiver (`archive-11`) caps requests at 40 rows and rejects oversized requests in full; 70 rows are ready → cedar's archive fails outright. Elm's limit is 100 and is fine. |
| 06 | `new-queue-has-no-subscriber-at-one-site` | Snapshot `subscriptions-416`: new jobs route to `report-dispatch`, but site **elm** subscribes only to `reports` → its 8 new jobs due in the window are never delivered. Cedar subscribes to both queues and is fine. |

## Cases 07–08 — correct changes (controls)

| Case | Expected behaviour |
|---|---|
| 07 | No defect. The partial index `(queue, scheduled_at, id) WHERE delivered_at IS NULL` matches the worker query. Verified in `reproduce/test_cases.py` (index exists after migration; the app still delivers). Any claimed defect here is a false positive unless verified as unanticipated-valid. |
| 08 | No defect. `total = delivered + pending = count(*)`. Verified by execution. Same false-positive rule as 07. |

## Grading notes

- Grade claims, not comments (PROTOCOL.md §4). A reviewer that buries the
  right mechanism inside a list of wrong guesses earns the catch for that
  claim and false positives for the wrong ones — both are recorded.
- "Needs more information" on 01–03 is **not** appropriate uncertainty:
  those defects are fully visible in the code. It grades as a miss for the
  defect, and the statement itself is not a claim.
- Style, naming, or performance suggestions on any case are `unsupported`
  unless they carry a checkable mechanism, in which case they are graded
  on their merits (and usually land as false positives or
  unanticipated-valid after verification).

## Case 09 — held-out (written 23 Nov 2026, after the rubric freeze and after all Condition A/B runs for cases 01–08 were opened)

| Case | Defect ID | Expected finding |
|---|---|---|
| 09 | `scheduled-report-never-committed` | Removing the `with db:` wrapper from `schedule()` leaves the INSERT uncommitted (sqlite3 legacy transaction handling). The caller still receives a plausible row id, but when the connection closes — e.g. the console's short-lived `schedule` command exits — the transaction rolls back and the scheduled report silently does not exist. Proven in `reproduce/test_cases.py`: schedule on a file-backed DB, close, reopen → baseline has 1 row, patched has 0. A catch must name the missing commit / rollback-on-close mechanism. "Needs a transaction" without the consequence, or generic style remarks, do not earn the catch. |
