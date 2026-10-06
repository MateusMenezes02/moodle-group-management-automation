# Architecture

## Overview

The project uses a small, deliberately separated architecture. Each module has one main responsibility, keeping the automation easy to inspect, test, and extend without coupling CSV concerns to browser navigation.

```text
.env + groups.csv
       │
       ├── config.py ──────── Settings
       └── csv_loader.py ──── GroupSpec list
                                │
                                ▼
                           main.py
                                │
                                ▼
                        moodle_client.py
                                │
                                ▼
                     Moodle browser interface
```

## Configuration

`src/config.py` loads `.env` from the project root and validates required values before a browser session is created. The settings object is immutable, and no credential value is stored in source code.

## CSV Loading

`src/csv_loader.py` owns input parsing and validation. It requires the exact headers `group_name,description`, rejects empty group names, and detects duplicate names in the input file using case-insensitive comparison. It returns `GroupSpec` objects rather than raw dictionaries.

## Moodle Browser Client

`src/moodle_client.py` owns the browser workflow and Moodle-specific knowledge. It signs in, selects the configured course, extracts its course ID, opens the Groups page, reads the accessible `Groups` list, and creates missing groups through Moodle's labeled form.

Selectors use roles for menu items, links, buttons, listboxes, and options; labels for credential and group fields; and exact matching for action buttons. No screen coordinates or XPath selectors are used.

### Group Name Normalization

Moodle renders a group list option as `Group name (member count)`. The client removes only a trailing numeric suffix in that exact format before comparison:

```text
Group A (0)  →  group a
Group A      →  group a
```

This makes repeated executions idempotent while preserving the original CSV name for creation.

## Execution Workflow

`src/main.py` composes the other modules:

1. Load settings and CSV groups.
2. Launch Chromium through Playwright.
3. Authenticate and open the target course Groups page.
4. Call `create_if_missing()` for each `GroupSpec`.
5. Emit an outcome log for each group.
6. Close the browser in a `finally` block, including if an error occurs.

Expected failures such as missing configuration, invalid CSV data, failed login, or an unavailable course are reported as `[ERROR]` with a non-zero exit status.

## Scope Boundary

The current MVP creates missing groups only. It intentionally does not add users to groups, edit groups, remove groups, or invoke Moodle APIs.
