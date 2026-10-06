"""Fluxo Playwright para gerenciamento de grupos no Moodle local."""

from __future__ import annotations

import re
from urllib.parse import parse_qs, urlparse

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from config import Settings
from csv_loader import GroupSpec


class MoodleAutomationError(RuntimeError):
    """Erro de navegação ou validação do Moodle."""


class MoodleClient:
    _MEMBER_COUNT_SUFFIX = re.compile(r"\s+\(\d+\)\s*$")

    def __init__(self, page: Page, settings: Settings) -> None:
        self.page = page
        self.settings = settings
        self.course_id: str | None = None

    def login(self) -> None:
        self.page.goto(f"{self.settings.base_url}/login/index.php", wait_until="domcontentloaded")
        username = self.page.get_by_label("Username", exact=True)
        if username.count() == 0:
            # A sessão já pode existir; só a aceitamos se for o Moodle local.
            if not self.page.url.startswith(self.settings.base_url):
                raise MoodleAutomationError("Não foi possível abrir o Moodle local.")
            return

        username.fill(self.settings.username)
        self.page.get_by_label("Password", exact=True).fill(self.settings.password)
        self.page.get_by_role("button", name="Log in", exact=True).click()
        self.page.wait_for_load_state("domcontentloaded")
        if self.page.get_by_label("Username", exact=True).count() > 0:
            raise MoodleAutomationError("Login falhou; verifique MOODLE_USERNAME e MOODLE_PASSWORD.")

    def open_course_groups(self) -> None:
        # Navega pela interface real: My courses > curso por nome.
        self.page.get_by_role("menuitem", name="My courses", exact=True).click()
        self.page.wait_for_load_state("domcontentloaded")
        course = self.page.get_by_role("link", name=self.settings.course_name, exact=True)
        try:
            course.click(timeout=10_000)
        except PlaywrightTimeoutError as exc:
            raise MoodleAutomationError(f"Curso não encontrado: {self.settings.course_name}") from exc
        self.page.wait_for_load_state("domcontentloaded")

        query = parse_qs(urlparse(self.page.url).query)
        course_id = query.get("id", [None])[0]
        if not course_id:
            raise MoodleAutomationError("Não foi possível identificar o ID do curso pela URL do Moodle.")
        self.course_id = course_id

        # URL confirmada na interface Moodle 5.1 deste laboratório.
        self.page.goto(f"{self.settings.base_url}/group/index.php?id={course_id}", wait_until="domcontentloaded")
        self.page.get_by_role("listbox", name="Groups", exact=True).wait_for()

    def existing_group_names(self) -> set[str]:
        groups_list = self.page.get_by_role("listbox", name="Groups", exact=True)
        # A interface Moodle 5.1 exibe opções como "Nome do grupo (0)", sendo
        # o sufixo a quantidade de membros. Não o usamos para a identidade.
        return {
            self._canonical_group_name(name)
            for name in groups_list.get_by_role("option").all_text_contents()
        }

    @classmethod
    def _canonical_group_name(cls, displayed_name: str) -> str:
        """Remove somente o contador final acrescentado pela tela de grupos."""
        return cls._MEMBER_COUNT_SUFFIX.sub("", displayed_name).strip().casefold()

    def create_if_missing(self, group: GroupSpec) -> bool:
        if self._canonical_group_name(group.name) in self.existing_group_names():
            return False

        self.page.get_by_role("button", name="Create group", exact=True).click()
        self.page.get_by_label("Group name", exact=True).fill(group.name)
        self.page.get_by_label("Group description", exact=True).fill(group.description)
        self.page.get_by_role("button", name="Save changes", exact=True).click()
        self.page.wait_for_load_state("domcontentloaded")

        if self._canonical_group_name(group.name) not in self.existing_group_names():
            raise MoodleAutomationError(f"Moodle não confirmou a criação do grupo: {group.name}")
        return True
