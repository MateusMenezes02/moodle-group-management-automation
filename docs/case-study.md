# Case Study: Idempotent Moodle Group Creation

## Context

This project is a local automation prototype for a Moodle course administration workflow. Its goal is to turn a structured CSV file into a repeatable group-creation process without relying on production systems, customer data, or hard-coded credentials.

## Challenge

Manual group setup is manageable for a few entries but becomes repetitive as a course structure grows. A one-time automation is not enough: it should be safe to execute again after interruption, review, or CSV reprocessing without creating duplicate groups.

## Approach

The solution uses Python and Playwright to operate Moodle through its visible browser interface. The automation starts with validated CSV input, logs in using environment variables, opens the target course, and compares requested groups with Moodle's current Groups list.

When a group is missing, the automation fills Moodle's real group creation form and verifies that the group appears after saving. When it already exists, the automation logs a skip instead of submitting another form.

## Key Technical Decision: State-Based Idempotency

Moodle's group selector displays a member count alongside a group name, such as `Group A (0)`. Direct string comparison against a CSV value of `Group A` would fail and lead to duplicate-creation attempts.

The client removes only the final `(<number>)` display suffix before comparing names. This deliberately narrow normalization allows the automation to recognize an existing group while retaining the original CSV name for creation.

## Implementation Highlights

- Semantic Playwright selectors based on accessible roles and labels.
- Strict CSV header and duplicate validation.
- Environment-based configuration through `python-dotenv`.
- Clear `[OK]`, `[SKIPPED]`, and `[ERROR]` outcomes.
- Browser cleanup through a `finally` block.
- Verification after creation instead of assuming a successful button click means a group exists.

## Validation

The MVP was validated in a local Moodle test environment with three fictional CSV groups. A subsequent execution detected all three as existing and skipped them, confirming that the group-count display format was handled correctly.

## Scope and Trade-offs

The project intentionally uses the Moodle UI rather than an API because the exercise focuses on browser automation. This makes selector quality and UI verification important. The current selectors are verified against the Moodle 5.1 English interface and should be reviewed if the Moodle theme, language, or major version changes.

The MVP does not manage memberships, update group settings, delete groups, or process customer data.

## Lessons

- UI automation is more reliable when it models application state explicitly.
- Accessible markup is both a usability feature and a strong automation interface.
- Small modules with explicit boundaries make a proof of concept easier to audit and share.
- Sanitizing configuration and artifacts early is essential before publishing technical work.
