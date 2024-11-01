from OSMPythonTools.nominatim import Nominatim
import pandas as pd
import time
import folium
from fpdf import FPDF
import tkinter as tk
from tkinter import messagebox, filedialog
import webbrowser

data_path = 'data/data.csv'
data = pd.read_csv(data_path, sep=';')

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
    home_status_val = home_status_var.get()
    comentarios_val = comentarios_text.get("1.0", tk.END).strip()

    try:
        lat, lon = convertir_direccion_en_coordenadas(direccion_val)
    except Exception as e:
        messagebox.showerror("Error", f"Dirección Invalida: {e}")
        return

    new_data = {
        "ID": id_val,
        "Dirección": direccion_val,
        "Latitud": lat,
        "Longitud": lon,
        "Agua": agua_val,
        "Comida": comida_val,
        "Ropa": ropa_val,
        "Medicamentos": medicamentos_val,
        "Estado de la vivienda": home_status_val,
        "Comentarios": comentarios_val
    }

    try:
        df = pd.read_csv(data_path, sep=';')
        if int(id_val) in df['ID'].values:
            df.update(pd.DataFrame([new_data]).set_index('ID'))
        else:
            df = df.append(new_data, ignore_index=True)
        df.to_csv(data_path, sep=';', index=False)
        messagebox.showinfo("Éxito", "Datos guardados correctamente")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar los datos: {e}")

def generar_pdf():
    try:
        df = pd.read_csv(data_path, sep=';')
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer los datos: {e}")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Información global de necesidad
    pdf.cell(200, 10, txt="Información Global de Necesidad", ln=True, align='C')
    pdf.ln(10)

    necesidades_globales = {
        "Agua": df["Agua"].sum(),
        "Comida": df["Comida"].sum(),
        "Ropa": df["Ropa"].sum(),
        "Medicamentos": df["Medicamentos"].sum()
    }

    for key, value in necesidades_globales.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    pdf.ln(10)

    # Información por cada ID
    pdf.cell(200, 10, txt="Información por ID", ln=True, align='C')
    pdf.ln(10)

    for index, row in df.iterrows():
        pdf.cell(200, 10, txt=f"ID: {row['ID']}", ln=True)
        pdf.cell(200, 10, txt=f"Dirección: {row['Dirección']}", ln=True)
        pdf.cell(200, 10, txt=f"Latitud: {row['Latitud']}", ln=True)
        pdf.cell(200, 10, txt=f"Longitud: {row['Longitud']}", ln=True)
        pdf.cell(200, 10, txt=f"Agua: {'Sí' if row['Agua'] else 'No'}", ln=True)
        pdf.cell(200, 10, txt=f"Comida: {'Sí' if row['Comida'] else 'No'}", ln=True)
        pdf.cell(200, 10, txt=f"Ropa: {'Sí' if row['Ropa'] else 'No'}", ln=True)
        pdf.cell(200, 10, txt=f"Medicamentos: {'Sí' if row['Medicamentos'] else 'No'}", ln=True)
        pdf.cell(200, 10, txt=f"Estado de la vivienda: {row['Estado de la vivienda']}", ln=True)
        pdf.cell(200, 10, txt=f"Comentarios: {row['Comentarios']}", ln=True)
        pdf.ln(10)

    try:
        pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if pdf_path:
            pdf.output(pdf_path)
            messagebox.showinfo("Éxito", "PDF generado correctamente")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el PDF: {e}")

def cargar_datos():
    id_val = id_entry.get()
    try:
        df = pd.read_csv(data_path, sep=';')
        user_data = df[df['ID'] == int(id_val)]
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
            popup=f"ID: {row['ID']}<br>Dirección: {row['Dirección']}<br>Agua: {'Sí' if row['Agua'] else 'No'}<br>Comida: {'Sí' if row['Comida'] else 'No'}<br>Ropa: {'Sí' if row['Ropa'] else 'No'}<br>Medicamentos: {'Sí' if row['Medicamentos'] else 'No'}<br>Estado de la vivienda: {row['Estado de la vivienda']}<br>Comentarios: {row['Comentarios']}",
        ).add_to(mapa)

    mapa_path = 'mapa.html'
    mapa.save(mapa_path)

    # Mostrar el mapa en una nueva ventana del navegador
    webbrowser.open(mapa_path)
    messagebox.showinfo("Éxito", "Mapa generado y mostrado correctamente")

def crear_nuevo_usuario():
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
    home_status_var.set("Sin desperfectos")
    comentarios_text.delete("1.0", tk.END)
    messagebox.showinfo("Éxito", "Nuevo usuario creado con ID: {}".format(new_id))


root = tk.Tk()
root.title("Formulario de Necesidades")

tk.Label(root, text="ID").grid(row=0, column=0)
id_entry = tk.Entry(root)
id_entry.grid(row=0, column=1)
tk.Button(root, text="Nuevo Usuario", command=crear_nuevo_usuario).grid(row=0, column=2)
tk.Button(root, text="Cargar Usuario", command=cargar_datos).grid(row=0, column=3)

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

root.mainloop()