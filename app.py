from flask import Flask, request, render_template, jsonify
import pandas as pd
import requests
from io import StringIO

app = Flask(__name__)

# Función para cargar un archivo CSV desde Google Drive
def load_csv_from_google_drive(file_id):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)
    return df

# Cargar las tablas
file_id_main = "1FgRL2aVx6jRsbLX7CGPRLytcb2aWlkcB"  # Tabla principal
file_id_mineral1 = "1fd4uGPjzAsLSh0a8cS91rhTubbO8_YwS"  # Tabla del mineral 1
file_id_mineral2 = "1qFdQrVTYHFF4C2Fd5lI4cjBH2imf6ehO"  # Tabla del mineral 2

df_main = load_csv_from_google_drive(file_id_main)
df_mineral1 = load_csv_from_google_drive(file_id_mineral1)
df_mineral2 = load_csv_from_google_drive(file_id_mineral2)

# Diccionario para mapear nombres de minerales a sus tablas
mineral_tables = {
    "Epidota": df_mineral1,
    "Pirita": df_mineral2,
}

# URL de la imagen
#imagen_url = "https://raw.githubusercontent.com/ginfo-iige/borrar/refs/heads/main/1.jpg"

# Agregar botones a la tabla principal
df_main['Acciones'] = df_main['Nombre '].apply(
    lambda x: f'<button class="load-table-btn" data-mineral="{x}">Ver Tabla</button>'
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_field = request.form['search_field']
        search_value = request.form['search_value']
        results = df_main[df_main[search_field].astype(str).str.contains(search_value, case=False, na=False)]
        return render_template('index.html', tables=[results.to_html(classes='data', escape=False)], titles=df_main.columns.values)
    return render_template('index.html', tables=[df_main.to_html(classes='data', escape=False)], titles=df_main.columns.values)

# Ruta para cargar la tabla asociada
@app.route('/load_table', methods=['POST'])
def load_table():
    mineral_name = request.json['mineral_name']
    
    if mineral_name in mineral_tables:
        df = mineral_tables[mineral_name]
        # Renombrar las columnas
        df.columns = ['Variable', 'Detalle']
        
        # Reordenar las columnas (asegurarse de que "Variable" esté primero)
        df = df[['Variable', 'Detalle']]
        
        # Extraer el enlace de la imagen desde la posición [7, 1]
        imagen_url = df.iloc[7, 1]  # Fila 7, columna 1
        # Devolver la tabla y la URL de la imagen
        return jsonify({
            "table": df.to_dict('records'),
            "imagen_url": imagen_url
        })
    return jsonify({"error": "Mineral no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
