import json
import os
from datetime import date, datetime
from typing import Sequence, Any
from Classes.Task import Task


class Utils:
    DEFAULT_FILE = os.path.join("Data", "task.json")  # Carpeta y fichero por defecto
    VALID_PRIORITIES = ("alta", "media", "baja")  # Prioridades permitidas

    # Diccionario de atributos privados a públicos para la serialización
    PRIVATE_TO_PUBLIC = {
        '_id_task': 'id_task', '_title': 'title', '_priority': 'priority',
        '_tags': 'tags', '_completed': 'completed', '_description': 'description',
        '_deadline': 'deadline'
    }

    @staticmethod
    def save_tasks_list(tasks: Sequence[Task], filepath: str = DEFAULT_FILE) -> bool:
        """ Guarda la lista de tareas en un archivo JSON.
        return: True si se guardó correctamente, False en caso contrario """

        def date_serializer(obj: Any) -> str:
            # Serializador personalizado para fechas
            if isinstance(obj, (date, datetime)): return obj.isoformat()
            raise TypeError(f"No serializable: {type(obj)}")

        try:
            data = []
            for task in tasks:
                # Mapeamos los atributos privados a sus nombres públicos
                task_dict = {Utils.PRIVATE_TO_PUBLIC.get(k, k): v for k, v in task.__dict__.items()}
                data.append(task_dict)

            # Crea el directorio si no existe
            os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, default=date_serializer, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            # En una GUI real, esto debería lanzar una excepción o usar logging
            print(f"❌ Error al guardar: {e}")
            return False

    @staticmethod
    def load_tasks_list(filepath: str) -> list[dict]:
        """ Carga la lista de tareas desde un archivo JSON.
        return: lista de diccionarios con los datos de las tareas """
        if not os.path.exists(filepath): return []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception:
            return []

    @staticmethod
    def dicts_to_tasks(data: list[dict]) -> list[Task]:
        """ Convierte una lista de diccionarios en una lista de objetos Task.
        return: lista de objetos Task instanciados """
        tasks = []
        for d in data:
            deadline = None
            if d.get('deadline'):
                try:
                    # Extraemos solo la parte de la fecha si viene con hora
                    deadline = date.fromisoformat(d['deadline'].split('T')[0])
                except:
                    pass

            tasks.append(Task(
                id_task=d.get('id_task', 0),
                title=d.get('title', 'Sin título'),
                priority=d.get('priority', 'media'),
                tags=d.get('tags', []),
                completed=d.get('completed', False),
                description=d.get('description', ''),
                deadline=deadline
            ))
        return tasks