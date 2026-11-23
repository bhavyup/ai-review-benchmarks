# Raw review — provider: coderabbit · case 05 · condition B
PR: https://github.com/upreti-labs/run-coderabbit/pull/10 · base pilot/base · head pilot/05 · status in_progress

## Reviews (verbatim, in order received)

### review by coderabbitai[bot] · 2026-11-23T13:43:43Z · COMMENTED

<!-- coderabbit-ai-generated:v1 -->



<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://storage.googleapis.com/coderabbit_public_assets/review-comment-icons-v1/message-square-off-dark.svg"><img src="https://storage.googleapis.com/coderabbit_public_assets/review-comment-icons-v1/message-square-off.svg" width="16" height="16" align="absmiddle" alt=""></picture> Additional comments: 1</summary><blockquote>
<dl>
<dd>
<br>

<details>
<summary>reports.py-10-10: 1</summary><blockquote>
<dl>
<dd>
<br>

`10-10`: **<picture><img src="https://storage.googleapis.com/coderabbit_public_assets/review-comment-icons-v1/major-16.svg" width="16" height="16" align="absmiddle" alt=""></picture> Major** · **Data Integrity & Integration** · **Quick win**

<picture><img src="https://storage.googleapis.com/coderabbit_public_assets/pre-merge-checks-warning.svg" width="20" height="20" align="absmiddle" alt=""></picture> **Unverified finding**
Verification ran but could not confirm this finding. It is shown for review, not as a verified issue.

**Keep each batch within the site's request limit.**

At cedar, the first batch contains 50 rows, but the receiver accepts at most 40. It rejects the entire batch. The previous batches of 25 fit the limit. Use a site-specific batch limit, or keep the limit at or below 40 for cedar.

<!-- cr-comment:v1:5dd00fe1d827de637ae1851d -->

</dd>
</dl>
</blockquote></details>

</dd>
</dl>
</blockquote></details>

<h6>
<details>
<summary><picture><img src="https://storage.googleapis.com/coderabbit_public_assets/review-comment-icons-v1/info.svg" width="12" height="12" align="absmiddle" alt=""></picture> Review info</summary>
<dl>
<dd>
<br>

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://storage.googleapis.com/coderabbit_public_assets/review-comment-icons-v1/cog-dark.svg"><img src="https://storage.googleapis.com/coderabbit_public_assets/review-comment-icons-v1/cog.svg" width="16" height="16" align="absmiddle" alt=""></picture> Run configuration</summary>
<dl>
<dd>
<br>

- **Source mode**: Auto
- **Repository**: Unavailable
- **Branch**: Unavailable
- **File**: No configuration file from this repository applied
- **Commit**: Unavailable
- **Layers**: defaults
- **Review profile**: CHILL
- **Plan**: Advanced
- **Run ID**: `d3579dfb-ae96-40b2-ae3e-10d6f24e488e`

</dd>
</dl>
</details>

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://storage.googleapis.com/coderabbit_public_assets/review-comment-icons-v1/git-commit-horizontal-dark.svg"><img src="https://storage.googleapis.com/coderabbit_public_assets/review-comment-icons-v1/git-commit-horizontal.svg" width="16" height="16" align="absmiddle" alt=""></picture> Commits</summary>
<dl>
<dd>
<br>

Reviewing files that changed from the base of the PR and between 9b5ac64ab0d3ba414c5edec1e64fcdf8b3b19a1a and 1f6f2a4d891c1481ae09c816fac4edcf361c45f1.

</dd>
</dl>
</details>

<details>
<summary><picture><source media="(prefers-color-scheme: dark)" srcset="https://storage.googleapis.com/coderabbit_public_assets/review-comment-icons-v1/file-plus-corner-dark.svg"><img src="https://storage.googleapis.com/coderabbit_public_assets/review-comment-icons-v1/file-plus-corner.svg" width="16" height="16" align="absmiddle" alt=""></picture> Files selected for processing: 1</summary>
<dl>
<dd>
<br>

* `reports.py`

</dd>
</dl>
</details>

**Included review availability:** This review used your included allowance. Your plan provides up to 10 included reviews per hour; 0 remain after this review.

</dd>
</dl>
</details>
</h6>

<!-- This is an auto-generated comment by CodeRabbit for review status -->

<!-- coderabbit-review-publication v1 publication=f819cde9-16b1-4083-9b5b-f34de57bcef9 attempt=41d444ce-7563-41f9-b735-ecfef386af4c batch=1/1 -->

### PR comment by coderabbitai[bot] · 2026-11-23T13:41:41Z

<!-- coderabbit-ai-generated:v1 -->

<!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- review_stack_entry_start -->

<a href="https://app.coderabbit.ai/change-stack/upreti-labs/run-coderabbit/pull/10?scope=ghh_OusAJGA4HG8ljoOV0wJvVx8NmnZIjc2DdjmxOu0xZWA&amp;cs_source=review_comment"><picture><source media="(prefers-color-scheme: dark)" srcset="https://storage.googleapis.com/coderabbit_public_assets/review-stack-buttons-v1/explain-change-dark.svg"><source media="(prefers-color-scheme: light)" srcset="https://storage.googleapis.com/coderabbit_public_assets/review-stack-buttons-v1/explain-change.svg"><img src="https://storage.googleapis.com/coderabbit_public_assets/review-stack-buttons-v1/explain-change.svg" alt="Explain Change →" height="32"></picture></a>

<!-- review_stack_entry_end -->
<!-- walkthrough_start -->

<details>
<summary><strong>Walkthrough</strong></summary>
<dl>
<dd>
<br>

<!-- coderabbit_walkthrough_overview_removed -->

**Changes: Export Batch Size**

|Layer / File(s)|Summary|
|:---|:---|
|**Update export batch limit** <br> `reports.py`|`EXPORT_BATCH_SIZE` changes from 25 to 50. `export_to_sink` reads up to 50 rows per batch.|

**Possibly related PRs**

- [upreti-labs/run-coderabbit#5](https://github.com/upreti-labs/run-coderabbit/pull/5): Changes the export batch size to 50 records per archive request, matching this PR’s batch-size change.

</dd>
</dl>
</details>

<!-- walkthrough_end -->
<!-- change_assessment_start -->
<!-- change_assessment_commit:"1f6f2a4d891c1481ae09c816fac4edcf361c45f1" -->
<!-- change_assessment_priority:{"version":1,"urgency":"p3","manual":false} -->
**Change:** Other
<!-- change_assessment_end -->
<details>
<summary><strong>Merge Risk:</strong> <strong><picture><img src="https://storage.googleapis.com/coderabbit_public_assets/review-comment-icons-v1/risk-normal-16.svg" width="16" height="16" align="absmiddle" alt=""></picture> Moderate</strong> · up to <code>1f6f2</code></summary>
<dl>
<dd>
<br>

<!-- final_review_risk_start -->
<!-- final_review_risk_label
**Merge Risk:** **🟡 Moderate** · up to `1f6f2`
-->
<!-- final_review_risk_coverage:{"sourceCommitId":"1f6f2a4d891c1481ae09c816fac4edcf361c45f1","coveredCommitId":"1f6f2a4d891c1481ae09c816fac4edcf361c45f1","kind":"reviewed"} -->

This raises the export batch size from 25 to 50 rows. The PR description says one site, cedar, accepts at most 40 rows per request and rejects larger requests entirely, which would fail that site's export. The repository's archive command only prints batches locally, so this could not be confirmed from the code. Confirm the per-site limits against the real receiver, or use a site-specific batch size, before merging.
<!-- final_review_risk_end -->

</dd>
</dl>
</details>

<details>
<summary><strong>Security architecture risk:</strong> <strong><picture><img src="https://storage.googleapis.com/coderabbit_public_assets/review-comment-icons-v1/risk-normal-16.svg" width="16" height="16" align="absmiddle" alt=""></picture> Moderate</strong> · up to <code>1f6f2</code></summary>
<dl>
<dd>
<br>

<!-- architecture_review_start -->
<!-- architecture_review_label
### Security Architecture Review

**Security architecture risk:** **🟡 Moderate** · up to `1f6f2`
-->

At the reported cutover settings, Cedar would reject the first 50-row request, leaving its scheduled archive incomplete. Elm’s limit accommodates both requests. Reverting the batch size would make new requests fit again, but would not by itself reconcile rows already accepted.

**Retained concerns**
- **Medium · reliability · inferred:** At the reported Cedar cutover, the first 50-row request would be rejected in full. Without recovery, a fail-stop adapter would leave all 70 rows unarchived by that invocation; an adapter that continues and successfully sends the final 20 would leave 50 unarchived. The previous batch size fits the receiver limit, but the exporter has no checkpoint for reconciling a partial run before replay.

<details>
<summary><strong>Security review details</strong></summary>
<dl>
<dd>
<br>

**Security Blast Radius**
- _inferred_ — The demonstrated exposure is archive availability and completeness at Cedar under the supplied cutover scenario. Elm does not share the request-size incompatibility, and the verified code change does not expand export access.

**Hardening Proposals**
- _proposed_ — Gate the cutover on the effective receiver limits. Keep requests within the lowest supported cap or enforce a verified per-site cap, and establish how rejected batches are acknowledged and replayed without duplicating accepted rows.

</dd>
</dl>
</details>
<!-- architecture_review_end -->

</dd>
</dl>
</details>
<!-- finishing_touch_checkbox_start -->

<details>
<summary><strong>Finishing Touches</strong></summary>
<dl>
<dd>
<br>

<details open>
<summary><strong>Generate unit tests (beta)</strong></summary>
<dl>
<dd>
<br>

- [ ] <!-- {"checkboxId": "6ba7b810-9dad-11d1-80b4-00c04fd430c8", "radioGroupId": "utg-output-choice-group-unknown_comment_id"} --> Commit to this branch
- [ ] <!-- {"checkboxId": "f47ac10b-58cc-4372-a567-0e02b2c3d479", "radioGroupId": "utg-output-choice-group-unknown_comment_id"} --> Create a new PR

</dd>
</dl>
</details>

</dd>
</dl>
</details>

<!-- finishing_touch_checkbox_end -->

<!-- autopilot:start -->
- [ ] <!-- {"checkboxId":"2708ad07-9f24-4260-9c11-7dc76a49f2e3"} --> <strong title="Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts">Autofix</strong> · Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts
<!-- autopilot:end -->
<!-- verify_invitation_start -->
### CodeRabbit Verify

- [ ] <!-- {"checkboxId":"run-qa-agent"} --> Run CodeRabbit Verify to test the changes in this pull request.
<!-- verify_invitation_end -->

### PR comment by coderabbitai[bot] · 2026-11-23T13:41:43Z

<!-- coderabbit-qa-agent -->
<!-- coderabbit-qa-agent-state run=7213e28a-991b-467f-9e3b-82c0803befa4 revision=17 created=1795441298743 terminal=true -->
<a href="https://app.coderabbit.ai/change-stack/upreti-labs/run-coderabbit/pull/10/verify?cs_source=qa_pr_comment&amp;qaRunId=7213e28a-991b-467f-9e3b-82c0803befa4&amp;qaView=history"><picture><source media="(prefers-color-scheme: dark)" srcset="https://storage.googleapis.com/coderabbit_public_assets/qa-agent-review-evidence-dark.svg?v=3"><source media="(prefers-color-scheme: light)" srcset="https://storage.googleapis.com/coderabbit_public_assets/qa-agent-review-evidence.svg?v=3"><img src="https://storage.googleapis.com/coderabbit_public_assets/qa-agent-review-evidence.svg?v=3" alt="Review evidence" height="32"></picture></a>

### CodeRabbit Verify

Passed on PR 10 head: the CLI archived 50 deliveries in one batch, then 55 deliveries in batches of 50 and 5\. All records were ordered and preserved\.

**All scenarios passed · 1 of 1 scenario complete · <sup><img src="https://app.coderabbit.ai/public/review-action-buttons/qa-status-v1/passed.svg" width="16" height="16" alt="Passed" title="Passed" align="middle"></sup> 1 passed**

Tested commit [`1f6f2a4`](https://github.com/upreti-labs/run-coderabbit/commit/1f6f2a4d891c1481ae09c816fac4edcf361c45f1) · Total time: 7m 33s

| Result | Scenario | Run summary |
| --- | --- | --- |
| <div align="center">![Passed](https://app.coderabbit.ai/public/review-action-buttons/qa-status-v1/passed.svg)</div> | [It archives scheduled report deliveries in batches of up to 50 records](https://app.coderabbit.ai/change-stack/upreti-labs/run-coderabbit/pull/10/verify?cs_source=qa_pr_comment&qaRunId=7213e28a-991b-467f-9e3b-82c0803befa4&qaView=history&scenario=archive-batch-size-50) | Passed on PR 10 head: the CLI archived 50 deliveries in one batch, then 55 deliveries in batches of 50 and 5\. All records were ordered and preserved\. · [Evidence](https://app.coderabbit.ai/change-stack/upreti-labs/run-coderabbit/pull/10/verify?cs_source=qa_pr_comment&qaRunId=7213e28a-991b-467f-9e3b-82c0803befa4&qaView=history&scenario=archive-batch-size-50) |

[View test results](<https://app.coderabbit.ai/change-stack/upreti-labs/run-coderabbit/pull/10/verify?cs_source=qa_pr_comment&qaRunId=7213e28a-991b-467f-9e3b-82c0803befa4&qaView=history>) · [Revise scenarios](<https://app.coderabbit.ai/change-stack/upreti-labs/run-coderabbit/pull/10/verify?cs_source=qa_pr_comment>) · [Turn off automatic Verify](<https://app.coderabbit.ai/verify/settings?providerRepository=1468756982&orgId=2abdc22b-45fc-4c0c-aa27-30a482635c49&orgProvider=github>)
