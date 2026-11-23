# Raw review — provider: R-BQZ · case 04 · condition B
PR: https://github.com/upreti-labs/run-proofline/pull/9 · base pilot/base · head pilot/04 · status in_progress

## Reviews (verbatim, in order received)

### review by prooflinedev[bot] · 2026-11-23T13:53:31Z · COMMENTED

<!-- proofline:review-comment -->
<!-- proofline:review-publication:9c7d532e-a62f-4853-ba8b-57fe001ef315 -->
**Proofline** has 3 new findings to review.

[View full review in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a208ad-086f-7569-a020-a6d18b80250b)

<!-- proofline:published-findings -->
<!-- proofline:published-finding-series=01a208ae-e14d-76f3-bbb8-d25eec64049d -->
<!-- proofline:published-thread-series=01a208ae-e14d-76f3-bbb8-d25eec64049d -->
<!-- proofline:published-finding-series=01a208ae-e14a-757c-8941-6c1bee153f8e -->
<!-- proofline:published-thread-series=01a208ae-e14a-757c-8941-6c1bee153f8e -->
<!-- proofline:published-finding-series=01a208ae-e14e-779b-8200-bf3194e8fa6c -->
<!-- proofline:published-thread-series=01a208ae-e14e-779b-8200-bf3194e8fa6c -->
<!-- /proofline:published-findings -->
<!-- proofline:published-code=01a208ae-e159-7210-8ec5-bf11afe04b20 -->
<!-- proofline:published-code-thread=01a208ae-e159-7210-8ec5-bf11afe04b20 -->
<!-- proofline:published-code=01a208ae-e151-76a1-bd89-a969a5346509 -->
<!-- proofline:published-code-thread=01a208ae-e151-76a1-bd89-a969a5346509 -->
<!-- proofline:published-code=01a208ae-e15e-77c4-b679-fdf9bf4c94da -->
<!-- proofline:published-code-thread=01a208ae-e15e-77c4-b679-fdf9bf4c94da -->

### inline comment by prooflinedev[bot] · 2026-11-23T13:53:31Z · migrations/002_retire_format.sql:1

<!-- proofline:finding-series=01a208ae-e14d-76f3-bbb8-d25eec64049d -->
**Serious** · Concurrent console runs can crash while applying migration 002

Two invocations can read `user_version = 1` before either commits. The second then tries to drop `legacy_format` after the first has removed it.

SQLite raises an error before the second invocation runs its command.

Acquire a SQLite write lock before reading `user_version`, and hold it through migration and the version update.

[View finding in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a208ad-086f-7569-a020-a6d18b80250b/findings/01a208ae-e159-7210-8ec5-bf11afe04b20)

### inline comment by prooflinedev[bot] · 2026-11-23T13:53:31Z · migrations/002_retire_format.sql:1

<!-- proofline:finding-series=01a208ae-e14a-757c-8941-6c1bee153f8e -->
**Warning** · First history page waits for a full deliveries rewrite

On a version-1 database, `history --limit 1` runs the new `DROP COLUMN` migration synchronously before fetching at most two rows.

The first request after upgrade waits for a rewrite whose I/O grows with the size of `deliveries`; before this change it only read the page.

Run the migration in an explicit upgrade step before serving history requests.

[View finding in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a208ad-086f-7569-a020-a6d18b80250b/findings/01a208ae-e151-76a1-bd89-a969a5346509)

### inline comment by prooflinedev[bot] · 2026-11-23T13:53:31Z · migrations/002_retire_format.sql:1

<!-- proofline:finding-series=01a208ae-e14e-779b-8200-bf3194e8fa6c -->
**Warning** · Migration 002 can make history fail during an archive

Migration `002` adds a schema write before `history` runs. In SQLite’s default rollback-journal mode, a stalled `archive` can hold a read lock beyond the migration’s busy timeout.

On a version-1 database, `history --limit 1` exits with `database is locked` instead of returning a page.

Run migration `002` in a separate upgrade step after active readers finish, rather than on `history` startup.

<details>
<summary>Details</summary>

Before this change, a version-1 database had no pending migration, so `history` could read alongside `archive`. With this change, if an already-running `archive` stalls in stdout with rows still unread, its cursor can retain a shared lock while the migration needs an exclusive lock to commit.

</details>

[View finding in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a208ad-086f-7569-a020-a6d18b80250b/findings/01a208ae-e15e-77c4-b679-fdf9bf4c94da)
