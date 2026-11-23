# Raw review — provider: greptile · case 06 · condition B
PR: https://github.com/upreti-labs/run-greptile/pull/11 · base pilot/base · head pilot/06 · status in_progress

## Reviews (verbatim, in order received)

### review by greptile-apps[bot] · 2026-11-23T13:40:14Z · COMMENTED

(no body)

### inline comment by greptile-apps[bot] · 2026-11-23T13:40:13Z · reports.py:9

<a href=""><img alt="P1" src="https://greptile-static-assets.s3.amazonaws.com/badges/p1.svg?v=9" align="top"></a> **Elm deliveries stop running.** `schedule` now puts every new job on `report-dispatch`, but the supplied inventory shows Elm consumes only `reports` throughout the observation window. `deliver_due` matches queue names exactly, so Elm's eight newly scheduled deliveries remain pending through 09:30. Add the new subscription at Elm before switching its scheduling, or keep that site on `reports` until its workers are ready. Keep the old subscription for existing jobs.

### PR comment by greptile-apps[bot] · 2026-11-23T13:40:10Z

<!-- greptile_summary -->

<h2><a href="https://app.greptile.com/api/retrigger?id=116607264&amp;sig=d14b67460d41366638959bf8f0f97959b2cd88222c361d2dd695dd68fc406ccc"><picture><source media="(prefers-color-scheme: dark)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/RetriggerDark.svg?v=2"><source media="(prefers-color-scheme: light)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/Retrigger.svg?v=2"><img alt="Retrigger" src="https://greptile-static-assets.s3.amazonaws.com/badges/Retrigger.svg?v=2" align="right"></picture></a><a href="https://app.greptile.com/-/switch-tenant?tenant=upreti-labs&amp;next=%2Fupreti-labs%2Frun-greptile%2Fpull%2F11&amp;utm_source=greptile_review&amp;utm_medium=github&amp;utm_campaign=view_in_greptile"><picture><source media="(prefers-color-scheme: dark)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptileDark.svg?v=2"><source media="(prefers-color-scheme: light)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptile.svg?v=2"><img alt="View in Greptile" src="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptile.svg?v=2" align="right"></picture></a>Confidence Score: 4/5</h2>

**[Medium impact]** The queue change affects every newly scheduled report and which workers can pick it up\.

Block merging until Elm can consume the new queue or keeps scheduling on its current queue.

<h2>Findings</h2>

1. <img alt="P1" src="https://greptile-static-assets.s3.amazonaws.com/badges/p1.svg?v=9" align="top">&nbsp;**Elm deliveries stop running** <a href="https://github.com/upreti-labs/run-greptile/pull/11#discussion_r4666585249">▶</a>

<h3>Summary</h3>

Newly scheduled deliveries now use `report-dispatch`; existing jobs keep their assigned queues.

- New report deliveries use the dedicated dispatch queue.

<!-- greptile_confidence_score:4 -->

<sub>Reviews (1) · Last reviewed commit: ["Use the new delivery queue"](https://github.com/upreti-labs/run-greptile/commit/fcb0c2a94196532d3d49af8d99d731474b00c1c2) · [Reviewed by Greptile](https://www.greptile.com/?utm_source=greptile_review&utm_medium=github&utm_campaign=review_private)</sub>
