import numpy as np
from scipy.integrate import quad


def calcular_serie_compleja(funcion, a, b, N):
    """
    Calcula los coeficientes complejos c_n de Fourier.

    La función se representa mediante:
    f(x) = sum(c_n * exp(i*2*pi*n*(x-a)/L))
    """

    if b <= a:
        raise ValueError("El límite superior debe ser mayor que el inferior.")

    if N < 0:
        raise ValueError("El número de armónicos no puede ser negativo.")

    L = b - a

    coeficientes = {}

    for n in range(-N, N + 1):

        def parte_real(x):
            valor = funcion(x) * np.exp(
                -1j * 2 * np.pi * n * (x - a) / L
            )
            return float(np.real(valor))

        def parte_imaginaria(x):
            valor = funcion(x) * np.exp(
                -1j * 2 * np.pi * n * (x - a) / L
            )
            return float(np.imag(valor))

        real, _ = quad(parte_real, a, b)
        imaginaria, _ = quad(parte_imaginaria, a, b)

        coeficientes[n] = (real + 1j * imaginaria) / L

    return {
        "cn": coeficientes,
        "N": N,
        "a": a,
        "b": b,
        "L": L
    }


def evaluar_serie_compleja(x, coeficientes, N=None):
    """
    Evalúa la serie compleja de Fourier en uno o varios puntos.
    """

    if N is None:
        N = coeficientes["N"]

    N = min(N, coeficientes["N"])

    a = coeficientes["a"]
    L = coeficientes["L"]

    x = np.asarray(x, dtype=float)

    resultado = np.zeros_like(x, dtype=complex)

    for n in range(-N, N + 1):

        angulo = 2 * np.pi * n * (x - a) / L

        resultado += (
            coeficientes["cn"][n] * np.exp(1j * angulo)
        )

    resultado = np.real_if_close(resultado)

    if resultado.ndim == 0:
        return float(np.real(resultado))

    return np.real(resultado)