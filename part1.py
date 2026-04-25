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