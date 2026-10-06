"""Configuração carregada exclusivamente de variáveis de ambiente."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv


PROJECT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    base_url: str
    username: str
    password: str
    course_name: str
    groups_csv: Path
    headless: bool


def _required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ValueError(f"Variável obrigatória ausente ou vazia: {name}")
    return value


def load_settings() -> Settings:
    base_url = _required("MOODLE_BASE_URL").rstrip("/")
    parsed = urlparse(base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("MOODLE_BASE_URL deve ser uma URL HTTP(S) válida.")

    return Settings(
        base_url=base_url,
        username=_required("MOODLE_USERNAME"),
        password=_required("MOODLE_PASSWORD"),
        course_name=_required("MOODLE_COURSE_NAME"),
        groups_csv=PROJECT_DIR / "data" / "groups.csv",
        headless=os.getenv("PLAYWRIGHT_HEADLESS", "true").lower() not in {"0", "false", "no"},
    )
