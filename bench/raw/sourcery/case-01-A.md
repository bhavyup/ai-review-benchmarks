# Raw review — provider: sourcery · case 01 · condition A
PR: https://github.com/upreti-labs/run-sourcery/pull/1 · base pilot/base · head pilot/01 · status in_progress

## Reviews (verbatim, in order received)

### review by sourcery-ai[bot] · 2026-11-23T13:33:11Z · COMMENTED

Hey - I've found 3 issues

<details>
<summary>Prompt for AI Agents</summary>

~~~markdown
Please address the comments from this code review:

## Individual Comments

### Comment 1
<location path="reports.py" line_range="45" />
<code_context>
     params = []
     if cursor is not None:
-        query += " WHERE id < ?"
+        query += " WHERE scheduled_at < ?"
         params.append(cursor)
-    query += " ORDER BY id DESC LIMIT ?"
</code_context>
<issue_to_address>
**Later pages omit tied deliveries**

When multiple deliveries share a scheduled time across a page boundary, the timestamp-only cursor filter excludes the remaining deliveries at that timestamp, even though the ordering uses `id` to distinguish them, so callers see incomplete history.

Use both `scheduled_at` and `id` in the cursor and next-page boundary.

Also at `reports.py:49`.
</issue_to_address>

### Comment 2
<location path="reports.py" line_range="45-49" />
<code_context>
     params = []
     if cursor is not None:
-        query += " WHERE id < ?"
+        query += " WHERE scheduled_at < ?"
         params.append(cursor)
-    query += " ORDER BY id DESC LIMIT ?"
+    query += " ORDER BY scheduled_at DESC, id DESC LIMIT ?"
     rows = db.execute(query, (*params, limit + 1)).fetchall()
-    next_cursor = rows[limit - 1][0] if len(rows) > limit else None
+    next_cursor = rows[limit - 1][2] if len(rows) > limit else None
     return HistoryPage(rows[:limit], next_cursor)

</code_context>
<issue_to_address>
**Saved cursors stop paging**

When a cursor returned by the previous version is reused after an upgrade or against a new-version instance, the new query treats the supplied cursor as a scheduled time, so a cursor saved by the previous version—which contained a delivery ID—is interpreted as a timestamp; with normal Unix-second schedules, the next page is empty.

Version or otherwise distinguish cursor formats, and handle prior-version cursors during the compatibility window.
</issue_to_address>

### Comment 3
<location path="reports.py" line_range="47" />
<code_context>
+        query += " WHERE scheduled_at < ?"
         params.append(cursor)
-    query += " ORDER BY id DESC LIMIT ?"
+    query += " ORDER BY scheduled_at DESC, id DESC LIMIT ?"
     rows = db.execute(query, (*params, limit + 1)).fetchall()
-    next_cursor = rows[limit - 1][0] if len(rows) > limit else None
</code_context>
<issue_to_address>
**History pages get slower**

When the deliveries table grows, sQLite has no index starting with `scheduled_at`, so the new ordering and cursor filter require scanning the deliveries table and sorting rows for each page; history requests become increasingly expensive as deliveries accumulate.

Add a migration creating an index on `(scheduled_at, id)` to support the history filter and ordering.
</issue_to_address>
~~~

</details>

### Sourcery assessment

**Approval pending.** 3 findings to address first.

Blocking findings: `reports.py:45`, `reports.py:49`, `reports.py:47`

***

Your trial expires on December 7, 2026. Please [upgrade](https://app.sourcery.ai/dashboard/billing?connection=github&owner=upreti-labs&from_surface=github_bot&intent=trial_upgrade) to continue using Sourcery ✨

### inline comment by sourcery-ai[bot] · 2026-11-23T13:33:11Z · reports.py:45

**🟠 High · Later pages omit tied deliveries**

When multiple deliveries share a scheduled time across a page boundary, the timestamp-only cursor filter excludes the remaining deliveries at that timestamp, even though the ordering uses `id` to distinguish them, so callers see incomplete history.

Use both `scheduled_at` and `id` in the cursor and next-page boundary.

Also at `reports.py:49`.

<details>
<summary>Prompt for AI agents</summary>

~~~markdown
In `reports.py` at line 45:

**Later pages omit tied deliveries**

When multiple deliveries share a scheduled time across a page boundary, the timestamp-only cursor filter excludes the remaining deliveries at that timestamp, even though the ordering uses `id` to distinguish them, so callers see incomplete history.

Use both `scheduled_at` and `id` in the cursor and next-page boundary.

Also at `reports.py:49`.
~~~

</details>

### inline comment by sourcery-ai[bot] · 2026-11-23T13:33:12Z · reports.py:49

**🟡 Medium · Saved cursors stop paging**

When a cursor returned by the previous version is reused after an upgrade or against a new-version instance, the new query treats the supplied cursor as a scheduled time, so a cursor saved by the previous version—which contained a delivery ID—is interpreted as a timestamp; with normal Unix-second schedules, the next page is empty.

Version or otherwise distinguish cursor formats, and handle prior-version cursors during the compatibility window.

<details>
<summary>Prompt for AI agents</summary>

~~~markdown
In `reports.py` at lines 45-49:

**Saved cursors stop paging**

When a cursor returned by the previous version is reused after an upgrade or against a new-version instance, the new query treats the supplied cursor as a scheduled time, so a cursor saved by the previous version—which contained a delivery ID—is interpreted as a timestamp; with normal Unix-second schedules, the next page is empty.

Version or otherwise distinguish cursor formats, and handle prior-version cursors during the compatibility window.
~~~

</details>

### inline comment by sourcery-ai[bot] · 2026-11-23T13:33:12Z · reports.py:47

**🟡 Medium · History pages get slower**

When the deliveries table grows, sQLite has no index starting with `scheduled_at`, so the new ordering and cursor filter require scanning the deliveries table and sorting rows for each page; history requests become increasingly expensive as deliveries accumulate.

Add a migration creating an index on `(scheduled_at, id)` to support the history filter and ordering.

<details>
<summary>Prompt for AI agents</summary>

~~~markdown
In `reports.py` at line 47:

**History pages get slower**

When the deliveries table grows, sQLite has no index starting with `scheduled_at`, so the new ordering and cursor filter require scanning the deliveries table and sorting rows for each page; history requests become increasingly expensive as deliveries accumulate.

Add a migration creating an index on `(scheduled_at, id)` to support the history filter and ordering.
~~~

</details>

### PR comment by sourcery-ai[bot] · 2026-11-23T13:31:11Z

<!-- Generated by sourcery-ai[bot]: start review_guide -->

## Reviewer's Guide

### Implementation

Order report history by scheduled time and use the scheduled time as the cursor for fetching the next page.
- `reports.py` L45-49

---

<details>
<summary>Tips and commands</summary>

#### Interacting with Sourcery

- **Trigger a new review:** Comment `@sourcery-ai review` on the pull request.
- **Continue discussions:** Reply directly to Sourcery's review comments.
- **Generate a GitHub issue from a review comment:** Ask Sourcery to create an
  issue from a review comment by replying to it. You can also reply to a
  review comment with `@sourcery-ai issue` to create an issue from it.
- **Generate a pull request title:** Write `@sourcery-ai` anywhere in the pull
  request title to generate a title at any time. You can also comment
  `@sourcery-ai title` on the pull request to (re-)generate the title at any time.
- **Generate a pull request summary:** Write `@sourcery-ai summary` anywhere in
  the pull request body to generate a PR summary at any time exactly where you
  want it. You can also comment `@sourcery-ai summary` on the pull request to
  (re-)generate the summary at any time.
- **Generate reviewer's guide:** Comment `@sourcery-ai guide` on the pull
  request to (re-)generate the reviewer's guide at any time.
- **Resolve all Sourcery comments:** Comment `@sourcery-ai resolve` on the
  pull request to resolve all Sourcery comments. Useful if you've already
  addressed all the comments and don't want to see them anymore.
- **Dismiss all Sourcery reviews:** Comment `@sourcery-ai dismiss` on the pull
  request to dismiss all existing Sourcery reviews. Especially useful if you
  want to start fresh with a new review - don't forget to comment
  `@sourcery-ai review` to trigger a new review!

#### Customizing Your Experience

Access your [dashboard](https://app.sourcery.ai/dashboard/review-settings?connection=github&owner=upreti-labs&from_surface=github_bot&intent=review_settings) to:
- Enable or disable review features such as the Sourcery-generated pull request
  summary, the reviewer's guide, and others.
- Change the review language.
- Add, remove or edit custom review instructions.
- Adjust other review settings.

#### Getting Help

- [Contact our support team](mailto:support@sourcery.ai) for questions or feedback.
- Visit our [documentation](https://docs.sourcery.ai) for detailed guides and information.
- Keep in touch with the Sourcery team by following us on [X/Twitter](https://x.com/SourceryAI), [LinkedIn](https://www.linkedin.com/company/sourcery-ai/) or [GitHub](https://github.com/sourcery-ai).

</details>

<!-- Generated by sourcery-ai[bot]: end review_guide -->
