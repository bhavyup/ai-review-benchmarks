# Raw review — provider: R-NSD · case 05 · condition A
PR: https://github.com/upreti-labs/run-greptile/pull/5 · base pilot/base · head pilot/05 · status completed

## Reviews (verbatim, in order received)

### PR comment by greptile-apps[bot] · 2026-11-23T12:44:13Z

<!-- greptile_summary -->

<h2><a href="https://app.greptile.com/api/retrigger?id=116557145&amp;sig=f5f1824f25e13beabe27cb6c9b6863d5645cc2673ac330c0208997675975821e"><picture><source media="(prefers-color-scheme: dark)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/RetriggerDark.svg?v=2"><source media="(prefers-color-scheme: light)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/Retrigger.svg?v=2"><img alt="Retrigger" src="https://greptile-static-assets.s3.amazonaws.com/badges/Retrigger.svg?v=2" align="right"></picture></a><a href="https://app.greptile.com/-/switch-tenant?tenant=upreti-labs&amp;next=%2Fupreti-labs%2Frun-greptile%2Fpull%2F5&amp;utm_source=greptile_review&amp;utm_medium=github&amp;utm_campaign=view_in_greptile"><picture><source media="(prefers-color-scheme: dark)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptileDark.svg?v=2"><source media="(prefers-color-scheme: light)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptile.svg?v=2"><img alt="View in Greptile" src="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptile.svg?v=2" align="right"></picture></a>Confidence Score: 5/5</h2>

**[Low impact]** This change appears safe to merge.

<h3>Summary</h3>

Increases archive exports from 25 to 50 records per request, reducing calls for larger exports.

- Archive requests now carry up to 50 delivery records.

No actionable issues found.

<!-- greptile_confidence_score:5 -->

<sub>Reviews (1) · Last reviewed commit: ["Increase export batch size"](https://github.com/upreti-labs/run-greptile/commit/1f6f2a4d891c1481ae09c816fac4edcf361c45f1) · [Reviewed by Greptile](https://www.greptile.com/?utm_source=greptile_review&utm_medium=github&utm_campaign=review_private)</sub>
