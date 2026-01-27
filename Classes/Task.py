from typing import Optional
from datetime import date


class Task:
    def __init__(self, id_task: int, title: str, priority: str,
                 tags: list[str] = [], completed: bool = False, description: Optional[str] = "",
                 deadline: Optional[date] = None) -> None:
        self._id_task = id_task
        self._title = title
        self._description = description or ""
        self._deadline = deadline
        self._priority = priority
        self._tags = tags[:]
        self._completed = completed

    # Properties CORREGIDOS
    @property
    def id_task(self) -> int:
        return self._id_task

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        self._title = title

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        self._description = description

    @property
    def deadline(self) -> Optional[date]:  # Optional!
        return self._deadline

    @deadline.setter
    def deadline(self, deadline: Optional[date]) -> None:
        self._deadline = deadline

    @property
    def priority(self) -> str:
        return self._priority

    @priority.setter
    def priority(self, priority: str) -> None:
        self._priority = priority

    @property
    def tags(self) -> list[str]:
        return self._tags[:]  # Copia para evitar modificación externa

    @tags.setter
    def tags(self, tags: list[str]) -> None:
        self._tags = tags[:]

    @property
    def completed(self) -> bool:
        return self._completed

    @completed.setter
    def completed(self, completed: bool) -> None:
        self._completed = completed

    def print_task(self) -> None:
        status = "✓" if self.completed else "○"
        deadline_str = str(self.deadline)[:10] if self.deadline else "Sin fecha  "

        # Formato tabla: | ID | Título | Pri | Status | Fecha    | Tags | Descripcion
        print(f"| {self._id_task} | {self.title[:25]:25} | {self.priority[:3]:3} | {status:2} | {deadline_str:10} | {', '.join(self.tags)[:12]:<12} | {self.description:10} |")
