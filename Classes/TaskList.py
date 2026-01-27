from Classes.Task import Task
import Utils
from Utils import Utils


class TaskList:
    def __init__(self, id_list: int, list_name: str, filepath: str = Utils.DEFAULT_FILE):
        self._id_list, self._list_name, self.filepath = id_list, list_name, filepath
        self._content = []
        self.load_from_file()  # Auto-carga

    def load_from_file(self) -> bool:
        try:
            self._content = Utils.dicts_to_tasks(Utils.load_tasks_list(self.filepath))
            return True
        except (FileNotFoundError, ValueError):
            return False

    def save_to_file(self) -> bool:
        return Utils.save_tasks_list(self._content, self.filepath)


    def _create_initial_file(self) -> None:  # Ya no necesario
        """Opcional: Crea vacío solo si quieres forzar."""
        Utils.save_tasks_list([], self.filepath)

    def add_task(self, task: Task) -> None:
        self.content.append(task)

    def remove_task(self, index: int) -> None:
        self.content.pop(index)

    def complete_task(self, index: int) -> None:
        self.content[index].completed = True

    def complete_all(self) -> None:
        for task in self.content:
            task.completed = True

    def restart_all(self) -> None:
        for task in self.content:
            task.completed = False

    @property
    def id_task(self) -> int:
        return self._id_list

    @id_task.setter
    def id_task(self, id_task: str) -> None:
        self._id_list = id_task

    @property
    def list_name(self) -> str:
        return self._list_name

    @list_name.setter
    def list_name(self, list_name: str) -> None:
        self._list_name = list_name

    @property
    def content(self) -> list[Task]:
        return self._content

    @content.setter
    def content(self, content: list[Task]) -> None:
        self._content = content

    def print_tasks_list(self) -> None:
        print("\n TAREAS")
        print("-" * 85)
        print("| ID | Título                    | Pri | ✓ | Fecha       | Tags          | Descripcion                        |")
        print("-" * 85)

        for task in self.content:
            task.print_task()

        print("-" * 85)
        print(f"Total: {len(self.content)} tareas")



