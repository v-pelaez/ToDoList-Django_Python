import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from typing import Optional, Dict, List

from Classes.TaskList import TaskList
from Classes.Task import Task
from Classes.Utils import Utils


class TaskDialog(tk.Toplevel):
    def __init__(self, parent: tk.Tk, task: Optional[Task] = None) -> None:
        """# Inicializo el modal para crear o editar una tarea."""
        super().__init__(parent)
        self.title("Editar Tarea" if task else "Nueva Tarea")
        self.geometry("400x350")
        self.resizable(False, False)

        # Bloqueo la interacción con la ventana principal mientras este modal esté abierto
        self.transient(parent)
        self.grab_set()

        # Diccionario donde guardaré los datos de retorno
        self.result_data: Optional[Dict[str, str | list[str] | datetime.date | None]] = None

        # Defino las variables reactivas para los inputs
        self.title_var = tk.StringVar(value=task.title if task else "")
        self.priority_var = tk.StringVar(value=task.priority if task else "media")

        # Formateo la fecha si existe, si no, lo dejo en blanco
        deadline_str = task.deadline.isoformat() if task and task.deadline else ""
        self.deadline_var = tk.StringVar(value=deadline_str)
        self.tags_var = tk.StringVar(value=",".join(task.tags) if task else "")

        self._setup_ui()

        # Cargo la descripción manualmente porque el widget Text no soporta variables reactivas simples
        if task:
            self.desc_text.insert(tk.END, task.description)

    def _setup_ui(self) -> None:
        """# Configuro la maquetación del formulario."""
        form_frame = ttk.Frame(self, padding=15)
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="* Título:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.title_var, width=30).grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(form_frame, text="* Prioridad:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Combobox(form_frame, textvariable=self.priority_var, values=Utils.VALID_PRIORITIES, state="readonly",
                     width=27).grid(row=1, column=1, sticky=tk.W, pady=5)

        ttk.Label(form_frame, text="Fecha (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.deadline_var, width=30).grid(row=2, column=1, sticky=tk.W, pady=5)

        ttk.Label(form_frame, text="Tags (separados por coma):").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.tags_var, width=30).grid(row=3, column=1, sticky=tk.W, pady=5)

        ttk.Label(form_frame, text="Descripción:").grid(row=4, column=0, sticky=tk.NW, pady=5)
        self.desc_text = tk.Text(form_frame, width=22, height=4)
        self.desc_text.grid(row=4, column=1, sticky=tk.W, pady=5)

        # Contenedor para la botonera
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=15)
        ttk.Button(buttons_frame, text="Guardar", command=self._save_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Cancelar", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def _save_data(self) -> None:
        """# Valido los campos y empaqueto el resultado antes de destruir el modal."""
        input_title = self.title_var.get().strip()
        if not input_title:
            messagebox.showerror("Error", "El título es obligatorio.", parent=self)
            return

        parsed_deadline = None
        if self.deadline_var.get().strip():
            try:
                parsed_deadline = datetime.strptime(self.deadline_var.get().strip(), "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha incorrecto. Usa YYYY-MM-DD.", parent=self)
                return

        # Asigno el resultado validado
        self.result_data = {
            "title": input_title,
            "priority": self.priority_var.get(),
            "deadline": parsed_deadline,
            "tags": [t.strip() for t in self.tags_var.get().split(",") if t.strip()],
            "description": self.desc_text.get("1.0", tk.END).strip()
        }
        self.destroy()


class MainWindow:
    def __init__(self, root: tk.Tk) -> None:
        """# Inicializo la ventana principal de la aplicación."""
        self.root = root
        self.root.title("To-Do List Manager")
        self.root.geometry("900x600")

        # Instancio la clase que gestiona la lógica de las tareas
        self.task_list = TaskList(1, "Mi Lista")

        # Variables reactivas para la barra de filtros
        self.filter_type_var = tk.StringVar(value="ninguno")
        self.filter_value_var = tk.StringVar(value="")
        self.sort_type_var = tk.StringVar(value="creacion")

        self._setup_ui()
        self._refresh_table()

    def _setup_ui(self) -> None:
        """# Construyo todos los componentes visuales de la ventana base."""
        # 1. Barra de herramientas superior (Acciones CRUD)
        self.toolbar_frame = ttk.Frame(self.root)
        self.toolbar_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(10, 5))

        ttk.Button(self.toolbar_frame, text="Añadir Tarea", command=self._add_task).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar_frame, text="Editar", command=self._edit_task).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar_frame, text="Eliminar", command=self._delete_task).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar_frame, text="Completar", command=self._complete_task).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar_frame, text="Guardar y Salir", command=self._save_and_exit).pack(side=tk.RIGHT, padx=2)

        # 2. Barra secundaria para Filtros y Ordenación
        self.filter_frame = ttk.LabelFrame(self.root, text="Filtros y Ordenación")
        self.filter_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        ttk.Label(self.filter_frame, text="Filtrar por:").pack(side=tk.LEFT, padx=(10, 2))
        filter_options = ttk.Combobox(self.filter_frame, textvariable=self.filter_type_var,
                                      values=("ninguno", "estado", "prioridad", "etiqueta"), state="readonly", width=10)
        filter_options.pack(side=tk.LEFT, padx=2)

        ttk.Label(self.filter_frame, text="Valor:").pack(side=tk.LEFT, padx=(10, 2))
        ttk.Entry(self.filter_frame, textvariable=self.filter_value_var, width=15).pack(side=tk.LEFT, padx=2)

        ttk.Label(self.filter_frame, text="Ordenar por:").pack(side=tk.LEFT, padx=(20, 2))
        sort_options = ttk.Combobox(self.filter_frame, textvariable=self.sort_type_var,
                                    values=("creacion", "fecha", "prioridad"), state="readonly", width=10)
        sort_options.pack(side=tk.LEFT, padx=2)

        ttk.Button(self.filter_frame, text="Aplicar", command=self._refresh_table).pack(side=tk.LEFT, padx=(15, 2))
        ttk.Button(self.filter_frame, text="Limpiar", command=self._clear_filters).pack(side=tk.LEFT, padx=2)

        # 3. Contenedor principal de la tabla (Treeview)
        self.tree_frame = ttk.Frame(self.root)
        self.tree_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        columns = ("id", "title", "priority", "status", "deadline", "tags")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Título")
        self.tree.heading("priority", text="Pri")
        self.tree.heading("status", text="✓")
        self.tree.heading("deadline", text="Fecha")
        self.tree.heading("tags", text="Etiquetas")

        self.tree.column("id", width=40, anchor=tk.CENTER)
        self.tree.column("title", width=250, anchor=tk.W)
        self.tree.column("priority", width=60, anchor=tk.CENTER)
        self.tree.column("status", width=40, anchor=tk.CENTER)
        self.tree.column("deadline", width=100, anchor=tk.CENTER)
        self.tree.column("tags", width=200, anchor=tk.W)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Añado el scroll vertical a la tabla
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _clear_filters(self) -> None:
        """# Reseteo las variables de filtro a sus valores por defecto y recargo la tabla."""
        self.filter_type_var.set("ninguno")
        self.filter_value_var.set("")
        self.sort_type_var.set("creacion")
        self._refresh_table()

    def _refresh_table(self) -> None:
        """# Obtengo los datos filtrados y ordenados del modelo y refresco el Treeview."""
        # Limpio el contenido actual de la tabla
        for row in self.tree.get_children():
            self.tree.delete(row)

        filter_by = self.filter_type_var.get()
        filter_val = self.filter_value_var.get().strip()
        sort_by = self.sort_type_var.get()

        # Ajusto los nulos según espera el backend
        if filter_by == "ninguno" or not filter_val:
            filter_by = None
            filter_val = None

        # Pido la lista procesada al modelo de datos
        tasks_to_display: List[Task] = self.task_list.get_filtered_and_sorted(filter_by, filter_val, sort_by)

        # Pinto las filas resultantes
        for task in tasks_to_display:
            status_str = "✓" if task.completed else "○"
            deadline_str = str(task.deadline) if task.deadline else "-"
            tags_str = ", ".join(task.tags)

            self.tree.insert("", tk.END, values=(
                task.id_task,
                task.title,
                task.priority,
                status_str,
                deadline_str,
                tags_str
            ))

    def _get_selected_index(self) -> Optional[int]:
        """# Busco el índice en memoria de la tarea que el usuario ha seleccionado en la vista."""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Atención", "Selecciona una tarea de la lista primero.")
            return None

        item_values = self.tree.item(selected_items[0], "values")
        task_id = int(item_values[0])

        for idx, task in enumerate(self.task_list.content):
            if task.id_task == task_id:
                return idx
        return None

    def _add_task(self) -> None:
        """# Instancio el modal de creación y proceso los datos si el usuario confirma."""
        dialog = TaskDialog(self.root)
        self.root.wait_window(dialog)

        if dialog.result_data:
            new_id = max([t.id_task for t in self.task_list.content], default=0) + 1
            new_task = Task(id_task=new_id, **dialog.result_data)
            self.task_list.add_task(new_task)
            self._refresh_table()

    def _edit_task(self) -> None:
        """# Recupero la tarea seleccionada, abro el modal con sus datos y aplico las modificaciones."""
        idx = self._get_selected_index()
        if idx is None: return

        target_task = self.task_list.content[idx]
        dialog = TaskDialog(self.root, task=target_task)
        self.root.wait_window(dialog)

        if dialog.result_data:
            target_task.title = dialog.result_data["title"]
            target_task.priority = dialog.result_data["priority"]
            target_task.deadline = dialog.result_data["deadline"]
            target_task.tags = dialog.result_data["tags"]
            target_task.description = dialog.result_data["description"]
            self._refresh_table()

    def _delete_task(self) -> None:
        """# Borro la tarea seleccionada del modelo tras confirmación del usuario."""
        idx = self._get_selected_index()
        if idx is None: return

        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta tarea?"):
            self.task_list.remove_task(idx)
            self._refresh_table()

    def _complete_task(self) -> None:
        """# Cambio el estado de completado de la tarea seleccionada."""
        idx = self._get_selected_index()
        if idx is None: return

        self.task_list.complete_task(idx)
        self._refresh_table()

    def _save_and_exit(self) -> None:
        """# Persisto el estado de memoria al JSON y destruyo la ventana."""
        if self.task_list.save_to_file():
            self.root.destroy()
        else:
            messagebox.showerror("Error", "No se pudieron guardar los cambios en el archivo.")


def main() -> None:
    """# Punto de entrada principal para lanzar el bucle de la UI."""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()