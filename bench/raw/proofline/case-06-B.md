# Raw review — provider: proofline · case 06 · condition B
PR: https://github.com/upreti-labs/run-proofline/pull/10 · base pilot/base · head pilot/06 · status in_progress

## Reviews (verbatim, in order received)

### review by prooflinedev[bot] · 2026-11-23T13:53:09Z · COMMENTED

<!-- proofline:review-comment -->
<!-- proofline:review-publication:9d997c16-a753-4a08-9104-0c6c73e5419a -->
**Proofline** has 1 new finding to review.

[View full review in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a208ad-e81e-7540-838b-f647b8b6a7d7)

<!-- proofline:published-findings -->
<!-- proofline:published-finding-series=01a208ae-8c56-7287-b996-8fe66ceb7803 -->
<!-- proofline:published-thread-series=01a208ae-8c56-7287-b996-8fe66ceb7803 -->
<!-- /proofline:published-findings -->
<!-- proofline:published-code=01a208ae-8c65-70a0-8e7b-2fddf052da9f -->
<!-- proofline:published-code-thread=01a208ae-8c65-70a0-8e7b-2fddf052da9f -->

### inline comment by prooflinedev[bot] · 2026-11-23T13:53:10Z · reports.py:9

<!-- proofline:finding-series=01a208ae-8c56-7287-b996-8fe66ceb7803 -->
**Warning** · The quickstart worker leaves the scheduled report pending

This change schedules deliveries on `report-dispatch`, but the quickstart worker still selects only jobs on `reports`.

On a fresh database, the documented worker delivers zero jobs and leaves the scheduled report pending.

Update the worker command in [`README.md`](https://github.com/upreti-labs/run-proofline/blob/fcb0c2a94196532d3d49af8d99d731474b00c1c2/README.md?plain=1#L6-L8) to use `--queue report-dispatch`.

[View finding in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a208ad-e81e-7540-838b-f647b8b6a7d7/findings/01a208ae-8c65-70a0-8e7b-2fddf052da9f)
