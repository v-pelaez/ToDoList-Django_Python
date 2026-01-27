import json
import os
from datetime import date
from typing import Sequence, Any
from Classes.Task import Task


class Utils:
    DEFAULT_FILE = "../Data/task.json"

    # Mapeo private → public para compatibilidad
    PRIVATE_TO_PUBLIC = {
        '_id_task': 'id_task', '_title': 'title', '_priority': 'priority',
        '_tags': 'tags', '_completed': 'completed', '_description': 'description',
        '_deadline': 'deadline'
    }

    @staticmethod
    def save_tasks_list(tasks: Sequence[Task], filepath: str = DEFAULT_FILE) -> bool:
        def date_serializer(obj: Any) -> str:
            if isinstance(obj, date): return obj.isoformat()
            raise TypeError(f"No serializable: {type(obj)}")

        try:
            data = []
            for task in tasks:
                task_dict = task.__dict__.copy()
                # Limpia claves: _private → public
                data.append({Utils.PRIVATE_TO_PUBLIC.get(k, k): v for k, v in task_dict.items()})

            os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, default=date_serializer, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"❌ Save error: {e}")
            return False

    @staticmethod
    def load_tasks_list(filepath: str) -> list[dict]:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"{filepath} no existe")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON inválido: {e}")

    @staticmethod
    def dicts_to_tasks(data: list[dict]) -> list[Task]:
        tasks = []
        for task_dict in data:
            deadline_str = task_dict.get('deadline')
            deadline = None
            if deadline_str:
                try:
                    clean = deadline_str.split('T')[0].strip()
                    deadline = date.fromisoformat(clean)
                except ValueError:
                    print(f"Fecha skip: {deadline_str}")

            # Usa .get() safe + defaults
            task = Task(
                id_task=task_dict.get('id_task', 0),
                title=task_dict.get('title', 'Sin título'),
                priority=task_dict.get('priority', 'Baja'),
                tags=task_dict.get('tags', []),
                completed=task_dict.get('completed', False),
                description=task_dict.get('description', ''),
                deadline=deadline
            )
            tasks.append(task)
        return tasks
