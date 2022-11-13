#!/usr/bin/env python

import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random

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

str = "Bicep"

colors = list(mcolors.CSS4_COLORS)
for key in df2.keys():
    if str in key:
        df2[key].astype(float).ffill().plot(kind='line', lw=2, marker='.', markersize=10)

plt.title("Bicep exercises")

plt.legend(loc='upper left')

plt.show()
#print(df.head())
