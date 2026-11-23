# Scores

Claim-level grades per PROTOCOL.md §4. Rates are always shown with their denominators.

| Provider | Catches | Partials | Appr. uncertainty | False positives | Unsupported | Unanticipated-valid | Misses (expected defects not hit) | Claims graded | Precision |
|---|---|---|---|---|---|---|---|---|---|
| proofline | 6 | 0 | 0 | 2 | 0 | 6 | 4 | 14 | 12/14 = 0.86 |
| greptile | 8 | 0 | 0 | 0 | 0 | 1 | 2 | 9 | 9/9 = 1.00 |
| coderabbit | 8 | 0 | 0 | 0 | 0 | 2 | 2 | 10 | 10/10 = 1.00 |
| qodo | 8 | 0 | 0 | 0 | 0 | 2 | 2 | 10 | 10/10 = 1.00 |
| sourcery | 8 | 0 | 0 | 0 | 0 | 6 | 2 | 14 | 14/14 = 1.00 |

Expected defects in the key: 7 across 7 defective cases (conditions counted separately for snapshot cases in the miss count). Recall per provider = (catches + ½·partials on expected defects) ÷ expected defects for the conditions that provider completed — compute it from grades.csv when writing the report, and state the denominator.
