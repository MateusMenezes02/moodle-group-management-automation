# Project Screenshots

This folder contains real screenshots captured from the local Moodle test environment used to validate the automation.

All screenshots were captured in an isolated local environment using fictional data. No client, learner, production, credential, or confidential information is included.

## 01 — Moodle Groups Before Automation

![Moodle groups before automation](01-moodle-groups-before.png)

Shows the Moodle Groups page before running the automation.

This represents the initial state of the test course before the demo groups are created.

## 02 — First Script Execution

![First script execution](02-script-execution.png)

Shows the terminal output from the first successful execution of the Python + Playwright automation.

The workflow reads the configured group data and creates the fictional groups in Moodle.

## 03 — Moodle Groups After Automation

![Moodle groups after automation](03-moodle-groups-after.png)

Shows the Moodle Groups page after the automation completes successfully.

The fictional groups are now visible in the LMS:

- Group A
- Group B
- Group C

## 04 — Idempotent Second Run

![Idempotent second run](04-second-run-idempotent.png)

Shows a second execution of the automation.

The script detects that the groups already exist and skips them instead of creating duplicates.

This demonstrates the idempotent behavior of the workflow.
