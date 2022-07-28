import sqlite3
BD = 'plan.db'


def run_query(query, parametros = ()):
    """EJECUTA LA PETICIÓN SOLICITADA CON LOS PARÁMETROS PASADOS"""

    bd =  sqlite3.connect(BD)
    cursor = bd.cursor()
    resultado = cursor.execute(query, parametros).fetchall()
    bd.commit()
    cursor.close()
    bd.close()
    return resultado


def crear_tabla(nombre_tabla):
    """CREA UNA TABLA CON LAS COLUMNAS YA PREDEFINIDAS"""

    query = [
        """
        CREATE TABLE IF NOT EXISTS '{}'(
            Codigo TEXT NOT NULL,
            Año INTEGER NOT NULL,
            Cuatrimestre INTEGER NOT NULL,
            Nombre TEXT NOT NULL,
            Estado TEXT NOT NULL,
            Nota INTEGER NOT NULL,
            'Correlativas_de_cursada' TEXT,
            'Correlativas_de_aprobado' TEXT,
            'Tipo de materia' TEXT
        )
        """]
        
    run_query(query[0].format(nombre_tabla))


def inicializar():
    """COMPRUEBA SI EXISTE LA TABLA PLAN, SI NO EXISTE LA CREA"""

    query = """SELECT name FROM sqlite_master WHERE type='table'"""
    rquery = run_query(query)
    if not rquery or 'plan' not in rquery:
        crear_tabla("plan")

inicializar()

def add(codigo, año, cuatrimestre, nombre, estado, nota, correlativas_cur, correlativas_apr, tipo_mat):
    """AÑADE UNA MATERIA A LA TABLA PLAN"""

    parametros = (codigo, año, cuatrimestre, nombre, estado, nota, correlativas_cur, correlativas_apr, tipo_mat)

    if not existe(codigo):
        query = """INSERT INTO plan (Codigo, Año, Cuatrimestre, Nombre, Estado, Nota, 'Correlativas_de_cursada', 'Correlativas_de_aprobado', 'Tipo de materia') VALUES (?,?,?,?,?,?,?,?,?)"""
        run_query(query,parametros)
        return True
    else:
        return False


def obtener(codigo, param_obtener):
    """DEVUELVE EL PARÁMETRO SOLICITADO DE LA MATERIA CORRESPONDIENTE AL CÓDIGO"""

    query = f"""SELECT {param_obtener} FROM plan WHERE Codigo = ?"""
    return run_query(query, (codigo,))


def obtener_todos(codigo):
    """DEVUELVE TODOS LOS DATOS DE LA MATERIA CORRESPONDIENTE AL CÓDIGO"""

    query = """SELECT * FROM plan WHERE Codigo = ?"""
    return run_query(query, (codigo,))


def update(codigo, nuevos_datos):
    """RECIBE EL CÓDIGO DE LA MATERIA JUNTO CON LAS COLUMNAS A MODIFICAR CON SUS NUEVOS DATOS"""

    if existe(codigo):
        for columna in nuevos_datos:
            query = """UPDATE plan SET '{}'='{}' WHERE Codigo = ?""".format(columna, nuevos_datos[columna])
            run_query(query, (codigo,))
            if columna == "codigo":
                codigo = nuevos_datos[columna]
        return True
    else:
        return False


def delete(codigo):
    """ELIMINA UNA MATERIA POR SU CÓDIGO"""

    if existe(codigo):
        query = "DELETE FROM plan WHERE Codigo = ?"
        run_query(query, (codigo,))
        return True
    else:
        return False


def existe(codigo):

    """COMPRUEBA LA EXISTENCIA DE UNA MATERIA POR SU CÓDIGO"""

    if len(obtener(codigo, "nombre")) != 0:
        return True
    else:
        return False
