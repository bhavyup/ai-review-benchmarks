# Raw review — provider: sourcery · case 02 · condition A
PR: https://github.com/upreti-labs/run-sourcery/pull/2 · base pilot/base · head pilot/02 · status in_progress

## Reviews (verbatim, in order received)

### review by sourcery-ai[bot] · 2026-11-23T13:34:04Z · COMMENTED

Hey - I've found 2 issues

<details>
<summary>Prompt for AI Agents</summary>

~~~markdown
Please address the comments from this code review:

## Individual Comments

### Comment 1
<location path="reports.py" line_range="56" />
<code_context>
+    rows = db.execute("SELECT id, report, scheduled_at FROM deliveries ORDER BY id")
     for row in rows:
-        writer.writerow(row)
+        output.write(",".join(map(str, row)) + "\n")


</code_context>
<issue_to_address>
**Exports corrupt rows and risk formulas**

When a report name contains a comma, quote, or newline, especially a newline followed by a spreadsheet formula that an operator opens in spreadsheet software, `write_export` joins fields without CSV escaping, so consumers split fields or records incorrectly; an embedded newline can also start a row containing the formula, which spreadsheet software can execute.

Serialize each row with a CSV writer that correctly quotes and escapes its fields.
</issue_to_address>

### Comment 2
<location path="reports.py" line_range="54" />
<code_context>
-    writer.writerow(["id", "report", "scheduled_at"])
-    rows = db.execute("SELECT id, report, scheduled_at FROM deliveries ORDER BY id").fetchall()
+    output.write("id,report,scheduled_at\n")
+    rows = db.execute("SELECT id, report, scheduled_at FROM deliveries ORDER BY id")
     for row in rows:
-        writer.writerow(row)
</code_context>
<issue_to_address>
**Concurrent writes fail during exports**

When a slow or large export keeps the SELECT cursor open while another process schedules or delivers a report, `write_export` holds SQLite's read lock while writing rows, preventing the concurrent transaction from committing; after the lock timeout, the write fails with `database is locked`.

Fetch all rows before writing them so the SELECT cursor is no longer active during output.
</issue_to_address>
~~~

</details>

### Sourcery assessment

**Needs a human reviewer.** 2 findings to address first, and fields containing commas, quotes, or newlines are no longer escaped, so the export can be parsed into incorrect columns or rows. The source records remain intact and the export can be regenerated, though reverting alone would not fix files already produced.

Blocking findings: `reports.py:56`, `reports.py:54`

***

Your trial expires on December 7, 2026. Please [upgrade](https://app.sourcery.ai/dashboard/billing?connection=github&owner=upreti-labs&from_surface=github_bot&intent=trial_upgrade) to continue using Sourcery ✨

### inline comment by sourcery-ai[bot] · 2026-11-23T13:34:05Z · reports.py:56

**🟠 High · Exports corrupt rows and risk formulas**

When a report name contains a comma, quote, or newline, especially a newline followed by a spreadsheet formula that an operator opens in spreadsheet software, `write_export` joins fields without CSV escaping, so consumers split fields or records incorrectly; an embedded newline can also start a row containing the formula, which spreadsheet software can execute.

Serialize each row with a CSV writer that correctly quotes and escapes its fields.

<details>
<summary>Prompt for AI agents</summary>

~~~markdown
In `reports.py` at line 56:

**Exports corrupt rows and risk formulas**

When a report name contains a comma, quote, or newline, especially a newline followed by a spreadsheet formula that an operator opens in spreadsheet software, `write_export` joins fields without CSV escaping, so consumers split fields or records incorrectly; an embedded newline can also start a row containing the formula, which spreadsheet software can execute.

Serialize each row with a CSV writer that correctly quotes and escapes its fields.
~~~

</details>

### inline comment by sourcery-ai[bot] · 2026-11-23T13:34:05Z · reports.py:54

**🟡 Medium · Concurrent writes fail during exports**

When a slow or large export keeps the SELECT cursor open while another process schedules or delivers a report, `write_export` holds SQLite's read lock while writing rows, preventing the concurrent transaction from committing; after the lock timeout, the write fails with `database is locked`.

Fetch all rows before writing them so the SELECT cursor is no longer active during output.

<details>
<summary>Prompt for AI agents</summary>

~~~markdown
In `reports.py` at line 54:

**Concurrent writes fail during exports**

When a slow or large export keeps the SELECT cursor open while another process schedules or delivers a report, `write_export` holds SQLite's read lock while writing rows, preventing the concurrent transaction from committing; after the lock timeout, the write fails with `database is locked`.

Fetch all rows before writing them so the SELECT cursor is no longer active during output.
~~~

</details>

### PR comment by sourcery-ai[bot] · 2026-11-23T13:31:32Z

<!-- Generated by sourcery-ai[bot]: start review_guide -->

## Reviewer's Guide

### Implementation

Write delivery rows incrementally instead of fetching the full result set before exporting.
- `reports.py` L3 (removed lines), L53-56

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
