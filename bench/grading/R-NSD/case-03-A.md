# Raw review — provider: R-NSD · case 03 · condition A
PR: https://github.com/upreti-labs/run-greptile/pull/3 · base pilot/base · head pilot/03 · status in_progress

## Reviews (verbatim, in order received)

### review by greptile-apps[bot] · 2026-11-23T12:43:09Z · COMMENTED

(no body)

### inline comment by greptile-apps[bot] · 2026-11-23T12:43:08Z · reports.py:78

<a href=""><img alt="P1" src="https://greptile-static-assets.s3.amazonaws.com/badges/p1.svg?v=9" align="top"></a> **Small queues never deliver.** The loop only visits full batches of twenty. With 1–19 due jobs, `deliver_due` does nothing and returns zero; with 21, it delivers twenty and leaves one pending. Repeated worker runs cannot deliver the remainder unless more jobs arrive. Use `range(0, len(jobs), batch_size)` so the final slice includes any remaining jobs.

### PR comment by greptile-apps[bot] · 2026-11-23T12:43:05Z

<!-- greptile_summary -->

<h2><a href="https://app.greptile.com/api/retrigger?id=116556280&amp;sig=b0fd6e8f24501d8bd06fde159a41231c401becdb8cb62c60d771e2f8896f80ac"><picture><source media="(prefers-color-scheme: dark)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/RetriggerDark.svg?v=2"><source media="(prefers-color-scheme: light)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/Retrigger.svg?v=2"><img alt="Retrigger" src="https://greptile-static-assets.s3.amazonaws.com/badges/Retrigger.svg?v=2" align="right"></picture></a><a href="https://app.greptile.com/-/switch-tenant?tenant=upreti-labs&amp;next=%2Fupreti-labs%2Frun-greptile%2Fpull%2F3&amp;utm_source=greptile_review&amp;utm_medium=github&amp;utm_campaign=view_in_greptile"><picture><source media="(prefers-color-scheme: dark)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptileDark.svg?v=2"><source media="(prefers-color-scheme: light)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptile.svg?v=2"><img alt="View in Greptile" src="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptile.svg?v=2" align="right"></picture></a>Confidence Score: 4/5</h2>

**[Medium impact]** The change affects delivery work for named queues\.

Fix the loop bounds before merging so small queues can deliver their reports.

<h2>Findings</h2>

1. <img alt="P1" src="https://greptile-static-assets.s3.amazonaws.com/badges/p1.svg?v=9" align="top">&nbsp;**Small queues never deliver** <a href="https://github.com/upreti-labs/run-greptile/pull/3#discussion_r4665965172">▶</a>

<h3>Summary</h3>

The PR batches receipt inserts and delivery updates in groups of twenty.

- The queue worker records due deliveries in batches of twenty.

The loop skips the final partial batch, leaving small queues undelivered.

<!-- greptile_confidence_score:4 -->

<sub>Reviews (1) · Last reviewed commit: ["Batch queued deliveries"](https://github.com/upreti-labs/run-greptile/commit/6cca1e909a083c5a7f3fefc60ba637c2c84c411c) · [Reviewed by Greptile](https://www.greptile.com/?utm_source=greptile_review&utm_medium=github&utm_campaign=review_private)</sub>
