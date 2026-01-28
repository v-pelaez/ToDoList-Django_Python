from Classes.TaskList import TaskList
from Classes.Task import Task
from Classes.Utils import Utils


def main():
    my_task_list = TaskList(1, "Mi Lista")

    while True:
        Utils.print_menu()
        opcion = input("\nElige opción: ").strip()

        try:
            match opcion:
                case "1":  # Añadir
                    data = Utils.get_data_task()
                    new_task = Task(id_task=len(my_task_list.content) + 1, **data)
                    my_task_list.add_task(new_task)
                    print("✅ Tarea añadida.")

                case "2":  # Editar
                    idx = int(input("ID de la tarea a editar: ")) - 1
                    task = my_task_list.content[idx]
                    task.title = input(f"Nuevo título [{task.title}]: ") or task.title
                    task.description = input(f"Nueva descripción [{task.description}]: ") or task.description
                    task.priority = input(f"Nueva prioridad [{task.priority}]: ") or task.priority
                    print("✨ Tarea actualizada.")

                case "3":  # Eliminar
                    idx = int(input("ID a eliminar: ")) - 1
                    my_task_list.remove_task(idx)

                case "4":  # Completar una
                    idx = int(input("ID a completar: ")) - 1
                    my_task_list.complete_task(idx)

                case "5":  # Mostrar
                    my_task_list.print_tasks()

                case "6":  # Filtrado y Orden Avanzado
                    Utils.conf_filter_sorter(my_task_list)

                case "7":  # Buscar
                    Utils.search_task(my_task_list)

                case "8":  # Completar todas
                    my_task_list.complete_all()
                    print("✅ Todas completadas.")

                case "9":  # Reiniciar todas
                    my_task_list.restart_all()
                    print("🔄 Todas reiniciadas.")



                case "0":
                    my_task_list.save_to_file()
                    print("¡Hasta luego!")
                    break

        except (ValueError, IndexError):
            print("❌ Error: Entrada no válida.")

        input("\nEnter para continuar...")



main()