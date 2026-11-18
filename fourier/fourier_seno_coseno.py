
import numpy as np
from scipy.integrate import quad


def calcular_serie_coseno(funcion, a, b, N):
    """
    Calcula una serie de cosenos usando una base centrada
    en el intervalo [a, b].
    """

    if b <= a:
        raise ValueError("El límite superior debe ser mayor que el inferior.")

    if N < 0:
        raise ValueError("El número de armónicos no puede ser negativo.")

    L = b - a
    centro = (a + b) / 2

    integral_a0, _ = quad(
        lambda x: float(funcion(x)), a, b
    )

    a0 = (2 / L) * integral_a0
    an = []

    for n in range(1, N + 1):
        integral, _ = quad(
            lambda x: float(
                funcion(x) * np.cos(2 * np.pi * n * (x - centro) / L)
            ),
            a,
            b
        )

        an.append((2 / L) * integral)

    return {
        "a0": a0,
        "an": an,
        "N": N,
        "a": a,
        "b": b,
        "L": L,
        "centro": centro
    }


def evaluar_serie_coseno(x, coeficientes, N=None):
    """Evalúa la aproximación mediante cosenos."""

    if N is None:
        N = coeficientes["N"]

    N = min(N, coeficientes["N"])

    L = coeficientes["L"]
    centro = coeficientes["centro"]

    x = np.asarray(x, dtype=float)

    resultado = np.full_like(
        x, coeficientes["a0"] / 2, dtype=float
    )

    for n in range(1, N + 1):
        angulo = 2 * np.pi * n * (x - centro) / L

        resultado += (
            coeficientes["an"][n - 1] * np.cos(angulo)
        )

    if resultado.ndim == 0:
        return float(resultado)

    return resultado


def calcular_serie_seno(funcion, a, b, N):
    """
    Calcula una serie de senos usando una base centrada
    en el intervalo [a, b].
    """

    if b <= a:
        raise ValueError("El límite superior debe ser mayor que el inferior.")

    if N < 0:
        raise ValueError("El número de armónicos no puede ser negativo.")

    L = b - a
    centro = (a + b) / 2
    print("ESTOY EJECUTANDO LA VERSION NUEVA DE SENOS")
    bn = []

    for n in range(1, N + 1):
        integral, _ = quad(
            lambda x: float(
                funcion(x) * np.sin(2 * np.pi * n * (x - centro) / L)
            ),
            a,
            b
        )

        bn.append((2 / L) * integral)

    return {
        "bn": bn,
        "N": N,
        "a": a,
        "b": b,
        "L": L,
        "centro": centro
    }


def evaluar_serie_seno(x, coeficientes, N=None):
    """Evalúa la aproximación mediante senos."""

    if N is None:
        N = coeficientes["N"]

    N = min(N, coeficientes["N"])

    L = coeficientes["L"]
    centro = coeficientes["centro"]

    x = np.asarray(x, dtype=float)

    resultado = np.zeros_like(x, dtype=float)

    for n in range(1, N + 1):
        angulo = 2 * np.pi * n * (x - centro) / L

        resultado += (
            coeficientes["bn"][n - 1] * np.sin(angulo)
        )

    if resultado.ndim == 0:
        return float(resultado)

    return resultado
