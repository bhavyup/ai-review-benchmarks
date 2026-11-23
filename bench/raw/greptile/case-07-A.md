# Raw review — provider: greptile · case 07 · condition A
PR: https://github.com/upreti-labs/run-greptile/pull/7 · base pilot/base · head pilot/07 · status in_progress

## Reviews (verbatim, in order received)

### PR comment by greptile-apps[bot] · 2026-11-23T12:44:58Z

<!-- greptile_summary -->

<h2><a href="https://app.greptile.com/api/retrigger?id=116557893&amp;sig=495ebbc21f3a161375678fbc734cf054e1b7d46f9a83be13b9dac0c63835c88d"><picture><source media="(prefers-color-scheme: dark)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/RetriggerDark.svg?v=2"><source media="(prefers-color-scheme: light)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/Retrigger.svg?v=2"><img alt="Retrigger" src="https://greptile-static-assets.s3.amazonaws.com/badges/Retrigger.svg?v=2" align="right"></picture></a><a href="https://app.greptile.com/-/switch-tenant?tenant=upreti-labs&amp;next=%2Fupreti-labs%2Frun-greptile%2Fpull%2F7&amp;utm_source=greptile_review&amp;utm_medium=github&amp;utm_campaign=view_in_greptile"><picture><source media="(prefers-color-scheme: dark)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptileDark.svg?v=2"><source media="(prefers-color-scheme: light)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptile.svg?v=2"><img alt="View in Greptile" src="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptile.svg?v=2" align="right"></picture></a>Confidence Score: 5/5</h2>

**[Low impact]** This PR appears safe to merge; no actionable issues were found.

<h3>Summary</h3>

Adds a partial index to speed up finding pending deliveries by queue and scheduled time.

- The report worker has an index for finding due jobs by queue and time.

No actionable issues found.

<!-- greptile_confidence_score:5 -->

<sub>Reviews (1) · Last reviewed commit: ["Index pending deliveries"](https://github.com/upreti-labs/run-greptile/commit/68ef658388c5cc9ec890d030918fb6a0b36ea369) · [Reviewed by Greptile](https://www.greptile.com/?utm_source=greptile_review&utm_medium=github&utm_campaign=review_private)</sub>
