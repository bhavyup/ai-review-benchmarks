# Raw review — provider: R-BQZ · case 02 · condition A
PR: https://github.com/upreti-labs/run-proofline/pull/2 · base pilot/base · head pilot/02 · status in_progress

## Reviews (verbatim, in order received)

### review by prooflinedev[bot] · 2026-11-23T12:02:07Z · COMMENTED

<!-- proofline:review-comment -->
<!-- proofline:review-publication:c563677e-a974-4458-93a9-a8b624789b4e -->
**Proofline** has 2 new findings to review.

[View full review in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a20848-0f01-75ea-92a7-00858c21be09)

<!-- proofline:published-findings -->
<!-- proofline:published-finding-series=01a20848-c199-76b0-82a5-c30dcd8f04bf -->
<!-- proofline:published-thread-series=01a20848-c199-76b0-82a5-c30dcd8f04bf -->
<!-- proofline:published-finding-series=01a20848-c19b-7019-a0f7-12cc9baf1993 -->
<!-- proofline:published-thread-series=01a20848-c19b-7019-a0f7-12cc9baf1993 -->
<!-- /proofline:published-findings -->
<!-- proofline:published-code=01a20848-c19c-72d8-998a-a2fda5ea0641 -->
<!-- proofline:published-code-thread=01a20848-c19c-72d8-998a-a2fda5ea0641 -->
<!-- proofline:published-code=01a20848-c1a8-754a-af69-5ff7da8cce3e -->
<!-- proofline:published-code-thread=01a20848-c1a8-754a-af69-5ff7da8cce3e -->

### inline comment by prooflinedev[bot] · 2026-11-23T12:02:07Z · reports.py:52

<!-- proofline:finding-series=01a20848-c199-76b0-82a5-c30dcd8f04bf -->
**Warning** · CSV export splits report names containing commas into extra columns

This change makes `write_export` join fields without CSV quoting, even though scheduled report names can contain commas, newlines, or quotes.

CSV readers can return extra columns or records, or misread the report name.

Keep iterating over the database cursor, but write the header and each row with `csv.writer`.

[View finding in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a20848-0f01-75ea-92a7-00858c21be09/findings/01a20848-c19c-72d8-998a-a2fda5ea0641)

### inline comment by prooflinedev[bot] · 2026-11-23T12:02:07Z · reports.py:55

<!-- proofline:finding-series=01a20848-c19b-7019-a0f7-12cc9baf1993 -->
**Warning** · CSV export splits report names containing commas or newlines

This change joins fields with commas instead of quoting and escaping them with `csv.writer`.

A report name containing a comma or newline can be parsed as extra columns or rows.

Keep iterating over the database cursor, but write the header and each row with `csv.writer`.

<details>
<summary>Details</summary>

The exported columns cannot contain SQL NULL under the current schema, so NULL serialization is not a reachable part of this defect.

</details>

[View finding in Proofline](https://proofline.sh/orgs/by-id/01a20844-88a4-77ad-871c-e0fb490cf0e8/reviews/01a20848-0f01-75ea-92a7-00858c21be09/findings/01a20848-c1a8-754a-af69-5ff7da8cce3e)
