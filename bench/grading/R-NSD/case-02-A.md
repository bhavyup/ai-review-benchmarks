# Raw review — provider: R-NSD · case 02 · condition A
PR: https://github.com/upreti-labs/run-greptile/pull/2 · base pilot/base · head pilot/02 · status in_progress

## Reviews (verbatim, in order received)

### review by greptile-apps[bot] · 2026-11-23T12:42:54Z · COMMENTED

(no body)

### inline comment by greptile-apps[bot] · 2026-11-23T12:42:53Z · reports.py:56

<a href=""><img alt="P1" src="https://greptile-static-assets.s3.amazonaws.com/badges/p1.svg?v=9" align="top"></a> **Report names break CSV rows.** A valid report name such as `Sales, Europe` now becomes two fields because `write_export` joins values without CSV quoting. Names containing line breaks also create extra records. The console accepts these names and `schedule` stores them unchanged.

Keep `csv.writer` and call `writer.writerow(row)` inside the cursor loop. This preserves streaming without changing the exported data.

### PR comment by greptile-apps[bot] · 2026-11-23T12:42:50Z

<!-- greptile_summary -->

<h2><a href="https://app.greptile.com/api/retrigger?id=116555926&amp;sig=574f1c7e66b7637bcf232bae38331d194ad5bb82f958559f6eeb91684c282908"><picture><source media="(prefers-color-scheme: dark)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/RetriggerDark.svg?v=2"><source media="(prefers-color-scheme: light)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/Retrigger.svg?v=2"><img alt="Retrigger" src="https://greptile-static-assets.s3.amazonaws.com/badges/Retrigger.svg?v=2" align="right"></picture></a><a href="https://app.greptile.com/-/switch-tenant?tenant=upreti-labs&amp;next=%2Fupreti-labs%2Frun-greptile%2Fpull%2F2&amp;utm_source=greptile_review&amp;utm_medium=github&amp;utm_campaign=view_in_greptile"><picture><source media="(prefers-color-scheme: dark)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptileDark.svg?v=2"><source media="(prefers-color-scheme: light)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptile.svg?v=2"><img alt="View in Greptile" src="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptile.svg?v=2" align="right"></picture></a>Confidence Score: 4/5</h2>

**[Medium impact]** The change reaches the report export workflow\.

Restore CSV-aware writing before merging so exported deliveries remain readable.

<h2>Findings</h2>

1. <img alt="P1" src="https://greptile-static-assets.s3.amazonaws.com/badges/p1.svg?v=9" align="top">&nbsp;**Report names break CSV rows** <a href="https://github.com/upreti-labs/run-greptile/pull/2#discussion_r4665962633">▶</a>

<h3>Summary</h3>

The export now writes deliveries as the database returns them instead of loading every row first.

- Report exports write each delivery as the database reads it.

<!-- greptile_confidence_score:4 -->

<sub>Reviews (1) · Last reviewed commit: ["Stream the report export"](https://github.com/upreti-labs/run-greptile/commit/9d551b83dc3a9b0c30868859ea97feef934e7b9b) · [Reviewed by Greptile](https://www.greptile.com/?utm_source=greptile_review&utm_medium=github&utm_campaign=review_private)</sub>
