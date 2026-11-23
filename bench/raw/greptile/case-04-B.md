# Raw review — provider: greptile · case 04 · condition B
PR: https://github.com/upreti-labs/run-greptile/pull/9 · base pilot/base · head pilot/04 · status in_progress

## Reviews (verbatim, in order received)

### review by greptile-apps[bot] · 2026-11-23T13:38:16Z · COMMENTED

(no body)

### inline comment by greptile-apps[bot] · 2026-11-23T13:38:15Z · migrations/002_retire_format.sql:1

<a href=""><img alt="P1" src="https://greptile-static-assets.s3.amazonaws.com/badges/p1.svg?v=9" align="top"></a> **Older workers stop polling.** The supplied inventory lists two active `workers-17` replicas at elm that still run `SELECT id, legacy_format FROM deliveries WHERE delivered_at IS NULL`. Dropping `legacy_format` makes those reads fail while the replicas continue running. Upgrade or stop every reader of this column at elm before applying the migration there. The listed `workers-18` replicas do not reference the removed column.

### PR comment by greptile-apps[bot] · 2026-11-23T13:38:12Z

<!-- greptile_summary -->

<h2><a href="https://app.greptile.com/api/retrigger?id=116605461&amp;sig=078e2a077c5bc234222ec44defd9299683cacdef8a0106165f7ad1d6b218bc00"><picture><source media="(prefers-color-scheme: dark)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/RetriggerDark.svg?v=2"><source media="(prefers-color-scheme: light)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/Retrigger.svg?v=2"><img alt="Retrigger" src="https://greptile-static-assets.s3.amazonaws.com/badges/Retrigger.svg?v=2" align="right"></picture></a><a href="https://app.greptile.com/-/switch-tenant?tenant=upreti-labs&amp;next=%2Fupreti-labs%2Frun-greptile%2Fpull%2F9&amp;utm_source=greptile_review&amp;utm_medium=github&amp;utm_campaign=view_in_greptile"><picture><source media="(prefers-color-scheme: dark)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptileDark.svg?v=2"><source media="(prefers-color-scheme: light)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptile.svg?v=2"><img alt="View in Greptile" src="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptile.svg?v=2" align="right"></picture></a>Confidence Score: 4/5</h2>

**[Medium impact]** The migration changes the deliveries schema while workers are polling\.

Do not merge until the older workers at elm are upgraded or stopped before the migration runs.

<h2>Findings</h2>

1. <img alt="P1" src="https://greptile-static-assets.s3.amazonaws.com/badges/p1.svg?v=9" align="top">&nbsp;**Older workers stop polling** <a href="https://github.com/upreti-labs/run-greptile/pull/9#discussion_r4666563169">▶</a>

<h3>Summary</h3>

Removes `legacy_format` from `deliveries`.

- The deliveries table drops its old format field.

<!-- greptile_confidence_score:4 -->

<sub>Reviews (1) · Last reviewed commit: ["Retire the legacy delivery column"](https://github.com/upreti-labs/run-greptile/commit/420baea889887b127f1c87d99f728e40f7664996) · [Reviewed by Greptile](https://www.greptile.com/?utm_source=greptile_review&utm_medium=github&utm_campaign=review_private)</sub>
