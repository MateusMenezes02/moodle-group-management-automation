"""Ponto de entrada do MVP de criação idempotente de grupos Moodle."""

from __future__ import annotations

import logging
import sys

from playwright.sync_api import sync_playwright

from config import load_settings
from csv_loader import load_groups
from moodle_client import MoodleAutomationError, MoodleClient


logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def main() -> int:
    try:
        settings = load_settings()
        groups = load_groups(settings.groups_csv)

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=settings.headless)
            page = browser.new_page()
            try:
                client = MoodleClient(page, settings)
                client.login()
                client.open_course_groups()
                for group in groups:
                    if client.create_if_missing(group):
                        logger.info("[OK] %s created", group.name)
                    else:
                        logger.info("[SKIPPED] %s already exists", group.name)
            finally:
                browser.close()
        return 0
    except (FileNotFoundError, ValueError, MoodleAutomationError) as exc:
        logger.error("[ERROR] %s", exc)
        return 1
    except Exception as exc:  # Registra erro inesperado sem ocultar a falha.
        logger.exception("[ERROR] Unexpected automation failure: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
