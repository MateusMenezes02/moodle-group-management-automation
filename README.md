# Moodle Group Management Automation

An idempotent Python and Playwright MVP for creating course groups in a local Moodle test environment from a CSV file.

This project was built as a controlled automation case study. It creates missing groups, records clear outcomes, and safely skips groups that already exist. It does not manage real users, modify existing groups, or delete Moodle data.

## Project Overview

The automation reads a small CSV dataset, signs in to Moodle, opens a configured course, and creates the listed groups when necessary. It is designed for a local, fictional Moodle environment and uses environment variables for all credentials.

## Problem

Creating course groups manually is repetitive and error-prone when a course needs a predefined group structure. Re-running a basic script can also create duplicate groups unless it verifies the current Moodle state first.

## Solution

The MVP combines CSV input, Playwright browser automation, and Moodle's accessible UI controls. Before creating a group, it reads the current Groups list and compares normalized group names. Existing groups are skipped; only missing groups are created.

## How It Works

1. Load and validate `data/groups.csv`.
2. Load the Moodle URL, username, password, and course name from `.env`.
3. Sign in to the configured Moodle instance.
4. Open **My courses**, select the configured course, and derive its Moodle course ID.
5. Open the course Groups page.
6. Read existing group options from the accessible `Groups` list.
7. Create each missing group using the real Moodle form labels.
8. Verify that each created group appears in the Groups list.

## Demo

### Before Automation

The test course starts without the demo groups created by the automation.

![Moodle groups before automation](screenshots/01-moodle-groups-before.png)

### First Execution

The Python + Playwright workflow reads the CSV input and creates the configured groups in Moodle.

![First script execution](screenshots/02-script-execution.png)

### Result in Moodle

After the automation completes, the created groups are visible in the Moodle group-management interface.

![Moodle groups after automation](screenshots/03-moodle-groups-after.png)

### Idempotent Second Run

Running the automation again does not create duplicates. Existing groups are detected and skipped.

![Idempotent second run](screenshots/04-second-run-idempotent.png)

See [screenshots/README.md](screenshots/README.md) for detailed screenshot documentation.

## Tech Stack

- Python 3.10+
- Playwright for Chromium browser automation
- python-dotenv for local environment configuration
- CSV from Python's standard library
- Moodle 5.1 local test environment

## Project Structure

```text
automation/
├── src/
│   ├── config.py          # Environment loading and validation
│   ├── csv_loader.py      # CSV validation and group models
│   ├── moodle_client.py   # Moodle UI workflow through Playwright
│   └── main.py            # Execution and log output
├── data/
│   └── groups.csv         # Example group input
├── docs/
│   ├── architecture.md
│   └── case-study.md
├── screenshots/
│   ├── 01-moodle-groups-before.png
│   ├── 02-script-execution.png
│   ├── 03-moodle-groups-after.png
│   ├── 04-second-run-idempotent.png
│   └── README.md          # Screenshot documentation
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

Prerequisites:

- Python 3.10 or newer
- A reachable Moodle test instance
- A Moodle account with permission to manage groups in the target course

```sh
cd automation
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## Configuration

```sh
cp .env.example .env
```

Set the values for your isolated test environment:

```ini
MOODLE_BASE_URL=http://localhost:8080
MOODLE_USERNAME=your-admin-username
MOODLE_PASSWORD=your-local-test-password
MOODLE_COURSE_NAME=your-test-course-name
PLAYWRIGHT_HEADLESS=true
```

`.env` is ignored by Git. Never commit passwords, browser profiles, client URLs, or production data.

## Example CSV Input

`data/groups.csv`:

```csv
group_name,description
Group A,Automation demo group A
Group B,Automation demo group B
Group C,Automation demo group C
```

The loader requires exactly the `group_name` and `description` columns, non-empty group names, and no duplicate names within the CSV.

## Running the Automation

With the virtual environment activated:

```sh
python src/main.py
```

## Idempotency

Moodle displays groups in its list as `Group name (member count)`, for example `Group A (0)`. The automation removes only this final numeric member-count suffix before comparing names. Therefore, a CSV entry named `Group A` matches Moodle's displayed `Group A (0)` and is skipped on later runs.

The automation validates a successful creation by checking that the new group appears in Moodle's Groups list after saving.

## Security & Privacy

- Credentials are loaded only from `.env`, never from source code.
- `.env`, virtual environments, bytecode, and operating-system files are excluded by `.gitignore`.
- The repository contains fictional group data only.
- The project is intended for an isolated Moodle test instance, not customer or production environments.
- Screenshots should be reviewed for usernames, URLs, tokens, and personal data before publication.

## Example Output

First run, when all groups are absent:

```text
[OK] Group A created
[OK] Group B created
[OK] Group C created
```

Later run, when the groups already exist:

```text
[SKIPPED] Group A already exists
[SKIPPED] Group B already exists
[SKIPPED] Group C already exists
```

## What I Learned

- Browser automations should rely on real, accessible UI semantics instead of coordinates or brittle XPath selectors.
- Idempotency depends on validating the application state, not merely assuming a previous run succeeded.
- UI text may include presentation details such as member counts; normalization needs to be narrow and intentional.
- Clear configuration boundaries make a local proof of concept safer to share and easier to evolve.

See [the architecture notes](docs/architecture.md), [the portfolio case study](docs/case-study.md), and [the screenshot capture plan](screenshots/README.md) for more context.
