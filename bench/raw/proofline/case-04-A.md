# Raw review — provider: proofline · case 04 · condition A
PR: https://github.com/upreti-labs/run-proofline/pull/4 · base pilot/base · head pilot/04 · status completed

## Reviews (verbatim, in order received)

### review by prooflinedev[bot] · 2026-11-23T12:05:29Z · COMMENTED

<!-- proofline:review-comment -->
<!-- proofline:review-publication:e4a383a7-532f-4f02-bf21-4a2ac6c0d60f -->
**Proofline** has 1 new finding to review.

[View full review in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a20849-0cd6-75d6-bc23-8b93f2917781)

<!-- proofline:published-findings -->
<!-- proofline:published-finding-series=01a2084b-6828-7232-95ef-756d5f7382bf -->
<!-- proofline:published-thread-series=01a2084b-6828-7232-95ef-756d5f7382bf -->
<!-- /proofline:published-findings -->
<!-- proofline:published-code=01a2084b-682d-769e-9267-3ed45e555173 -->
<!-- proofline:published-code-thread=01a2084b-682d-769e-9267-3ed45e555173 -->

### inline comment by prooflinedev[bot] · 2026-11-23T12:05:29Z · migrations/002_retire_format.sql:1

<!-- proofline:finding-series=01a2084b-6828-7232-95ef-756d5f7382bf -->
**Warning** · First history page waits for a full table rewrite

On a version-1 database, `history --limit 1` runs the new column-drop migration before querying.

The first page waits for SQLite to rewrite all `deliveries` rows; before this change it fetched at most two rows without a rewrite.

Run the column drop as an explicit upgrade step rather than on the history request path.

[View finding in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a20849-0cd6-75d6-bc23-8b93f2917781/findings/01a2084b-682d-769e-9267-3ed45e555173)
