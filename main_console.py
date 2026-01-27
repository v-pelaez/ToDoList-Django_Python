from datetime import datetime

from Classes.TaskList import TaskList
from Classes.Task import Task

myTaskList = TaskList(1, "Mi Lista")

while True:


    print("=" * 40)
    print("       TO DO LIST MANAGER")
    print("=" * 40)
    print("1. Añadir tarea")
    print("2. Eliminar tarea")
    print("3. Completar tarea")
    print("4. Completar todas")
    print("5. Reiniciar todas")
    print("6. Mostrar tareas")
    print("0. Salir")
    print("=" * 40)

    opcion = input("\nElige opción: ").strip()

    match opcion:
        case "1":
            try :
                print("Crear nueva tarea.")
                print(" [*] Obligatorio"
                      " [~] Opcional")
                title = input("* Título: ")
                description = input("~ Descripcion: ")
                priority = input("* Prioridad (alta/media/baja): ") or "media"
                tags_input = input("~ Tags (separados por coma): ")
                tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
                fecha_str = input("~ Fecha limite(DD/MM/YYYY): ")
                if fecha_str and len(fecha_str) > 0:
                    fecha_date = datetime.strptime(fecha_str, "%d/%m/%Y").date()
                else:
                    fecha_date = None


                my_task = Task(
                    id_task=len(myTaskList.content) + 1,
                    title=title,
                    priority=priority,
                    tags=tags,
                    completed=False,
                    deadline=fecha_date,
                    description=description,
                )
                myTaskList.add_task(my_task)
            except:
                print("Hubo un problema, por favor intente nuevamente y respete el formato de los campos")
            input("\nEnter para continuar...")

        case "2":
            try:
                idx = int(input("Índice a eliminar: "))-1
                myTaskList.remove_task(idx)
            except:
                print("Índice inválido")
            input("\nEnter para continuar...")

        case "3":
            try:
                idx = int(input("Índice a completar: "))-1
                myTaskList.complete_task(idx)
            except:
                print("Índice inválido")
            input("\nEnter para continuar...")

        case "4":
            myTaskList.complete_all()
            print("Todas completadas")
            input("\nEnter para continuar...")

        case "5":
            myTaskList.restart_all()
            print("Todas reiniciadas")
            input("\nEnter para continuar...")

        case "6":
            myTaskList.print_tasks_list()
            input("\nEnter para continuar...")

        case "0":
            myTaskList.save_to_file()
            print("¡Hasta luego!")
            break

        case _:
            print("Opción inválida")
            input("\nEnter para continuar...")
