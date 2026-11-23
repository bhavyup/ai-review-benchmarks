# Raw review — provider: R-BQZ · case 09 · condition A
PR: https://github.com/upreti-labs/run-proofline/pull/11 · base pilot/base · head pilot/09 · status in_progress

## Reviews (verbatim, in order received)

### review by prooflinedev[bot] · 2026-11-23T14:06:57Z · COMMENTED

<!-- proofline:review-comment -->
<!-- proofline:review-publication:126be4d5-fced-4e0c-aa99-5f60dcc58d85 -->
**Proofline** has 1 new finding to review.

[View full review in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a208ba-5525-7285-8081-aefa03a362b4)

<!-- proofline:published-findings -->
<!-- proofline:published-finding-series=01a208bb-2b5d-758b-b89d-07099b3a27b8 -->
<!-- proofline:published-thread-series=01a208bb-2b5d-758b-b89d-07099b3a27b8 -->
<!-- /proofline:published-findings -->
<!-- proofline:published-code=01a208bb-2b62-73e2-bbb3-4857402f82ab -->
<!-- proofline:published-code-thread=01a208bb-2b62-73e2-bbb3-4857402f82ab -->

### inline comment by prooflinedev[bot] · 2026-11-23T14:06:57Z · reports.py:26

<!-- proofline:finding-series=01a208bb-2b5d-758b-b89d-07099b3a27b8 -->
**Serious** · Scheduling prints an ID but discards the delivery

This change removes the commit from `schedule`, so the CLI closes the SQLite connection with the insert still pending.

The CLI prints a delivery ID, but the row is rolled back and a later worker cannot deliver it.

Restore the transaction context in `schedule` so the insert commits before the ID is returned.

[View finding in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a208ba-5525-7285-8081-aefa03a362b4/findings/01a208bb-2b62-73e2-bbb3-4857402f82ab)
