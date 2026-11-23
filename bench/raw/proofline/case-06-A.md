# Raw review — provider: proofline · case 06 · condition A
PR: https://github.com/upreti-labs/run-proofline/pull/6 · base pilot/base · head pilot/06 · status completed

## Reviews (verbatim, in order received)

### review by prooflinedev[bot] · 2026-11-23T12:04:08Z · COMMENTED

<!-- proofline:review-comment -->
<!-- proofline:review-publication:5a40f27a-2c66-4a9d-bd03-f874f7d57786 -->
**Proofline** has 1 new finding to review.

[View full review in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a2084a-1054-76a2-aed9-0f3f2471f385)

<!-- proofline:published-findings -->
<!-- proofline:published-finding-series=01a2084a-bbdb-7224-a835-13c7b92ec705 -->
<!-- proofline:published-thread-series=01a2084a-bbdb-7224-a835-13c7b92ec705 -->
<!-- /proofline:published-findings -->
<!-- proofline:published-code=01a2084a-bbde-7568-a2f3-fd5066bd79b7 -->
<!-- proofline:published-code-thread=01a2084a-bbde-7568-a2f3-fd5066bd79b7 -->

### inline comment by prooflinedev[bot] · 2026-11-23T12:04:08Z · reports.py:9

<!-- proofline:finding-series=01a2084a-bbdb-7224-a835-13c7b92ec705 -->
**Warning** · Quickstart worker leaves the scheduled report pending

This change enqueues reports on `report-dispatch`, but the [`README.md`](https://github.com/upreti-labs/run-proofline/blob/fcb0c2a94196532d3d49af8d99d731474b00c1c2/README.md?plain=1#L6-L7) quickstart still runs the worker on `reports`.

On a fresh database, the documented worker prints `0` and leaves the due report pending.

Change the quickstart worker command to use `--queue report-dispatch`.

[View finding in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a2084a-1054-76a2-aed9-0f3f2471f385/findings/01a2084a-bbde-7568-a2f3-fd5066bd79b7)
