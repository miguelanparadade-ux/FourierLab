import numpy as np
from scipy.integrate import quad


def calcular_coeficientes(funcion, a, b, N):
    """
    Calcula los coeficientes de la serie de Fourier tradicional.

    funcion: función matemática que se desea aproximar.
    a: límite inferior del intervalo.
    b: límite superior del intervalo.
    N: número de armónicos.
    """

    if b <= a:
        raise ValueError("El límite superior debe ser mayor que el inferior.")

    if N < 0:
        raise ValueError("El número de armónicos no puede ser negativo.")

    L = b - a

    # Cálculo del coeficiente a0
    integral_a0, _ = quad(lambda x: float(funcion(x)), a, b)
    a0 = (2 / L) * integral_a0

    # Listas para almacenar los coeficientes
    an = []
    bn = []

    # Cálculo de los coeficientes an y bn
    for n in range(1, N + 1):

        integral_an, _ = quad(
            lambda x: float(
                funcion(x) * np.cos(2 * np.pi * n * (x - a) / L)
            ),
            a,
            b
        )

        integral_bn, _ = quad(
            lambda x: float(
                funcion(x) * np.sin(2 * np.pi * n * (x - a) / L)
            ),
            a,
            b
        )

        an.append((2 / L) * integral_an)
        bn.append((2 / L) * integral_bn)

    return {
        "a0": a0,
        "an": an,
        "bn": bn,
        "N": N,
        "a": a,
        "b": b,
        "L": L
    }


def evaluar_serie_fourier(x, coeficientes, N=None):
    """
    Evalúa la aproximación de Fourier en uno o varios puntos x.
    """

    if N is None:
        N = coeficientes["N"]

    N = min(N, coeficientes["N"])

    a = coeficientes["a"]
    L = coeficientes["L"]

    x = np.asarray(x, dtype=float)

    # Comenzamos con el término constante
    resultado = np.full_like(x, coeficientes["a0"] / 2, dtype=float)

    # Sumamos los términos de cada armónico
    for n in range(1, N + 1):

        angulo = 2 * np.pi * n * (x - a) / L

        resultado += (
            coeficientes["an"][n - 1] * np.cos(angulo)
            + coeficientes["bn"][n - 1] * np.sin(angulo)
        )

    if resultado.ndim == 0:
        return float(resultado)

    return resultado