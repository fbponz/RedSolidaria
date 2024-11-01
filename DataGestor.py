import pandas as pd

class DataGestor:

    def __init__(self, file_path='data/data.csv'):
        self.file_path = file_path
        self.data = pd.read_csv(self.file_path)

    def set_values(self, id_val, lat, lon, direccion_val, agua_val, comida_val, ropa_val, medicamentos_val, actividad_val, home_status_val, comentarios_val):
        new_data = {
            "ID": id_val,
            "Dirección": direccion_val,
            "Latitud": lat,
            "Longitud": lon,
            "Agua": agua_val,
            "Comida": comida_val,
            "Ropa": ropa_val,
            "Medicamentos": medicamentos_val,
            "Actividad": actividad_val,
            "Estado de la vivienda": home_status_val,
            "Comentarios": comentarios_val
        }

        try:
            df = pd.read_csv(self.file_path, sep=';')
            if int(id_val) in df['ID'].values:
                df.update(pd.DataFrame([new_data]).set_index('ID'))
            else:
                df = df.append(new_data, ignore_index=True)
            df.to_csv(self.file_path, sep=';', index=False)
            return "Success", "Datos guardados correctamente"
        except Exception as e:
            return "Error", f"No se pudo guardar los datos: {e}"

    def read_data(self):
        self.data = pd.read_csv(self.file_path)

    def get_data_by_id(self, id_val):
        try:
            df = pd.read_csv(self.file_path, sep=';')
            result = df[df['ID'] == int(id_val)]
            if result.empty:
                return "Error", "No se encontraron datos para el ID proporcionado"
            return "Success", result
        except Exception as e:
            return "Error", f"No se pudo obtener los datos: {e}"

    def get_data(self):
        return self.data