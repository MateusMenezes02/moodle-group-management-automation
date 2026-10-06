# Screenshot Capture Plan

This folder intentionally contains no generated or synthetic screenshots.

Capture only from an isolated, fictional Moodle test environment. Before adding any image, review it for usernames, browser tabs, URLs outside the local test setup, tokens, notifications, and personal information.

| File name | Real screen to capture | What it should demonstrate |
| --- | --- | --- |
| `01-moodle-groups-before.png` | The Moodle Groups page before running the CSV workflow | Starting state of the test course |
| `02-script-execution.png` | Terminal output from the first successful script run | `[OK]` creation logs for fictional groups |
| `03-moodle-groups-after.png` | The Moodle Groups page after creation | The fictional groups visible in Moodle |
| `04-second-run-idempotent.png` | Terminal output from the next execution | `[SKIPPED]` logs showing idempotency |

Do not add placeholder images, mock browser captures, or screenshots containing credentials.
