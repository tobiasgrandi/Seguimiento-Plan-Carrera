import tkinter as tk
import database
from tkinter import Frame, Label, Toplevel, ttk
from tkinter.constants import CENTER, E, N, S, W
from tkinter import messagebox as mb
import auxiliares as aux
import webbrowser as wb

TEXTO_AYUDA_AGR_MAT = """Campos que solo aceptan números:\n- Año\n- Cuatrimestre (también acepta la opción "Anual")
- Nota\nEn los campos de correlativas se ingresan los códigos de las correlativas correspondientes separados por "-"\nEjemplo: 1-2-3 SIN ESPACIOS"""

TEXTO_AYUDA_MOD_MAT = """Ingrese el código de la materia que desea modificar junto con los datos a modificar de la misma.\nCampos que solo aceptan números:\n- Año\n- Cuatrimestre (también acepta la opción "Anual")
- Nota\nEn los campos de correlativas se ingresan los códigos de las correlativas correspondientes separados por "-"\nEjemplo: 1-2-3 SIN ESPACIOS"""

def main():


    def interfaz_ingresos(frame, datos_mat_a_mod = None):
        """INTERFAZ PARA INGRESAR DATOS, RECIBE EL FRAME AL QUE PERTENECE Y SI SE UTILIZA PARA MODIFICAR, TAMBIÉN RECIBE LOS DATOS DE LA MATERIA A MODIFICAR"""

        pad_y = 3
        pad_x = 30
        width_ = 25

        Label(frame, text="Código: ").grid(column=0,row=1)
        codigo = ttk.Entry(frame, width= width_, justify="center")
        codigo.widgetName = "codigo"
        codigo.grid(column=1, row=1, pady= pad_y, padx= pad_x)

        Label(frame, text="Año: ").grid(column=0, row=2)
        año = ttk.Entry(frame, width = width_, justify="center")
        año.widgetName = "año"
        año.grid(column=1, row=2, pady= pad_y, padx= pad_x)

        Label(frame, text="Cuatrimestre: ").grid(column=0, row=3)
        cuatrimestre = ttk.Entry(frame, width = width_, justify="center")
        cuatrimestre.widgetName = "cuatrimestre"
        cuatrimestre.grid(column=1, row=3, pady= pad_y, padx= pad_x)

        Label(frame, text="Nombre: ").grid(column=0, row=4)
        nombre = ttk.Entry(frame, width = width_, justify="center")
        nombre.widgetName = "nombre"
        nombre.grid(column=1, row=4, pady= pad_y, padx= pad_x)

        Label(frame, text="Estado: ").grid(column=0, row=5)
        estado = ttk.Combobox(frame, state="readonly", values=["Cursando", "Aprobada", "Final Pendiente", "Recursar", "Sin Cursar"], width=22, justify="center")
        estado.widgetName = "estado"
        estado.grid(column=1, row=5, pady= pad_y, padx= pad_x)
        estado.current(4)

        Label(frame, text="Nota: ").grid(column=0, row=6)
        nota = ttk.Entry(frame, width = width_, justify="center")
        nota.widgetName = "nota"
        nota.grid(column=1, row=6, pady= pad_y, padx= pad_x)

        Label(frame, text="Códigos correlativas de cursada: ").grid(column=0, row=7)
        correlativas_cur = ttk.Entry(frame, width = width_, justify="center")
        correlativas_cur.widgetName = "correlativas de cursada"
        correlativas_cur.grid(column=1, row=7, pady= pad_y, padx= pad_x)

        Label(frame, text="Códigos correlativas de aprobada: ").grid(column=0, row=8)
        correlativas_apr = ttk.Entry(frame, width = width_, justify="center")
        correlativas_apr.widgetName = "correlativas de aprobado"
        correlativas_apr.grid(column=1, row=8, pady= pad_y, padx= pad_x)

        Label(frame, text="Tipo de materia: ").grid(column=0, row=9)
        tipo_mat = ttk.Combobox(frame, state="readonly", values=["Obligatoria", "Electiva"], width=22, justify="center")
        tipo_mat.widgetName = "tipo de materia"
        tipo_mat.grid(column=1, row=9, pady= pad_y, padx= pad_x)
        tipo_mat.current(0)

        if datos_mat_a_mod:
            
            codigo.insert(0,datos_mat_a_mod[0])
            año.insert(0,datos_mat_a_mod[1])
            cuatrimestre.insert(0,datos_mat_a_mod[2])
            nombre.insert(0,datos_mat_a_mod[3])
            estado.current(estado["values"].index(datos_mat_a_mod[4]))

            if datos_mat_a_mod[5] != "-":
                nota.insert(0,datos_mat_a_mod[5])

            if datos_mat_a_mod[6] != "-":
                correlativas_cur.insert(0,datos_mat_a_mod[6])

            if datos_mat_a_mod[7] != "-":
                correlativas_apr.insert(0,datos_mat_a_mod[7])

            tipo_mat.current(tipo_mat["values"].index(datos_mat_a_mod[8]))
            
            

        entries = [codigo, año, cuatrimestre, nombre, estado, nota, correlativas_cur, correlativas_apr, tipo_mat]

        return entries


    def interfaz_agregar_materia(root, tree, orden):
        """INTERFAZ PARA AGREGAR UNA MATERIA, RECIBE LA RAÍZ, EL ÁRBOL Y EL ÓRDEN ACTUAL"""

        agr_mat = Toplevel(root)
        agr_mat.title("AGREGAR MATERIA")
        agr_mat.grab_set()
        agr_mat.focus_set()
        agr_mat.resizable(0,0)
        
        agr_frame = ttk.LabelFrame(agr_mat, text="AGREGAR MATERIA")
        agr_frame.grid(column=0, row=0)

        entries = interfaz_ingresos(agr_frame)

        Label(agr_frame, text="Código: ", fg= "red").grid(column=0,row=1)
        Label(agr_frame, text="Año: ", fg= "red").grid(column=0, row=2)
        Label(agr_frame, text="Cuatrimestre: ", fg= "red").grid(column=0, row=3)
        Label(agr_frame, text="Nombre: ", fg= "red").grid(column=0, row=4)

        ttk.Button(agr_frame, text="Agregar materia", command=lambda: aux.agregar(entries, agr_mat, tree, orden)).grid(columnspan= 2, row= 10)

        Label(agr_frame, text="Los campos en rojo son obligatorios").grid(column=0,row=11)

        ttk.Button(agr_frame,text="Ayuda", command=lambda: mb.showinfo("Ayuda",TEXTO_AYUDA_AGR_MAT, parent=agr_mat)).grid(column=1, row=11,sticky= S + E, pady= 5, padx= 5)


    def interfaz_modificar_materia(root, tree, orden):
        """INTERFAZ PARA MODIFICAR UNA MATERIA, RECIBE LA RAÍZ, EL ÁRBOL Y EL ÓRDEN ACTUAL"""

        try: #CHEQUEA QUE HAYA UNA MATERIA SELECCIONADA
            
            codigo_mat_a_mod = tree.item(tree.selection()[0])["text"]
            datos_mat_a_mod = database.obtener_todos(codigo_mat_a_mod)[0]

            mod_mat = Toplevel(root)
            mod_mat.title("MODIFICAR MATERIA")
            mod_mat.grab_set()
            mod_mat.focus_set()
            mod_mat.resizable(0,0)

            mod_frame = ttk.LabelFrame(mod_mat, text="MODIFICAR MATERIA")
            mod_frame.grid(column=0, row=0)

            Label(mod_frame, text="Código materia a modificar: ").grid(column=0, row=0)
            mat_a_modificar = ttk.Entry(mod_frame, width=25, justify="center")
            mat_a_modificar.insert(0, codigo_mat_a_mod)
            mat_a_modificar.grid(column=1, row=0, pady=3, padx=30)

            entries = interfaz_ingresos(mod_frame, datos_mat_a_mod)

            ttk.Button(mod_frame, text="Modificar materia", command=lambda: aux.modificar(mat_a_modificar,entries, mod_mat, tree, orden)).grid(columnspan=2, row=10)
            ttk.Button(mod_frame, text="Ayuda", command=lambda: mb.showinfo("Ayuda", TEXTO_AYUDA_MOD_MAT, parent=mod_mat)).grid(column=1, row=11, sticky= S + E, pady= 5, padx= 5)

        except:

            mb.showerror("Error", "Debe seleccionar una materia a modificar")


    def interfaz_tree(root, orden):
        """CREA LA INTERFAZ DEL ÁRBOL EN FORMA DE COLUMNAS Y FILAS JUNTO CON LA BARRA DESPLAZADORA, RECIBE LA RAÍZ Y EL ÓRDEN ACTUAL"""

        style = ttk.Style()

        tree_frame = ttk.Frame(root)
        tree_frame.grid(column= 0, row= 0, rowspan=8, pady= 5, padx= 5)

        tree = ttk.Treeview(tree_frame, columns=("año","cuatrimestre","nombre","estado","nota","correlativas de cursada","correlativas de aprobado","tipo de materia"), selectmode="browse")
        tree.grid(column= 0, row=1)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command= tree.yview)
        vsb.grid(column= 1, row= 1, sticky= N + S)
        tree.configure(yscrollcommand= vsb.set)

        tree.heading("#0", text="Código")
        tree.column("#0", width=80, anchor= CENTER)

        tree.heading("año", text="Año")
        tree.column("año", width=40, anchor=CENTER)

        tree.heading("cuatrimestre", text="Cuatrimestre")
        tree.column("cuatrimestre", width=80, anchor=CENTER)

        tree.heading("nombre", text= "Nombre")
        tree.column("nombre", width=170, anchor=CENTER)

        tree.heading("estado", text="Estado")
        tree.column("estado", width=100, anchor=CENTER)

        tree.heading("nota", text="Nota")
        tree.column("nota", width=40, anchor=CENTER)

        tree.heading("correlativas de cursada", text="Correlativas de cursada")
        tree.column("correlativas de cursada", width=150, anchor=CENTER)

        tree.heading("correlativas de aprobado", text="Correlativas de aprobado")
        tree.column("correlativas de aprobado", width=150, anchor=CENTER)

        tree.heading("tipo de materia", text="Tipo de materia")
        tree.column("tipo de materia", width=90, anchor=CENTER)

        aux.armar_tree(tree, orden)

        return tree


    def interfaz_ppal():
        """CREA LA RAÍZ Y SU CONTENIDO"""

        root = tk.Tk()
        root.title("Plan Carrera - Tobías Grandi")
        root.grid()
        root.resizable(0,0)

        frame_acciones = Frame(root)
        frame_acciones.grid(column=2,row=0, padx = 5, pady = 5)
        
        Label(frame_acciones,text="Filtrar por:").grid(column=0,row=1, sticky=W)
        orden = ttk.Combobox(frame_acciones, state="readonly", values= ["Año","Nombre","Estado","Nota"], justify="center")
        orden.grid(column=0, row=2, sticky= W + E)
        orden.current(0)

        frame_botones = Frame(root)
        frame_botones.grid(column=2, row= 1)

        frame_github = Frame(root)
        frame_github.grid(column=2, row= 7, padx= 7, pady= 5, sticky= E)
        ttk.Button(frame_github, text="GitHub", command=lambda: wb.open("https://python-para-impacientes.blogspot.com/2015/11/abrir-paginas-web-en-un-navegador-con.html", new=0, autoraise= True)).grid(column=0, row=0)
    
        tree = interfaz_tree(root, orden.get())
        tree.tag_configure("aprobada", foreground="black", background="#94FF62")
        tree.tag_configure("cursar", foreground="black", background="#FEF659")
        tree.tag_configure("final", foreground="black", background="#FFBD7A")
        tree.tag_configure("recursar", foreground="black", background="#D3D3D3")
        tree.tag_configure("cursando", foreground="black", background="#7AC1FF")

        orden.bind("<<ComboboxSelected>>", lambda _ : aux.armar_tree(tree, orden.get()))
        ttk.Button(frame_botones,text="Agregar materia", width= 22, command=lambda: interfaz_agregar_materia(root, tree, orden.get())).grid(column= 0, row=0, pady = 5, sticky= W + E)
        ttk.Button(frame_botones,text="Modificar materia", command=lambda: interfaz_modificar_materia(root, tree, orden.get())).grid(column= 0, row=1, pady = 5, sticky= W + E)
        ttk.Button(frame_botones,text="Eliminar materia", command=lambda: aux.eliminar(tree, orden.get())).grid(column= 0, row= 2, pady = 5, sticky= W + E)
        
        root.mainloop()


    interfaz_ppal()

main()