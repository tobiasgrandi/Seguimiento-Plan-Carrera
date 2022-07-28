import database
from tkinter import messagebox as mb


def es_correlativa(codigo_mat):
    """COMPRUEBA SI LA MATERIA ES CORRELATIVA DE ALGUNA OTRA PARA PODER ELIMINARLA, RECIBE EL CÓDIGO DE LA MATERIA A ELIMINAR"""

    correlativas_cur = database.run_query("SELECT correlativas_de_cursada FROM plan")
    correlativas_apr = database.run_query("SELECT correlativas_de_aprobado FROM plan")

    for correlativas in correlativas_cur:
        if codigo_mat in correlativas[0]:
            return True

    for correlativas in correlativas_apr:
        if codigo_mat in correlativas[0]:
            return True
    
    return False


def existen_corr(correlativas, toplevel):
    """COMPRUEBA QUE LAS CORRELATIVAS INGRESADAS EXISTAN, RECIBE LAS CORRELATIVAS Y LA VENTANA PADRE"""

    correlativas = correlativas.split("-")
    for correlativa in correlativas:
        if " " in correlativa or not database.existe(correlativa):
            mb.showerror("Error", "Las correlativas ingresadas no existen o el formato de ingreso no es el correcto\nVer Ayuda", parent=toplevel)
            return False
    return True


def corr_aprobadas(correlativas):
    """CHEQUEA SI LAS CORRELATIVAS INGRESADAS ESTÁN APROBADAS, RECIBE UNA LISTA DE CORRELATIVAS"""

    if correlativas != "-":
        correlativas = correlativas.split("-")

        for correlativa in correlativas:
            estado_corr = database.obtener(correlativa, "estado")[0][0]
            if estado_corr != "Aprobada":
                return False
        return True


def ingreso_invalido(toplevel):
    """MUESTRA ERROR SI EL INGRESO NO ES VÁLIDO, RECIBE LA VENTANA PADRE"""
    mb.showerror("Error", """Los campos "Año", "Cuatrimestre", "Nota", "Correlativas de cursada", "Correlativas de aprobado" solo pueden contener números\n
"Cuatrimestre" puede aceptar "Anual" como ingreso""", parent=toplevel)


def eliminar_ingresos(entries):
    """LIMPIA LOS CAMPOS DE INGRESOS, RECIBE LOS DATOS INGRESADOS"""

    for entry in entries:
        entry.delete(0,"end")
        if "combobox2" in str(entry):
            entry.current(0)
        elif "combobox" in str(entry):
            entry.current(4)


def validar_agregar(entries, toplevel):
    """VALIDA QUE LOS DATOS DE LA MATERIA A AGREGAR SEAN VÁLIDOS, RECIBE LOS DATOS Y LA VENTANA PADRE"""

    ingresos = []

    for entry in entries:
        ingreso = entry.get().title()
        if len(ingreso) == 0:
            match entry.widgetName:
                case "codigo"|"año"|"cuatrimestre"|"nombre":
                    mb.showerror("Error", "Debe completar todos los campos obligatorios", parent=toplevel)
                    return
                case _:
                    ingresos.append("-")
        else:
            match entry.widgetName:
                case "año"|"nota" if not ingreso.isdigit():
                    ingreso_invalido(toplevel)
                    return
                case "cuatrimestre" if not ingreso.isdigit() and ingreso != "Anual":
                    ingreso_invalido(toplevel)
                    return
                case "correlativas de cursada"|"correlativas de aprobado" if not existen_corr(ingreso, toplevel):
                    return
                case _:
                    ingresos.append(ingreso)
        
    return ingresos


def validar_modificar(entries, toplevel):
    """VALIDA QUE LOS NUEVOS DATOS DE LA MATERIA A MODIFICAR SEAN VÁLIDOS, RECIBE LOS NUEVOS DATOS Y LA VENTANA PADRE"""

    nuevos_datos = {}

    for entry in entries:

        ingreso = entry.get().title()

        if len(ingreso) > 0:
            match entry.widgetName:
                case "codigo" if database.existe(ingreso) and ingreso != database.obtener(ingreso, "codigo")[0][0]:
                    mb.showerror("Error", "Ya existe una materia con el código ingresado", parent=toplevel)
                    return
                case "año"|"nota" if not ingreso.isdigit():
                    ingreso_invalido(toplevel)
                    return
                case "cuatrimestre" if not ingreso.isdigit() and ingreso != "Anual":
                    ingreso_invalido(toplevel)
                    return
                case "correlativas de cursada"|"correlativas de aprobado" if not existen_corr(ingreso, toplevel):
                    return
                case _:
                    if entry.widgetName == "correlativas de cursada":
                        nuevos_datos["correlativas_de_cursada"] = ingreso
                    elif entry.widgetName == "correlativas de aprobado":
                        nuevos_datos["correlativas_de_aprobado"] = ingreso
                    else:
                        nuevos_datos[entry.widgetName] = ingreso

    return nuevos_datos


def agregar(entries, toplevel, tree, orden):
    """AGREGA UNA NUEVA MATERIA, RECIBE LOS NUEVOS DATOS, LA VENTANA PADRE, EL ÁRBOL Y EL ÓRDEN ACTUAL"""

    ingresos = validar_agregar(entries, toplevel)
    if ingresos:
        if database.add(ingresos[0], ingresos[1], ingresos[2], ingresos[3], ingresos[4], ingresos[5], ingresos[6], ingresos[7], ingresos[8]):
            eliminar_ingresos(entries)
            armar_tree(tree, orden)
            mb.showinfo("Listo", "La materia ha sido agregada correctamente", parent=toplevel)
        else:
            mb.showerror("Error", "Ya existe una materia con el código ingresado", parent=toplevel)


def eliminar(tree, orden):
    """ELIMINA LA MATERIA SELECCIONADA, RECIBE EL ÁRBOL Y EL ÓRDEN ACTUAL"""

    try:
        codigo_mat_elim = tree.item(tree.selection()[0])["text"]

        if not es_correlativa(codigo_mat_elim):
            nombre_mat = database.obtener(codigo_mat_elim, "nombre")[0][0]
            if mb.askyesno("Cuidado", f"Estás por eliminar {nombre_mat}\n¿Desea continuar?"):
                database.delete(codigo_mat_elim)
                armar_tree(tree, orden)
                mb.showinfo("Listo", f"{codigo_mat_elim} - {nombre_mat} borrada correctamente")
        else:
            mb.showerror("Error", "No se puede eliminar una materia que sea correlativa de otras")
        
    
    except:
        mb.showerror("Error", "Debe seleccionar una materia a eliminar")


def armar_tree(tree, orden):
    """AÑADE LOS DATOS AL ÁRBOL, RECIBE EL ÁRBOL Y EL ÓRDEN ACTUAL"""

    records = tree.get_children()

    for element in records:
        tree.delete(element)

    if orden == "Año":
        db_rows = database.run_query("SELECT * FROM plan ORDER BY año DESC, cuatrimestre DESC")
    elif orden == "Nota":
        db_rows = database.run_query("SELECT * FROM plan ORDER BY CASE nota WHEN '-' THEN -99 ELSE nota END")
    else:
        db_rows = database.run_query(f"SELECT * FROM plan ORDER BY {orden} DESC")
    for row in db_rows:
        estado = row[4]
        correlativas_curs = row[6]
        if estado == "Aprobada":
            tree.insert("",0,text=row[0],values=(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]), tags= ("aprobada",))
        elif estado == "Final Pendiente":
            tree.insert("",0,text=row[0],values=(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]), tags= ("final",))
        elif estado == "Recursar":
            tree.insert("",0,text=row[0],values=(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]), tags= ("recursar",))
        elif estado == "Cursando":
            tree.insert("",0,text=row[0],values=(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]), tags= ("cursando",))
        elif corr_aprobadas(correlativas_curs):
            database.update(row[0], {"Estado": "Se puede cursar"})
            tree.insert("",0,text=row[0],values=(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]), tags= ("cursar",))
        else:
            tree.insert("",0,text=row[0],values=(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))


def modificar(mat_a_modificar, entries, toplevel, tree, orden):
    """MODIFICA UNA MATERIA, RECIBE LA MATERIA SELECCIONADA A MODIFICAR, LOS NUEVOS DATOS, LA VENTANA PADRE, EL ÁRBOL Y EL ÓRDEN ACTUAL"""

    nuevos_datos = validar_modificar(entries, toplevel)
    codigo_mat_a_modificar = mat_a_modificar.get()
    
    if nuevos_datos:
        if database.update(codigo_mat_a_modificar, nuevos_datos):
            armar_tree(tree, orden)
            entries.append(mat_a_modificar)
            eliminar_ingresos(entries)
            entries.remove(mat_a_modificar)
            mb.showinfo("Listo","La materia ha sido modificada", parent=toplevel)
        else:
            mb.showerror("Error","No existe materia a modificar con el código ingresado", parent= toplevel)