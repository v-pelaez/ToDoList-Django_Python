import json
import os
from datetime import date, datetime
from typing import Sequence, Any
from Classes.Task import Task


class Utils:
    DEFAULT_FILE = os.path.join("Data", "task.json") # Carpeta y fichero por defecto
    VALID_PRIORITIES = ("alta", "media", "baja") # Prioridades permitidas

    # Diccionario de atributos privados a publicos
    PRIVATE_TO_PUBLIC = {
        '_id_task': 'id_task', '_title': 'title', '_priority': 'priority',
        '_tags': 'tags', '_completed': 'completed', '_description': 'description',
        '_deadline': 'deadline'
    }

    @staticmethod
    def print_menu():
        """ Muestra el menú principal por consola """

        print("\n" + "=" * 40)
        print("       TO DO LIST MANAGER")
        print("=" * 40)
        print("1. Añadir tarea      2. Editar tarea")
        print("3. Eliminar tarea    4. Completar tarea")
        print("5. Mostrar tareas    6. Filtrar y ordenar")
        print("7. Buscar tarea      8. Completar todas")
        print("9. Reiniciar todas   0. Guardar y Salir")
        print("=" * 40)

    @staticmethod
    def get_data_task():
        """ Solicita los datos de una tarea al usuario y los devuelve en un diccionario 
        return: dict con los datos de la tarea"""
        print("\nCrear nueva tarea ([*] Obligatorio [~] Opcional)")

        while True:
            title = input("* Título: ").strip()
            if title:
                break
            print("❌ El título es obligatorio.")

        description = input("~ Descripción: ").strip()

        while True:
            priority = input(f"* Prioridad {Utils.VALID_PRIORITIES} [media]: ").lower().strip() or "media"
            if priority in Utils.VALID_PRIORITIES:
                break
            print(f"❌ Prioridad no válida.")

        tags_input = input("~ Tags (separados por coma): ").strip()
        tags = [t.strip() for t in tags_input.split(",")] if tags_input else []

        deadline = None
        while True:
            date_str = input("~ Fecha límite (DD/MM/YYYY) [Enter para omitir]: ").strip()
            if not date_str:
                break
            try:
                deadline = datetime.strptime(date_str, "%d/%m/%Y").date()
                break
            except ValueError:
                print("❌ Formato incorrecto. Use DD/MM/YYYY.")

        return {
            "title": title, "description": description,
            "priority": priority, "tags": tags, "deadline": deadline
        }

    @staticmethod
    def search_task(my_task_list):
        """ Busca tareas en la lista según un término ingresado por el usuario"""
        query = input("Introduce término de búsqueda: ").lower().strip()
        if not query:
            print("❌ Debe ingresar un término de busqueda.")
            return

        results = [
            task for task in my_task_list.content   # Por cada tarea, si devuelve true lo añade al array
            if query in task.title.lower()          # Si lo contiene el titulo
               or query in task.description.lower() # O si lo contiene la descripción
               or any(query in tag.lower() for tag in task.tags) #o si alguna etiqueta lo contiene
        ]

        if results:
            print(f"\n--- Resultados encontrados para: '{query}' ---")
            my_task_list.print_tasks(tasks_to_print=results, title="RESULTADOS DE BÚSQUEDA")
        else:
            print("❌ No se encontraron coincidencias.")

    @staticmethod
    def save_tasks_list(tasks: Sequence[Task], filepath: str = DEFAULT_FILE) -> bool:
        """ Guarda la lista de tareas en un archivo JSON.
        return: True si se guardó correctamente, False en caso contrario """
        def date_serializer(obj: Any) -> str:
            if isinstance(obj, (date, datetime)): return obj.isoformat()
            raise TypeError(f"No serializable: {type(obj)}")

        try:
            data = []
            for task in tasks:
                task_dict = {Utils.PRIVATE_TO_PUBLIC.get(k, k): v for k, v in task.__dict__.items()}
                data.append(task_dict)

            os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, default=date_serializer, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
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
        return: lista de objetos Task """
        tasks = []
        for d in data:
            deadline = None
            if d.get('deadline'):
                try:
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

    @staticmethod
    def conf_filter_sorter(my_task_list):
        """ Configura y aplica filtros y ordenamientos a la lista de tareas """
        print("\n--- Opciones de Filtrado ---")
        print("1. Por Estado | 2. Por Prioridad | 3. Por Etiqueta | 4. Sin filtro")
        f_opc = input("Selecciona: ")

        f_by, f_val = None, None
        if f_opc == "1":
            f_by = "estado"
            val = input("¿completada o pendiente?: ").lower().strip()
            f_val = "completada" if val.startswith("comp") else "pendiente"
        elif f_opc == "2":
            f_by = "prioridad"
            while True:
                f_val = input(f"Prioridad {Utils.VALID_PRIORITIES}: ").lower().strip()
                if f_val in Utils.VALID_PRIORITIES: break
                print("❌ Prioridad no válida.")
        elif f_opc == "3":
            f_by = "etiqueta"
            f_val = input("Etiqueta a buscar: ").strip()

        print("\n--- Opciones de Orden ---")
        print("1. Fecha límite | 2. Prioridad | 3. ID (Creación)")
        s_opc = input("Selecciona: ")

        sort_map = {"1": "fecha", "2": "prioridad", "3": "creacion"}
        s_by = sort_map.get(s_opc, "creacion")

        final_list = my_task_list.get_filtered_and_sorted(f_by, f_val, s_by)
        my_task_list.print_tasks(final_list, title="VISTA FILTRADA Y ORDENADA")