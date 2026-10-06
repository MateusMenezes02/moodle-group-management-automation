"""Leitura e validação da lista de grupos de teste."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GroupSpec:
    name: str
    description: str


def load_groups(path: Path) -> list[GroupSpec]:
    if not path.is_file():
        raise FileNotFoundError(f"CSV não encontrado: {path}")

    with path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames != ["group_name", "description"]:
            raise ValueError("CSV deve ter exatamente os cabeçalhos: group_name,description")

        groups: list[GroupSpec] = []
        seen: set[str] = set()
        for line_number, row in enumerate(reader, start=2):
            name = (row.get("group_name") or "").strip()
            description = (row.get("description") or "").strip()
            if not name:
                raise ValueError(f"CSV linha {line_number}: group_name é obrigatório")
            if name.casefold() in seen:
                raise ValueError(f"CSV linha {line_number}: grupo duplicado no arquivo: {name}")
            seen.add(name.casefold())
            groups.append(GroupSpec(name=name, description=description))

    if not groups:
        raise ValueError("CSV não contém grupos")
    return groups
