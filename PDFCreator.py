from fpdf import FPDF
from tkinter import messagebox, filedialog

class PDFCreator:
    def __init__(self, data_gestor):
        self.data_gestor = data_gestor

    def generar_pdf(self):
        try:
            df = self.data_gestor.read_data()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer los datos: {e}")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Información global de necesidad
        pdf.cell(200, 10, txt="Información Global de Necesidad", ln=True, align='C')

        if 'Agua' in df.columns:
            df['AGUA_NUM'] = df['Agua'].apply(lambda x: 1 if x else 0)
        if 'Comida' in df.columns:
            df['COMIDA_NUM'] = df['Comida'].apply(lambda x: 1 if x else 0)
        if 'Ropa' in df.columns:
            df['ROPA_NUM'] = df['Ropa'].apply(lambda x: 1 if x else 0)
        if 'Medicamentos' in df.columns:
            df['MEDICAMENTOS_NUM'] = df['Medicamentos'].apply(lambda x: 1 if x else 0)
        if 'Actividad' in df.columns:
            df['ACTIVIDAD_NUM'] = df['Actividad'].apply(lambda x: 1 if x else 0)


        necesidades_globales = {
            "Agua": df['AGUA_NUM'].sum(),
            "Comida": df['COMIDA_NUM'].sum(),
            "Ropa": df['ROPA_NUM'].sum(),
            "Medicamentos": df['MEDICAMENTOS_NUM'].sum(),
            "Actividad": df['ACTIVIDAD_NUM'].sum()
        }

        for key, value in necesidades_globales.items():
            pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

        # Información por cada ID
        pdf.cell(200, 10, txt="Información por ID", ln=True, align='C')

        for index, row in df.iterrows():
            pdf.cell(200, 10, txt=f"ID: {row['ID']} - Nombre: {row['Nombre']}", ln=True)
            pdf.cell(200, 10, txt=f"Dirección: {row['Dirección']}", ln=True)
            pdf.cell(200, 10, txt=f"Agua: {'Sí' if row['Agua'] else 'No'} | Comida: {'Sí' if row['Comida'] else 'No'} | Ropa: {'Sí' if row['Ropa'] else 'No'} | Medicamentos: {'Sí' if row['Medicamentos'] else 'No'}", ln=True)
            pdf.cell(200, 10, txt=f"Estado de la vivienda: {row['Estado de la vivienda']}", ln=True)
            pdf.cell(200, 10, txt=f"Comentarios: \n {row['Comentarios']}", ln=True)
            pdf.ln(10)

        try:
            pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if pdf_path:
                pdf.output(pdf_path)
                messagebox.showinfo("Éxito", "PDF generado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF: {e}")