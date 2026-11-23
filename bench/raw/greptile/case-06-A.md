# Raw review — provider: greptile · case 06 · condition A
PR: https://github.com/upreti-labs/run-greptile/pull/6 · base pilot/base · head pilot/06 · status completed

## Reviews (verbatim, in order received)

### review by greptile-apps[bot] · 2026-11-23T12:44:43Z · COMMENTED

(no body)

### inline comment by greptile-apps[bot] · 2026-11-23T12:44:42Z · reports.py:9

<a href=""><img alt="P2" src="https://greptile-static-assets.s3.amazonaws.com/badges/p2.svg?v=9" align="top"></a> **Worker example skips new jobs.** `schedule` now writes `report-dispatch`, but the README still tells operators to run `work --queue reports`. Following that example schedules a job and then delivers zero jobs because `deliver_due` only reads the requested queue. Update the example to use `report-dispatch` and explain that operators should also drain `reports` for older jobs.

### PR comment by greptile-apps[bot] · 2026-11-23T12:44:39Z

<!-- greptile_summary -->

<h2><a href="https://app.greptile.com/api/retrigger?id=116557483&amp;sig=7a2c1e2dc2ec96bac8897ffaeeb8f6689f28e7acf3275c16260d02aff480a399"><picture><source media="(prefers-color-scheme: dark)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/RetriggerDark.svg?v=2"><source media="(prefers-color-scheme: light)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/Retrigger.svg?v=2"><img alt="Retrigger" src="https://greptile-static-assets.s3.amazonaws.com/badges/Retrigger.svg?v=2" align="right"></picture></a><a href="https://app.greptile.com/-/switch-tenant?tenant=upreti-labs&amp;next=%2Fupreti-labs%2Frun-greptile%2Fpull%2F6&amp;utm_source=greptile_review&amp;utm_medium=github&amp;utm_campaign=view_in_greptile"><picture><source media="(prefers-color-scheme: dark)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptileDark.svg?v=2"><source media="(prefers-color-scheme: light)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptile.svg?v=2"><img alt="View in Greptile" src="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptile.svg?v=2" align="right"></picture></a>Confidence Score: 4/5</h2>

**[Medium impact]** The change affects routing in the report scheduling and delivery workflow\.

The change appears safe to merge, with a non-blocking update needed for the worker example.

<h2>Findings</h2>

1. <img alt="P2" src="https://greptile-static-assets.s3.amazonaws.com/badges/p2.svg?v=9" align="top">&nbsp;**Worker example skips new jobs** <a href="https://github.com/upreti-labs/run-greptile/pull/6#discussion_r4665981325">▶</a>

<h3>Summary</h3>

Newly scheduled deliveries now use `report-dispatch`; existing jobs keep their assigned queue.

- New report deliveries use the `report-dispatch` queue.

<!-- greptile_confidence_score:4 -->

<sub>Reviews (1) · Last reviewed commit: ["Use the new delivery queue"](https://github.com/upreti-labs/run-greptile/commit/fcb0c2a94196532d3d49af8d99d731474b00c1c2) · [Reviewed by Greptile](https://www.greptile.com/?utm_source=greptile_review&utm_medium=github&utm_campaign=review_private)</sub>
