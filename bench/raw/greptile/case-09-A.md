# Raw review — provider: greptile · case 09 · condition A
PR: https://github.com/upreti-labs/run-greptile/pull/12 · base pilot/base · head pilot/09 · status in_progress

## Reviews (verbatim, in order received)

### review by greptile-apps[bot] · 2026-11-23T14:07:43Z · COMMENTED

(no body)

### inline comment by greptile-apps[bot] · 2026-11-23T14:07:42Z · reports.py:27

<a href=""><img alt="P1" src="https://greptile-static-assets.s3.amazonaws.com/badges/p1.svg?v=9" align="top"></a> **Scheduled reports are lost.** The console opens a default SQLite connection and calls `schedule` without committing afterward. SQLite starts a transaction for this insert; removing `with db:` leaves it uncommitted. The command prints an ID, then closes the connection and discards the delivery, so the worker never sees it. Restore the commit boundary before returning success.

### PR comment by greptile-apps[bot] · 2026-11-23T14:07:39Z

<!-- greptile_summary -->

<h2><a href="https://app.greptile.com/api/retrigger?id=116632231&amp;sig=85f8dd75606ac636b45c8384712587d812f3c56d1bb219b9c23a946e8a16ac2a"><picture><source media="(prefers-color-scheme: dark)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/RetriggerDark.svg?v=2"><source media="(prefers-color-scheme: light)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/Retrigger.svg?v=2"><img alt="Retrigger" src="https://greptile-static-assets.s3.amazonaws.com/badges/Retrigger.svg?v=2" align="right"></picture></a><a href="https://app.greptile.com/-/switch-tenant?tenant=upreti-labs&amp;next=%2Fupreti-labs%2Frun-greptile%2Fpull%2F12&amp;utm_source=greptile_review&amp;utm_medium=github&amp;utm_campaign=view_in_greptile"><picture><source media="(prefers-color-scheme: dark)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptileDark.svg?v=2"><source media="(prefers-color-scheme: light)" srcset="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptile.svg?v=2"><img alt="View in Greptile" src="https://greptile-static-assets.s3.amazonaws.com/badges/ViewInGreptile.svg?v=2" align="right"></picture></a>Confidence Score: 4/5</h2>

**[Medium impact]** The change reaches the report\-scheduling workflow and callers that use it\.

Restore the commit before merging so scheduled reports reach the worker.

<h2>Findings</h2>

1. <img alt="P1" src="https://greptile-static-assets.s3.amazonaws.com/badges/p1.svg?v=9" align="top">&nbsp;**Scheduled reports are lost** <a href="https://github.com/upreti-labs/run-greptile/pull/12#discussion_r4666904806">▶</a>

<h3>Summary</h3>

The PR removes the database context block from report scheduling.

- Report scheduling now leaves transaction control to its caller.

<!-- greptile_confidence_score:4 -->

<sub>Reviews (1) · Last reviewed commit: ["Simplify report scheduling"](https://github.com/upreti-labs/run-greptile/commit/c4a7c1df8dc6ac544a352be491e4a980f2e093cc) · [Reviewed by Greptile](https://www.greptile.com/?utm_source=greptile_review&utm_medium=github&utm_campaign=review_private)</sub>
