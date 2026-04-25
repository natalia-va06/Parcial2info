# Parcial2info
Este repositorio incluye los pasos tomados para desarrollar el código del sistema de exploración neuroambiental

import pandas as pd
import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np
import os

def validar_int(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except:
            print("Ingrese un número válido")

class ProcesadorSIATA:
    def __init__(self, ruta):
        try:
            data = sio.loadmat(ruta)
        except FileNotFoundError:
            print(" Error: No encontramos el archivo. Verifica que la ruta sea correcta.")

        self.df = pd.read_csv(ruta)
        self.nombre = os.path.basename(ruta)

        for col in self.df.columns:
            if "fecha" in col.lower() or "date" in col.lower():
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                self.df.set_index(col, inplace=True)
                break

    def mostrar_info(self):
        print(self.df.info())
        print(self.df.describe())

    def graficar(self):
        print("Columnas disponibles:")
        print(self.df.select_dtypes(include='number').columns)

        col = input("Elija columna: ")

        if col not in self.df.columns:
            print("Columna inválida")
            return

        fig, ax = plt.subplots(1, 3, figsize=(12,4))

        self.df[col].plot(ax=ax[0], title="Plot")
        self.df[col].plot(kind='box', ax=ax[1], title="Boxplot")
        self.df[col].plot(kind='hist', ax=ax[2], title="Hist")
        
        ax[0].set_xlabel("Tiempo")
        ax[0].set_ylabel("Valor")

        ax[1].set_ylabel("Valor")

        ax[2].set_xlabel("Valor")
        ax[2].set_ylabel("Frecuencia")

        plt.tight_layout()
        plt.savefig("siata_graficos.png")
        plt.show(block=False)
        plt.pause(3)
        plt.close()

    def operaciones(self):
        print(self.df.select_dtypes(include='number').columns)
        c1 = input("Columna 1: ")
        c2 = input("Columna 2: ")

        if c1 not in self.df.columns or c2 not in self.df.columns:
            print("Columnas inválidas")
            return

        self.df['apply'] = self.df[c1].apply(lambda x: x*2)
        self.df['map'] = self.df[c1].map(lambda x: x/2)
        self.df['suma'] = self.df[c1] + self.df[c2]

        print(self.df[[c1,c2,'apply','map','suma']].head())

    def remuestreo(self):
        print(self.df.select_dtypes(include='number').columns)
        col = input("Columna: ")

        if col not in self.df.columns:
            print("Columna inválida")
            return

        d = self.df[col].resample('D').mean()
        m = self.df[col].resample('M').mean()
        t = self.df[col].resample('Q').mean()

        plt.plot(d, label="Diario")
        plt.plot(m, label="Mensual")
        plt.plot(t, label="Trimestral")
        plt.legend()
        plt.savefig("remuestreo.png")
        plt.show()

class ProcesadorEEG:
    def __init__(self, ruta):
        self.ruta = ruta
        self.data = sio.loadmat(ruta)
        self.fs = 1000

    def mostrar_llaves(self):
        print(sio.whosmat(self.ruta))

    def obtener(self):
        for k in self.data:
            if not k.startswith('__'):
                print("Usando variable:", k)
                return self.data[k]

    def operar(self):
        m = self.obtener()
        print("Forma de la matriz:", m.shape)
        if m is None:
            print("No se encontró matriz válida")
            return

        if m.ndim == 3:
            m = m[:,:,0]

        c1 = validar_int("Canal 1: ")
        c2 = validar_int("Canal 2: ")
        c3 = validar_int("Canal 3: ")
        i = validar_int("Inicio: ")
        f = validar_int("Fin: ")
        
        if c1 >= m.shape[0] or c2 >= m.shape[0] or c3 >= m.shape[0]:
            print("Canal fuera de rango")
            return
        
        if i >= f:
            print("Rango inválido")
            return

        t = np.arange(i,f)/self.fs
        res = m[c1,i:f] + m[c2,i:f] + m[c3,i:f]

        fig, ax = plt.subplots(2,1)

        ax[0].plot(t, m[c1,i:f], label="c1")
        ax[0].plot(t, m[c2,i:f], label="c2")
        ax[0].plot(t, m[c3,i:f], label="c3")
        ax[0].legend()
        ax[0].set_xlabel("Tiempo (s)")
        ax[0].set_ylabel("Microvoltios (µV)")

        ax[1].plot(t, res)
        ax[1].set_xlabel("Tiempo (s)")
        ax[1].set_ylabel("Microvoltios (µV)")

        plt.savefig("eeg_suma.png")
        plt.show()

    def estadisticas(self):
        m = self.obtener()

        prom = np.mean(m, axis=2)
        std = np.std(m, axis=2)

        fig, ax = plt.subplots(2,1)
        t = np.arange(0,100)/self.fs

        ax[0].stem(t, prom[0,:100])
        ax[1].stem(t, std[0,:100])
        
        ax[0].set_xlabel("Muestras (tiempo)")
        ax[0].set_ylabel("Microvoltios (µV)")

        ax[1].set_xlabel("Muestras (tiempo)")
        ax[1].set_ylabel("Microvoltios (µV)")

        plt.savefig("eeg_stats.png")
        plt.show()
        
