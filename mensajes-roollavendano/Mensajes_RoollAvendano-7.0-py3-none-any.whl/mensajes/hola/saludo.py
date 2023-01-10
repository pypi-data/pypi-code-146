import numpy as np  

def saludar():
    print("Hola, te saludo desde saludos.saludar()")

def prueba():
    print("esto es una prueba nueva de la nueva version 7.0")

class Saludo:
    def __init__(self):
        print("Hola, te saludo desde Saludo.__init__()")

def generar_array(numeros):
    return np.arange(numeros)

if __name__ == '__main__':
    print(generar_array(5))
    saludar()