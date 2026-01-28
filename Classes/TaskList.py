from Classes.Task import Task
from Classes.Utils import Utils

class TaskList:
    def __init__(self, id_list: int, list_name: str, filepath: str = Utils.DEFAULT_FILE):
        """Constructor de la clase TaskList."""
        self._id_list, self._list_name, self.filepath = id_list, list_name, filepath
        self._content = []
        self.load_from_file()  # Auto-carga

    def load_from_file(self) -> bool:
        """Carga la lista de tareas desde el archivo. Retorna True si tuvo éxito, False si no."""
        try:
            self._content = Utils.dicts_to_tasks(Utils.load_tasks_list(self.filepath))
            return True
        except (FileNotFoundError, ValueError):
            return False

    def save_to_file(self) -> bool:
        """Guarda la lista de tareas en el archivo. Retorna True si tuvo éxito, False si no."""
        return Utils.save_tasks_list(self._content, self.filepath)


    def add_task(self, task: Task) -> None:
        """Agrega una tarea a la lista."""
        self.content.append(task)

    def remove_task(self, index: int) -> None:
        """Elimina una tarea de la lista por su índice."""
        self.content.pop(index)

    def complete_task(self, index: int) -> None:
        """Marca una tarea como completada por su índice."""
        self.content[index].completed = True

    def complete_all(self) -> None:
        """Marca todas las tareas como completadas."""
        for task in self.content:
            task.completed = True

    def restart_all(self) -> None:
        """Marca todas las tareas como no completadas."""
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

    def print_tasks(self, tasks_to_print: list[Task] = None, title: str = "TAREAS") -> None:
        """Imprime la lista de tareas en formato de tabla. Acepta una lista opcional de tareas a imprimir."""
        
        # Si no pasan una lista específica, usamos el contenido total
        target_list = tasks_to_print if tasks_to_print is not None else self.content

        print(f"\n {title.upper()}")
        print("-" * 85)
        print("| ID | Título                    | Pri | ✓ | Fecha       | Tags          | Descripcion                        |")
        print("-" * 85)

        if not target_list:
            print("| " + "No hay tareas para mostrar".center(81) + " |")
        else:
            for task in target_list:
                task.print_task()

        print("-" * 85)
        print(f"Total: {len(target_list)} tareas")

    def get_filtered_and_sorted(self, filter_by=None, filter_val=None, sort_by="creacion"):
        """Filtra y ordena las tareas por criterios."""

        filtered_list = []
        for task in self.content:
            if filter_by == "estado":
                is_completed = (filter_val == "completada")
                if task.completed == is_completed:
                    filtered_list.append(task)
            elif filter_by == "prioridad":
                if task.priority == filter_val:
                    filtered_list.append(task)
            elif filter_by == "etiqueta":
                for tag in task.tags:
                    if filter_val.lower() in tag.lower():
                        filtered_list.append(task)
                        break
            else:
                filtered_list.append(task)

        # Funciones de ayuda para ordenación
        def by_date(task):
            # True va después de False; así las tareas sin fecha (None) aparecen al final
            return (task.deadline is None, task.deadline)

        def by_priority(task):
            pesos = {"alta": 0, "media": 1, "baja": 2}
            return pesos.get(task.priority, 3)

        def by_id(task):
            return task.id_task

        # Aplicar la ordenación
        if sort_by == "fecha":
            filtered_list.sort(key=by_date)
        elif sort_by == "prioridad":
            filtered_list.sort(key=by_priority)
        else:
            filtered_list.sort(key=by_id)

        return filtered_list