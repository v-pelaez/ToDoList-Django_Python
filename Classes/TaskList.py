from typing import List, Optional
from datetime import date
from Classes.Task import Task
from Classes.Utils import Utils

class TaskList:
    def __init__(self, id_list: int, list_name: str, filepath: str = Utils.DEFAULT_FILE) -> None:

        self._id_list = id_list
        self._list_name = list_name
        self.filepath = filepath
        self._content: List[Task] = []
        self.load_from_file()

    def load_from_file(self) -> bool:

        try:
            self._content = Utils.dicts_to_tasks(Utils.load_tasks_list(self.filepath))
            return True
        except (FileNotFoundError, ValueError):
            return False

    def save_to_file(self) -> bool:

        return Utils.save_tasks_list(self._content, self.filepath)

    def add_task(self, task: Task) -> None:

        self._content.append(task)

    def remove_task(self, index: int) -> None:

        self._content.pop(index)

    def complete_task(self, index: int) -> None:

        self._content[index].completed = True

    def complete_all(self) -> None:

        for task in self._content:
            task.completed = True

    def restart_all(self) -> None:

        for task in self._content:
            task.completed = False

    @property
    def id_task(self) -> int:
        return self._id_list

    @id_task.setter
    def id_task(self, id_task: int) -> None:
        self._id_list = id_task

    @property
    def list_name(self) -> str:
        return self._list_name

    @list_name.setter
    def list_name(self, list_name: str) -> None:
        self._list_name = list_name

    @property
    def content(self) -> List[Task]:
        return self._content

    @content.setter
    def content(self, content: List[Task]) -> None:
        self._content = content


    def get_filtered_and_sorted(self, filter_by: Optional[str] = None, filter_val: Optional[str] = None, sort_by: str = "creacion") -> List[Task]:
        # Filtro y ordeno los datos para la tabla de la interfaz
        filtered_list: List[Task] = []
        search_val = filter_val.lower().strip() if filter_val else ""

        # Lógica de filtrado
        for task in self._content:
            if filter_by == "estado":
                if (search_val == "completada") == task.completed:
                    filtered_list.append(task)
            elif filter_by == "prioridad":
                if task.priority.lower() == search_val:
                    filtered_list.append(task)
            elif filter_by == "etiqueta":
                if any(search_val in tag.lower() for tag in task.tags):
                    filtered_list.append(task)
            else:
                # Si no hay filtros activos, incluyo la tarea
                filtered_list.append(task)

        # Lógica de ordenación
        def by_date(task: Task) -> date:
            # Uso date.max para que las tareas sin fecha aparezcan siempre al final
            return task.deadline if task.deadline else date.max

        def by_priority(task: Task) -> int:
            # Mapeo de importancia para ordenar correctamente por texto
            weights = {"alta": 0, "media": 1, "baja": 2}
            return weights.get(task.priority.lower(), 3)

        if sort_by == "fecha":
            filtered_list.sort(key=by_date)
        elif sort_by == "prioridad":
            filtered_list.sort(key=by_priority)
        else:
            # Orden por ID (orden de creación original)
            filtered_list.sort(key=lambda t: t.id_task)

        return filtered_list