# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 15:53:30 2025

@author: jijonj
"""
from flask import Flask, request, render_template
import pandas as pd
import requests
from io import StringIO

app = Flask(__name__)

# URL del archivo CSV en Google Drive
url = "https://drive.google.com/uc?export=download&id=1FgRL2aVx6jRsbLX7CGPRLytcb2aWlkcB"

# Función para cargar el archivo CSV
def load_csv():
    response = requests.get(url)
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)
    return df

@app.route('/', methods=['GET', 'POST'])
def index():
    df = load_csv()
    if request.method == 'POST':
        search_field = request.form['search_field']
        search_value = request.form['search_value']
        results = df[df[search_field].astype(str).str.contains(search_value, case=False, na=False)]
        return render_template('index.html', tables=[results.to_html(classes='data')], titles=df.columns.values)
    return render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

if __name__ == '__main__':
    app.run(debug=True)
