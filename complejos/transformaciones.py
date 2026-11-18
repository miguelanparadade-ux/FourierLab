
import numpy as np


def transformar_puntos(z, exponente=2):
    """
    Aplica la transformación w = z^n
    a una colección de puntos complejos.
    """
    z = np.asarray(z, dtype=complex)
    return z ** exponente


def transformar_recta_imaginaria(valor, inicio=-5, fin=5, puntos=300):
    """
    Construye la recta z = x + valor*i
    y aplica la transformación w = z^2.
    """

    x = np.linspace(inicio, fin, puntos)

    z = x + valor * 1j
    w = z ** 2

    return z, w


def obtener_coordenadas(z, w):
    """Separa las partes reales e imaginarias."""

    return {
        "z_real": np.real(z),
        "z_imaginario": np.imag(z),
        "w_real": np.real(w),
        "w_imaginario": np.imag(w)
    }


def obtener_ecuacion_parabola(valor):
    """
    Para w = z^2 y z = x + ai:
    v² = 4a²(u + a²).
    """

    return {
        "coeficiente": 4 * valor**2,
        "desplazamiento": valor**2,
        "ecuacion": (
            f"v² = {4 * valor**2}(u + {valor**2})"
        )
    }


def calcular_imagen_recta(valor, cantidad=10):
    """Genera puntos de la recta y sus imágenes."""

    x = np.linspace(-5, 5, cantidad)

    z = x + valor * 1j
    w = z ** 2

    return z, w
