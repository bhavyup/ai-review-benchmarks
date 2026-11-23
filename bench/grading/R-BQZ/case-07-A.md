# Raw review — provider: R-BQZ · case 07 · condition A
PR: https://github.com/upreti-labs/run-proofline/pull/7 · base pilot/base · head pilot/07 · status in_progress

## Reviews (verbatim, in order received)

### review by prooflinedev[bot] · 2026-11-23T12:05:49Z · COMMENTED

<!-- proofline:review-comment -->
<!-- proofline:review-publication:903b4dcd-ea73-4334-9898-b0fff2473563 -->
**Proofline** has 2 new findings to review.

[View full review in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a2084a-a581-743f-a0c4-2428bd14ed03)

<!-- proofline:published-findings -->
<!-- proofline:published-finding-series=01a2084c-46e3-74ab-beb9-57e96286f158 -->
<!-- proofline:published-thread-series=01a2084c-46e3-74ab-beb9-57e96286f158 -->
<!-- proofline:published-finding-series=01a2084c-46e4-767b-b5ea-c283efde8057 -->
<!-- proofline:published-thread-series=01a2084c-46e4-767b-b5ea-c283efde8057 -->
<!-- /proofline:published-findings -->
<!-- proofline:published-code=01a2084c-46e5-7031-bf3d-caa1fc1db3a4 -->
<!-- proofline:published-code-thread=01a2084c-46e5-7031-bf3d-caa1fc1db3a4 -->
<!-- proofline:published-code=01a2084c-46ea-7198-bb7d-b03e648c26ae -->
<!-- proofline:published-code-thread=01a2084c-46ea-7198-bb7d-b03e648c26ae -->

### inline comment by prooflinedev[bot] · 2026-11-23T12:05:49Z · migrations/002_pending_by_queue.sql:1

<!-- proofline:finding-series=01a2084c-46e3-74ab-beb9-57e96286f158 -->
**Warning** · Concurrent upgrades can abort a console command

Two commands upgrading the same version-1 database can both see `002` as pending. After one commits, the other tries to create `deliveries_due_by_queue` again.

The second command exits with an index-already-exists error before dispatch.

Acquire the write lock with `BEGIN IMMEDIATE`, then recheck `user_version` before applying migrations in that same transaction.

[View finding in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a2084a-a581-743f-a0c4-2428bd14ed03/findings/01a2084c-46e5-7031-bf3d-caa1fc1db3a4)

### inline comment by prooflinedev[bot] · 2026-11-23T12:05:49Z · migrations/002_pending_by_queue.sql:2

<!-- proofline:finding-series=01a2084c-46e4-767b-b5ea-c283efde8057 -->
**Warning** · History can fail during upgrade while archive output is stalled

Migration 002 requires `history` to commit an index creation before reading. In SQLite’s default rollback-journal mode, a stalled `archive` can hold a read lock past the migration’s busy timeout.

`history` exits with a database-locked error instead of returning a page.

Move index creation to an explicit upgrade step and let read-only commands run against version 1.

<details>
<summary>Details</summary>

Before this change, a version-1 database had no pending migration, so `history` and `archive` could both read. The old `archive` keeps its SELECT cursor open while sending batches. A single invocation of the new CLI is enough to hit the lock timeout; no competing migration is required.

</details>

[View finding in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a2084a-a581-743f-a0c4-2428bd14ed03/findings/01a2084c-46ea-7198-bb7d-b03e648c26ae)
