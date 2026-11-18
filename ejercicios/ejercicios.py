import numpy as np


EJERCICIOS = {

    "Ejercicio 1 - Fourier tradicional": {
        "tipo": "tradicional",
        "descripcion": "Función definida por partes: 0 y 1.",
        "a": -np.pi,
        "b": np.pi,
        "funcion": lambda x: np.where(x < 0, 0, 1)
    },

    "Ejercicio 4 - Fourier tradicional": {
        "tipo": "tradicional",
        "descripcion": "Función lineal f(x) = x + pi.",
        "a": -np.pi,
        "b": np.pi,
        "funcion": lambda x: x + np.pi
    },

    "Ejercicio 2 - Serie de cosenos": {
        "tipo": "coseno",
        "descripcion": "Función cuadrática f(x) = x².",
        "a": -1,
        "b": 1,
        "funcion": lambda x: x**2
    },

    "Ejercicio 4 - Serie de senos": {
        "tipo": "seno",
        "descripcion": "Función cúbica f(x) = x³.",
        "a": -np.pi,
        "b": np.pi,
        "funcion": lambda x: x**3
    },

    "Ejercicio 1 - Fourier compleja": {
        "tipo": "compleja",
        "descripcion": "Función definida por partes: -1 y 1.",
        "a": -2,
        "b": 2,
        "funcion": lambda x: np.where(x < 0, -1, 1)
    },

    "Ejercicio 6 - Fourier compleja": {
        "tipo": "compleja",
        "descripcion": "Función exponencial f(x) = e^(-|x|).",
        "a": -1,
        "b": 1,
        "funcion": lambda x: np.exp(-np.abs(x))
    }
}


def obtener_ejercicios():
    """
    Devuelve el catálogo completo de ejercicios.
    """
    return EJERCICIOS


def obtener_ejercicio(nombre):
    """
    Devuelve un ejercicio específico por su nombre.
    """
    if nombre not in EJERCICIOS:
        raise ValueError("El ejercicio seleccionado no existe.")

    return EJERCICIOS[nombre]