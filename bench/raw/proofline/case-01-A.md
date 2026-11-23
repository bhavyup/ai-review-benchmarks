# Raw review — provider: proofline · case 01 · condition A
PR: https://github.com/upreti-labs/run-proofline/pull/1 · base pilot/base · head pilot/01 · status in_progress

## Reviews (verbatim, in order received)

### review by prooflinedev[bot] · 2026-11-23T12:01:33Z · COMMENTED

<!-- proofline:review-comment -->
<!-- proofline:review-publication:1be9da1a-fce0-49af-b6e2-8cb3261333f3 -->
**Proofline** has 3 new findings to review.

[View full review in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a20847-6f94-77ab-9712-d1e2cf3591bd)

<!-- proofline:published-findings -->
<!-- proofline:published-finding-series=01a20848-5d5e-722b-bdc2-df6abfeed32d -->
<!-- proofline:published-thread-series=01a20848-5d5e-722b-bdc2-df6abfeed32d -->
<!-- proofline:published-finding-series=01a20848-5d64-7226-9366-b52fcd2455b8 -->
<!-- proofline:published-thread-series=01a20848-5d64-7226-9366-b52fcd2455b8 -->
<!-- proofline:published-finding-series=01a20848-5d65-72ff-8965-d654d1623964 -->
<!-- proofline:published-thread-series=01a20848-5d65-72ff-8965-d654d1623964 -->
<!-- /proofline:published-findings -->
<!-- proofline:published-code=01a20848-5d66-71c6-a330-1b39fcfd1f67 -->
<!-- proofline:published-code-thread=01a20848-5d66-71c6-a330-1b39fcfd1f67 -->
<!-- proofline:published-code=01a20848-5d6f-7073-b8eb-b6efd62842fe -->
<!-- proofline:published-code-thread=01a20848-5d6f-7073-b8eb-b6efd62842fe -->
<!-- proofline:published-code=01a20848-5d73-7154-846e-4a09ad806308 -->
<!-- proofline:published-code-thread=01a20848-5d73-7154-846e-4a09ad806308 -->

### inline comment by prooflinedev[bot] · 2026-11-23T12:01:33Z · reports.py:45

<!-- proofline:finding-series=01a20848-5d5e-722b-bdc2-df6abfeed32d -->
**Warning** · History skips deliveries tied at a page boundary

History sorts by `scheduled_at` and `id`, but its cursor stores only `scheduled_at` and the next page excludes every row with that timestamp.

When a page splits deliveries scheduled for the same second, subsequent pages silently omit the remaining deliveries from that second.

Encode both `scheduled_at` and `id` in the cursor and resume with a strict comparison on that pair.

[View finding in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a20847-6f94-77ab-9712-d1e2cf3591bd/findings/01a20848-5d66-71c6-a330-1b39fcfd1f67)

### inline comment by prooflinedev[bot] · 2026-11-23T12:01:33Z · reports.py:45

<!-- proofline:finding-series=01a20848-5d64-7226-9366-b52fcd2455b8 -->
**Warning** · Saved history cursors can silently return an empty page

This change treats saved delivery IDs passed as `--cursor` as timestamp cutoffs without detecting the old format.

An operator resuming with an ID below all scheduled timestamps sees an empty page instead of the remaining history or an obsolete-cursor error.

Version new cursors and reject legacy integers with a message explaining how to restart pagination.

[View finding in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a20847-6f94-77ab-9712-d1e2cf3591bd/findings/01a20848-5d6f-7073-b8eb-b6efd62842fe)

### inline comment by prooflinedev[bot] · 2026-11-23T12:01:33Z · reports.py:45

<!-- proofline:finding-series=01a20848-5d65-72ff-8965-d654d1623964 -->
**Warning** · First history page scans every delivery

This change orders by unindexed `scheduled_at` before applying `LIMIT`. With `N` deliveries, SQLite now examines all `N` rows and maintains a top-results sort instead of stopping after `limit + 1` primary-key entries.

Even a small first page gets slower as delivery history grows.

Add a migration creating an index on `(scheduled_at DESC, id DESC)`.

[View finding in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a20847-6f94-77ab-9712-d1e2cf3591bd/findings/01a20848-5d73-7154-846e-4a09ad806308)
