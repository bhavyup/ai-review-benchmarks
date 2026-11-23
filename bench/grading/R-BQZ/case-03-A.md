# Raw review — provider: R-BQZ · case 03 · condition A
PR: https://github.com/upreti-labs/run-proofline/pull/3 · base pilot/base · head pilot/03 · status in_progress

## Reviews (verbatim, in order received)

### review by prooflinedev[bot] · 2026-11-23T12:02:29Z · COMMENTED

<!-- proofline:review-comment -->
<!-- proofline:review-publication:3bec9bf1-f32a-463d-a389-a61761d78133 -->
**Proofline** has 1 new finding to review.

[View full review in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a20848-7df7-72d6-8e9a-0253ae8e3ba1)

<!-- proofline:published-findings -->
<!-- proofline:published-finding-series=01a20849-395a-71f9-91ce-4b1fbfbcc595 -->
<!-- proofline:published-thread-series=01a20849-395a-71f9-91ce-4b1fbfbcc595 -->
<!-- /proofline:published-findings -->
<!-- proofline:published-code=01a20849-395d-711a-ba47-8e300dc87731 -->
<!-- proofline:published-code-thread=01a20849-395d-711a-ba47-8e300dc87731 -->

### inline comment by prooflinedev[bot] · 2026-11-23T12:02:30Z · reports.py:79

<!-- proofline:finding-series=01a20849-395a-71f9-91ce-4b1fbfbcc595 -->
**Warning** · Worker leaves the final partial batch undelivered

`deliver_due` only iterates over full batches of 20, despite the documented promise to deliver all due jobs in one invocation.

The final 1–19 jobs remain pending; if fewer than 20 jobs are due, `work` reports zero and delivers none.

Use `range(0, len(jobs), batch_size)` so the existing slice includes the final partial batch.

[View finding in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a20848-7df7-72d6-8e9a-0253ae8e3ba1/findings/01a20849-395d-711a-ba47-8e300dc87731)

Also at:
- [`console.py`](https://github.com/upreti-labs/run-proofline/blob/6cca1e909a083c5a7f3fefc60ba637c2c84c411c/console.py#L32-L35) lines 32 to 35
