"""Persist tasks as JSON. Plain Python: no Qt needed for this part."""
import json
from dataclasses import asdict
from pathlib import Path

from models import Task


def load_tasks(path: Path) -> list[Task]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return [Task(**item) for item in data]


def save_tasks(path: Path, tasks: list[Task]) -> None:
    path.write_text(json.dumps([asdict(t) for t in tasks], indent=2), encoding="utf-8")
