import sqlite3

NOMBRE_BD = "biblioteca.db"
ESTADOS_VALIDOS = ("leído", "no leído")

CAMPOS_EDITABLES = {
    "1": ("titulo", "Título"),
    "2": ("autor", "Autor"),
    "3": ("genero", "Género"),
    "4": ("estado", "Estado de lectura"),
}



def crear_tabla(conexion):
    """Crea la tabla de libros si no existe."""
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            genero TEXT NOT NULL,
            estado TEXT NOT NULL
        )
    """)
    conexion.commit()


def mostrar_libro(libro):
    """Imprime un libro en una sola línea."""
    id_libro, titulo, autor, genero, estado = libro
    print(
        f"ID: {id_libro} | Título: {titulo} | "
        f"Autor: {autor} | Género: {genero} | Estado: {estado}"
    )


def pedir_texto(mensaje):
    """Pide un texto y repite la pregunta hasta que no esté vacío."""
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("El valor no puede estar vacío.")


def pedir_estado(mensaje):
    """Pide el estado de lectura y repite hasta que sea válido."""
    while True:
        estado = input(mensaje).strip().lower()
        # Aceptamos también la versión sin tilde
        estado = estado.replace("leido", "leído")
        if estado in ESTADOS_VALIDOS:
            return estado
        print("Estado no válido. Escribe 'leído' o 'no leído'.")


def pedir_id(mensaje):
    """Pide un ID numérico. Devuelve None si no es válido."""
    try:
        return int(input(mensaje))
    except ValueError:
        print("Debes ingresar un ID numérico.")
        return None




def agregar_libro(conexion):
    print("\n--- AGREGAR LIBRO ---")

    titulo = pedir_texto("Título: ")
    autor = pedir_texto("Autor: ")
    genero = pedir_texto("Género: ")
    estado = pedir_estado("¿Leído o no leído?: ")

    conexion.execute(
        "INSERT INTO libros (titulo, autor, genero, estado) VALUES (?, ?, ?, ?)",
        (titulo, autor, genero, estado),
    )
    conexion.commit()
    print("Libro agregado correctamente.")


def listar_libros(conexion):
    print("\n--- LISTADO DE LIBROS ---")

    libros = conexion.execute("SELECT * FROM libros").fetchall()

    if not libros:
        print("No hay libros registrados.")
        return

    for libro in libros:
        mostrar_libro(libro)


def buscar_libros(conexion):
    print("\n--- BUSCAR LIBROS ---")

    busqueda = pedir_texto("Escribe el título, autor o género: ")
    patron = f"%{busqueda}%"

    resultados = conexion.execute(
        """
        SELECT * FROM libros
        WHERE titulo LIKE ? OR autor LIKE ? OR genero LIKE ?
        """,
        (patron, patron, patron),
    ).fetchall()

    if not resultados:
        print("No se encontraron libros.")
        return

    for libro in resultados:
        mostrar_libro(libro)


def actualizar_libro(conexion):
    print("\n--- ACTUALIZAR LIBRO ---")

    listar_libros(conexion)

    id_libro = pedir_id("\nIngresa el ID del libro que deseas modificar: ")
    if id_libro is None:
        return

    libro = conexion.execute(
        "SELECT * FROM libros WHERE id = ?", (id_libro,)
    ).fetchone()

    if libro is None:
        print("No existe un libro con ese ID.")
        return

    print("\n¿Qué deseas modificar?")
    for numero, (_, nombre) in CAMPOS_EDITABLES.items():
        print(f"{numero}. {nombre}")

    opcion = input("Selecciona una opción: ").strip()

    if opcion not in CAMPOS_EDITABLES:
        print("Opción no válida.")
        return

    campo, _ = CAMPOS_EDITABLES[opcion]

    if campo == "estado":
        nuevo_valor = pedir_estado("Ingresa el nuevo estado (leído / no leído): ")
    else:
        nuevo_valor = pedir_texto("Ingresa el nuevo valor: ")


    conexion.execute(
        f"UPDATE libros SET {campo} = ? WHERE id = ?",
        (nuevo_valor, id_libro),
    )
    conexion.commit()
    print("Libro actualizado correctamente.")


def eliminar_libro(conexion):
    print("\n--- ELIMINAR LIBRO ---")

    listar_libros(conexion)

    id_libro = pedir_id("\nIngresa el ID del libro que deseas eliminar: ")
    if id_libro is None:
        return

    libro = conexion.execute(
        "SELECT titulo FROM libros WHERE id = ?", (id_libro,)
    ).fetchone()

    if libro is None:
        print("No existe un libro con ese ID.")
        return

    confirmacion = input(f"¿Deseas eliminar '{libro[0]}'? (s/n): ").strip().lower()

    if confirmacion == "s":
        conexion.execute("DELETE FROM libros WHERE id = ?", (id_libro,))
        conexion.commit()
        print("Libro eliminado correctamente.")
    else:
        print("Eliminación cancelada.")




def mostrar_menu():
    print("\n====== GESTOR DE BIBLIOTECA ======")
    print("1. Agregar libro")
    print("2. Actualizar libro")
    print("3. Eliminar libro")
    print("4. Ver todos los libros")
    print("5. Buscar libros")
    print("6. Salir")


def menu(conexion):
    acciones = {
        "1": agregar_libro,
        "2": actualizar_libro,
        "3": eliminar_libro,
        "4": listar_libros,
        "5": buscar_libros,
    }

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "6":
            print("¡Gracias por utilizar el gestor de biblioteca!")
            break

        accion = acciones.get(opcion)
        if accion:
            accion(conexion)
        else:
            print("Opción no válida. Intenta nuevamente.")


def main():
    conexion = sqlite3.connect(NOMBRE_BD)
    try:
        crear_tabla(conexion)
        menu(conexion)
    finally:
        conexion.close()


if __name__ == "__main__":
    main()