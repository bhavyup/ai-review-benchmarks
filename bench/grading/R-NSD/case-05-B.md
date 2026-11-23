# Raw review — provider: R-NSD · case 05 · condition B
PR: https://github.com/upreti-labs/run-greptile/pull/10 · base pilot/base · head pilot/05 · status in_progress

## Reviews (verbatim, in order received)

### review by greptile-apps[bot] · 2026-11-23T13:39:08Z · COMMENTED

(no body)

### inline comment by greptile-apps[bot] · 2026-11-23T13:39:07Z · reports.py:10

<a href=""><img alt="P1" src="https://greptile-static-assets.s3.amazonaws.com/badges/p1.svg?v=9" align="top"></a> **Cedar rejects larger exports.** Cedar has 70 ready records and accepts at most 40 per request. With `EXPORT_BATCH_SIZE = 50`, `export_to_sink` sends its first 50 records in one request, which Cedar rejects in full. Previously, requests of 25, 25, and 20 records all fit. Keep requests within each receiver’s limit, or retain a shared size that both sites accept.

### PR comment by greptile-apps[bot] · 2026-11-23T13:39:04Z

<!-- greptile_summary -->

<h2><a href="https://app.greptile.com/api/retrigger?id=116606401&amp;sig=3aef8c4dae5d4c556ee3fe10f777db55eef2742cfb2fd1dbe7faf1813d2bb3a3"><picture><source media="(prefers-color-scheme: dark)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/RetriggerDark.svg?v=2"><source media="(prefers-color-scheme: light)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/Retrigger.svg?v=2"><img alt="Retrigger" src="https://greptile-static-assets.s3.amazonaws.com/badges/Retrigger.svg?v=2" align="right"></picture></a><a href="https://app.greptile.com/-/switch-tenant?tenant=upreti-labs&amp;next=%2Fupreti-labs%2Frun-greptile%2Fpull%2F10&amp;utm_source=greptile_review&amp;utm_medium=github&amp;utm_campaign=view_in_greptile"><picture><source media="(prefers-color-scheme: dark)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptileDark.svg?v=2"><source media="(prefers-color-scheme: light)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptile.svg?v=2"><img alt="View in Greptile" src="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptile.svg?v=2" align="right"></picture></a>Confidence Score: 4/5</h2>

**[Medium impact]** The change affects archive exports and interacts with receiver request limits\.

Do not merge until archive requests stay within Cedar’s limit.

<h2>Findings</h2>

1. <img alt="P1" src="https://greptile-static-assets.s3.amazonaws.com/badges/p1.svg?v=9" align="top">&nbsp;**Cedar rejects larger exports** <a href="https://github.com/upreti-labs/run-greptile/pull/10#discussion_r4666572839">▶</a>

<h3>Summary</h3>

The PR increases archive requests from 25 to 50 records to reduce export calls.

- Archive requests now carry up to 50 report records.

<!-- greptile_confidence_score:4 -->

<sub>Reviews (1) · Last reviewed commit: ["Increase export batch size"](https://github.com/upreti-labs/run-greptile/commit/1f6f2a4d891c1481ae09c816fac4edcf361c45f1) · [Reviewed by Greptile](https://www.greptile.com/?utm_source=greptile_review&utm_medium=github&utm_campaign=review_private)</sub>
