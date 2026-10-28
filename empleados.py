

import sqlite3
import os

RUTA_BD = "database/EMPLEADOS.db"


# ==========================================
# MODULO 1. CREACION DE LA BASE DE DATOS
# ==========================================

def conectar():
    os.makedirs("database", exist_ok=True)
    return sqlite3.connect(RUTA_BD)


def crear_bd():
    conexion = conectar()
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
    print("Base de datos EMPLEADOS lista.")


# ==========================================
# MODULO 2. ALTA DE EMPLEADOS
# ==========================================

def alta_empleado():
    print("\n===== ALTA DE EMPLEADO =====")

    curp = input("CURP: ").strip().upper()
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    calle = input("Calle: ").strip()
    colonia = input("Colonia: ").strip()
    telefono = input("Telefono: ").strip()

    if not curp or not nombre or not apellido:
        print("CURP, nombre y apellido son obligatorios.")
        return

    try:
        edad = int(input("Edad: "))
        sueldo = float(input("Sueldo mensual: "))

        if edad < 0 or sueldo < 0:
            print("Edad y sueldo no pueden ser negativos.")
            return
    except ValueError:
        print("Error: escribe una edad y un sueldo validos.")
        return

    conexion = conectar()

    try:
        conexion.execute("""
            INSERT INTO empleado
            (curp, nombre, apellido, calle, colonia, telefono,
             edad, sueldo_mensual)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (curp, nombre, apellido, calle, colonia,
              telefono, edad, sueldo))

        conexion.commit()
        print("Empleado registrado correctamente.")

    except sqlite3.IntegrityError:
        print("Error: esa CURP ya esta registrada.")
    except sqlite3.Error as error:
        print(f"Error: {error}")
    finally:
        conexion.close()


# ==========================================
# MODULO 3. CONSULTA POR CURP
# ==========================================

def consultar_curp():
    curp = input("CURP del empleado: ").strip().upper()
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM empleado WHERE curp = ?", (curp,)
    )
    empleado = cursor.fetchone()
    conexion.close()

    if empleado:
        mostrar_empleado(empleado)
    else:
        print("No se encontro el empleado.")


# ==========================================
# MODULO 4. CONSULTA DE TODOS LOS REGISTROS
# ==========================================

def consultar_todos():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT curp, nombre, apellido, calle, colonia,
               telefono, edad, sueldo_mensual
        FROM empleado
        ORDER BY apellido, nombre
    """)

    empleados = cursor.fetchall()
    conexion.close()

    if not empleados:
        print("No hay empleados registrados.")
        return

    for empleado in empleados:
        mostrar_empleado(empleado)


def mostrar_empleado(empleado):
    nombres = [
        "CURP", "Nombre", "Apellido", "Calle",
        "Colonia", "Telefono", "Edad", "Sueldo mensual"
    ]

    print("\n-----------------------------")
    for nombre, valor in zip(nombres, empleado):
        print(f"{nombre}: {valor}")
    print("-----------------------------")


# ==========================================
# MODULO 5. BAJA DE EMPLEADOS
# ==========================================

def baja_empleado():
    curp = input("CURP del empleado a eliminar: ").strip().upper()
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT nombre, apellido FROM empleado WHERE curp = ?", (curp,)
    )
    empleado = cursor.fetchone()

    if not empleado:
        print("No se encontro el empleado.")
        conexion.close()
        return

    print(f"Empleado: {empleado[0]} {empleado[1]}")
    confirmar = input("¿Confirmas la baja? (s/n): ").strip().lower()

    if confirmar == "s":
        cursor.execute("DELETE FROM empleado WHERE curp = ?", (curp,))
        conexion.commit()
        print("Empleado eliminado correctamente.")
    else:
        print("Baja cancelada.")

    conexion.close()


# ==========================================
# MODULO 6. MODIFICACION DE EMPLEADOS
# ==========================================

def modificar_empleado():
    curp = input("CURP del empleado a modificar: ").strip().upper()
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM empleado WHERE curp = ?", (curp,))
    empleado = cursor.fetchone()

    if not empleado:
        print("No se encontro el empleado.")
        conexion.close()
        return

    print("Deja vacio un campo para conservar su valor actual.")

    nombre = input(f"Nombre [{empleado[1]}]: ").strip() or empleado[1]
    apellido = input(f"Apellido [{empleado[2]}]: ").strip() or empleado[2]
    calle = input(f"Calle [{empleado[3] or ''}]: ").strip() or empleado[3]
    colonia = input(f"Colonia [{empleado[4] or ''}]: ").strip() or empleado[4]
    telefono = input(f"Telefono [{empleado[5] or ''}]: ").strip() or empleado[5]

    try:
        edad_txt = input(f"Edad [{empleado[6]}]: ").strip()
        sueldo_txt = input(f"Sueldo mensual [{empleado[7]}]: ").strip()

        edad = int(edad_txt) if edad_txt else empleado[6]
        sueldo = float(sueldo_txt) if sueldo_txt else empleado[7]

        if edad < 0 or sueldo < 0:
            raise ValueError
    except ValueError:
        print("Edad o sueldo no validos.")
        conexion.close()
        return

    cursor.execute("""
        UPDATE empleado
        SET nombre = ?, apellido = ?, calle = ?, colonia = ?,
            telefono = ?, edad = ?, sueldo_mensual = ?
        WHERE curp = ?
    """, (nombre, apellido, calle, colonia, telefono,
          edad, sueldo, curp))

    conexion.commit()
    conexion.close()
    print("Empleado modificado correctamente.")


# ==========================================
# MODULO 7. MENU PRINCIPAL
# ==========================================

def menu():
    crear_bd()

    while True:
        print("\n================================")
        print("       ACME S.A. DE C.V.")
        print("       SISTEMA DE EMPLEADOS")
        print("================================")
        print("1. Alta de empleado")
        print("2. Baja de empleado")
        print("3. Consulta por CURP")
        print("4. Consulta de todos los registros")
        print("5. Modificacion de empleado")
        print("6. Salir")

        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":
            alta_empleado()
        elif opcion == "2":
            baja_empleado()
        elif opcion == "3":
            consultar_curp()
        elif opcion == "4":
            consultar_todos()
        elif opcion == "5":
            modificar_empleado()
        elif opcion == "6":
            print("Saliendo del sistema...")
            break
        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    menu()

