from OSMPythonTools.nominatim import Nominatim
import pandas as pd
import time
import folium
from fpdf import FPDF
import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.ttk as ttk
import webbrowser
from DataGestor import DataGestor
from PDFCreator import PDFCreator

data_path = 'data/data.csv'
data_gestor = DataGestor(data_path)

internet_connection = False

def convertir_direccion_en_coordenadas(direccion):
    nominatim = Nominatim()
    coordenadas = nominatim.query(direccion).toJSON()
    return coordenadas[0]['lat'], coordenadas[0]['lon']

def guardar_datos():
    id_val = id_entry.get()
    direccion_val = direccion_entry.get()
    agua_val = agua_var.get()
    comida_val = comida_var.get()
    ropa_val = ropa_var.get()
    medicamentos_val = medicamentos_var.get()
    actividad_val = actividad_var.get()
    home_status_val = home_status_var.get()
    comentarios_val = comentarios_text.get("1.0", tk.END).strip()

    if internet_connection:
        try:
            lat, lon = convertir_direccion_en_coordenadas(direccion_val)
        except Exception as e:
            messagebox.showerror("Error", f"Dirección Invalida: {e}")
            return
    else:
        lat = 0
        lon = 0
    
    data_gestor.set_values(
        id_val, lat, lon, direccion_val, agua_val, comida_val, ropa_val, medicamentos_val, actividad_val, home_status_val, comentarios_val
    )
    messagebox.showinfo("Éxito", "Datos guardados correctamente")

def generar_pdf():
    pdf_creator = PDFCreator(data_gestor)
    pdf_creator.generar_pdf()

def cargar_datos():
    id_val = id_entry.get()
    try:
        user_data = data_gestor.get_data_by_id(int(id_val))
        if user_data.empty:
            messagebox.showerror("Error", "ID no encontrado")
            return

        user_data = user_data.iloc[0]
        direccion_entry.delete(0, tk.END)
        direccion_entry.insert(0, user_data['Dirección'])
        agua_var.set(bool(user_data['Agua']))
        comida_var.set(bool(user_data['Comida']))
        ropa_var.set(bool(user_data['Ropa']))
        medicamentos_var.set(bool(user_data['Medicamentos']))
        actividad_var.set(bool(user_data['Actividad']))
        home_status_var.set(user_data['Estado de la vivienda'])
        comentarios_text.delete("1.0", tk.END)
        comentarios_text.insert(tk.END, user_data['Comentarios'])
        messagebox.showinfo("Éxito", "Datos cargados correctamente")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar los datos: {e}")

def mostrar_mapa():
    try:
        df = pd.read_csv(data_path, sep=';')
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer los datos: {e}")
        return

    mapa = folium.Map(location=[df['Latitud'].mean(), df['Longitud'].mean()], zoom_start=12)

    for index, row in df.iterrows():
        folium.Marker(
            location=[row['Latitud'], row['Longitud']],
            popup=f"<b>ID:</b> {row['ID']} <br> <b>Dirección:</b> {row['Dirección']}<br><b>Agua:</b> {'Sí' if row['Agua'] else 'No'}<br><b>Comida:</b> {'Sí' if row['Comida'] else 'No'}<br><b>Ropa:</b> {'Sí' if row['Ropa'] else 'No'}<br><b>Medicamentos:</b> {'Sí' if row['Medicamentos'] else 'No'}<br><b>Estado de la vivienda:</b> {row['Estado de la vivienda']}<br><b>Comentarios:</b> {row['Comentarios']}",
        ).add_to(mapa)

    mapa_path = 'mapa.html'
    mapa.save(mapa_path)

def crear_nueva_incidencia():
    try:
        df = pd.read_csv(data_path, sep=';')
        if df['ID'].empty:
            new_id = 1
        else:
            new_id = df['ID'].max() + 1
    except Exception as e:
        new_id = 1  # Si no se puede leer el archivo, empezamos con ID 1

    id_entry.delete(0, tk.END)
    id_entry.insert(0, new_id)
    direccion_entry.delete(0, tk.END)
    agua_var.set(False)
    comida_var.set(False)
    ropa_var.set(False)
    medicamentos_var.set(False)
    actividad_var.set(False)
    home_status_var.set("Sin desperfectos")
    comentarios_text.delete("1.0", tk.END)
    messagebox.showinfo("Éxito", "Nuevo usuario creado con ID: {}".format(new_id))

def actualizar_coordenadas():
    try:
        df = pd.read_csv(data_path, sep=';')
        for index, row in df.iterrows():
            if row['Latitud'] == 0.0 and row['Longitud'] == 0.0:
                try:
                    lat, lon = convertir_direccion_en_coordenadas(row['Dirección'])
                    df.at[index, 'Latitud'] = lat
                    df.at[index, 'Longitud'] = lon
                except Exception as e:
                    messagebox.showwarning("Advertencia", f"No se pudo actualizar la dirección: {row['Dirección']}")
        df.to_csv(data_path, sep=';', index=False)
        messagebox.showinfo("Éxito", "Coordenadas actualizadas correctamente")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar el archivo: {e}")

def guardar_estado_internet():
    with open("internet_status.txt", "w") as f:
        f.write("1" if internet_connection else "0")

def toggle_internet_connection():
    global internet_connection
    internet_connection = not internet_connection
    internet_status_label.config(text="Conectado" if internet_connection else "Desconectado")
    guardar_estado_internet()
    if internet_connection:
        actualizar_coordenadas()

root = tk.Tk()
root.title("Formulario de Necesidades")

tk.Label(root, text="ID").grid(row=0, column=0)
id_entry = tk.Entry(root)
id_entry.grid(row=0, column=1)
tk.Button(root, text="Nueva Incidencia", command=crear_nueva_incidencia).grid(row=0, column=2)
tk.Button(root, text="Cargar Incidencia", command=cargar_datos).grid(row=0, column=3)

tk.Label(root, text="Dirección").grid(row=1, column=0)
direccion_entry = tk.Entry(root)
direccion_entry.grid(row=1, column=1)

agua_var = tk.BooleanVar()
tk.Checkbutton(root, text="Agua", variable=agua_var).grid(row=2, column=0)

comida_var = tk.BooleanVar()
tk.Checkbutton(root, text="Comida", variable=comida_var).grid(row=2, column=1)

ropa_var = tk.BooleanVar()
tk.Checkbutton(root, text="Ropa", variable=ropa_var).grid(row=2, column=2)

medicamentos_var = tk.BooleanVar()
tk.Checkbutton(root, text="Medicamentos", variable=medicamentos_var).grid(row=2, column=3)

actividad_var = tk.BooleanVar()
tk.Checkbutton(root, text="Actividad", variable=actividad_var).grid(row=2, column=4)


tk.Label(root, text="Estado de la vivienda").grid(row=3, column=0)
home_status_var = tk.StringVar()
home_status_var.set("Sin desperfectos")
tk.OptionMenu(root, home_status_var, "Sin desperfectos", "Con algunos desperfectos", "No habitable").grid(row=3, column=1)

tk.Label(root, text="Comentarios").grid(row=4, column=0)
comentarios_text = tk.Text(root, height=4, width=40)
comentarios_text.grid(row=4, column=1, columnspan=3)

tk.Button(root, text="Guardar Datos", command=guardar_datos).grid(row=5, column=1)
tk.Button(root, text="Generar PDF", command=generar_pdf).grid(row=5, column=2)
tk.Button(root, text="Mostrar Mapa", command=mostrar_mapa).grid(row=5, column=3)

internet_var = tk.BooleanVar(value=internet_connection)
toggle_button = ttk.Checkbutton(root, text="Conexión a Internet", variable=internet_var, style="Switch.TCheckbutton", command=toggle_internet_connection)
toggle_button.grid(row=6, column=0, columnspan=2)

internet_status_label = tk.Label(root, text="Desconectado", font=("Arial", 10))
internet_status_label.grid(row=6, column=2)

root.mainloop()