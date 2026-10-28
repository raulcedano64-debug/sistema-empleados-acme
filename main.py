
from empleados import (
    crear_bd,
    alta_empleado,
    baja_empleado,
    consultar_empleado,
    consultar_todos,
    modificar_empleado
)


def menu():
    crear_bd()

    while True:
        print("\n===================================")
        print("   SISTEMA DE EMPLEADOS ACME")
        print("===================================")
        print("1. Alta de empleado")
        print("2. Baja de empleado")
        print("3. Consulta por CURP")
        print("4. Consulta de todos los empleados")
        print("5. Modificación de empleado")
        print("0. Salir")
        print("===================================")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            alta_empleado()

        elif opcion == "2":
            baja_empleado()

        elif opcion == "3":
            consultar_empleado()

        elif opcion == "4":
            consultar_todos()

        elif opcion == "5":
            modificar_empleado()

        elif opcion == "0":
            print("Gracias por utilizar el sistema ACME.")
            break

        else:
            print("Opción no válida. Intenta nuevamente.")


if __name__ == "__main__":
    menu()

