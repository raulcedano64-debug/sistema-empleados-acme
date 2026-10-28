
import sqlite3
import os


# ==========================================
# MODULO 1. CREACION DE LA BASE DE DATOS
# ==========================================

def crear_bd():
    os.makedirs("database", exist_ok=True)

    conexion = sqlite3.connect("database/EMPLEADOS.db")
    cursor = conexion.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleado (
            curp TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            calle TEXT,
            colonia TEXT,
            telefono TEXT,
            edad INTEGER NOT NULL DEFAULT 18,
            sueldo_mensual REAL NOT NULL DEFAULT 0
        )
    """)

    # Agregar los campos si la tabla ya existia
    cursor.execute("PRAGMA table_info(empleado)")
    columnas = [fila[1] for fila in cursor.fetchall()]

    if "edad" not in columnas:
        cursor.execute(
            "ALTER TABLE empleado ADD COLUMN edad INTEGER NOT NULL DEFAULT 18"
        )

    if "sueldo_mensual" not in columnas:
        cursor.execute(
            "ALTER TABLE empleado ADD COLUMN sueldo_mensual REAL NOT NULL DEFAULT 0"
        )

    conexion.commit()
    conexion.close()

    print("Base de datos EMPLEADOS creada correctamente.")


# ==========================================
# MODULO 2. ALTA DE EMPLEADOS
# ==========================================

def alta_empleado():
    conexion = sqlite3.connect("database/EMPLEADOS.db")
    cursor = conexion.cursor()

    print("\n===== ALTA DE EMPLEADO =====")

    curp = input("CURP: ").strip().upper()
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    calle = input("Calle: ").strip()
    colonia = input("Colonia: ").strip()
    telefono = input("Telefono: ").strip()

    if not curp or not nombre or not apellido:
        print("Error: CURP, nombre y apellido son obligatorios.")
        conexion.close()
        return

    try:
        cursor.execute("""
            INSERT INTO empleado
            (curp, nombre, apellido, calle, colonia, telefono)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (curp, nombre, apellido, calle, colonia, telefono))

        conexion.commit()
        print("Empleado registrado correctamente.")

    except sqlite3.IntegrityError:
        print("Error: la CURP ya existe.")

    except sqlite3.Error as error:
        print(f"Error al registrar al empleado: {error}")

    finally:
        conexion.close()


# ==========================================
# MODULO 3. MENU PRINCIPAL
# ==========================================

def menu():
    crear_bd()

    while True:
        print("\n================================")
        print("     ACME S.A. DE C.V.")
        print("   SISTEMA DE EMPLEADOS")
        print("================================")
        print("1. Crear base de datos")
        print("2. Dar de alta a un empleado")
        print("3. Salir")

        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":
            crear_bd()
        elif opcion == "2":
            alta_empleado()
        elif opcion == "3":
            print("Saliendo del sistema...")
            break
        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    menu()
