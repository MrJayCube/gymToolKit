#!/usr/bin/env python

import os
import io
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from flask import Flask, render_template, Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)

# load data using Python JSON module
with open('diario.json','r') as f:
    data = json.loads(f.read())
# Flatten data
df = pd.json_normalize(data)
df = df.transpose()
split = pd.DataFrame(df[0].to_list())
jsonver = json.loads(df.to_json())
jsonver = jsonver["0"]
ejercicios = []
entrenamiento = {}
entreamientoFinal = {}
dias = []

num_dia = 0

@app.route("/")
def index():
    for dia in jsonver:
        for ejercicio in range(len(jsonver[dia])):
            par = jsonver[dia][ejercicio]
            for elemento in par:
                if elemento not in ejercicios:
                    ejercicios.append(elemento)

    print(ejercicios)

    for dia in jsonver:
        dias.append(dia)
        temp = ejercicios.copy()
        entrenamiento = {}
        for ejercicio in range(len(jsonver[dia])):
            par = jsonver[dia][ejercicio]
            found = False
            for elemento in par:
                if elemento not in entrenamiento:
                    entrenamiento[elemento] = par[elemento].split('kg')[0]
                if elemento in temp:
                    temp.remove(elemento)
        for elemento in temp:
            if elemento not in entrenamiento:
                entrenamiento[elemento] = "0"

        entreamientoFinal[dia] = entrenamiento

    print(entreamientoFinal)
    df2 = pd.DataFrame(entreamientoFinal).transpose()
    print(df2.head())

    for key in df2.keys():
        df2[key] = df2[key].str.replace(' ', '')
        df2[key] = df2[key].str.replace(',', '.')

    df2.replace("0", np.nan, inplace=True)
    df2.columns = ejercicios

    str = "row"

    colors = list(mcolors.CSS4_COLORS)

    filedata = "{{image}}"

    for key in df2.keys():
        if str not in key:
            df2.pop(key)

    df2.astype(float).ffill().plot(subplots=True, layout=(4, -1), figsize=(15, 30), sharex=False)

    #plt.title("Bicep exercises")

    plt.legend(loc='upper left')

    #plt.show()
    #print(df.head())
    print(os.getcwd())
    name = "prueba"
    url = f'static/images/plot-{name}.png'
    plt.savefig(url)
    plt.cla()
    plt.clf()
    filedata = filedata.replace('{{image}}', f'<p>plot-{name}.png</p><img src={url} '
                                                 f'alt="Chart" height="2160" width="3840">' + "{{image}}")

    return filedata

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081, debug=True)
