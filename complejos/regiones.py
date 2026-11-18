
import numpy as np


def calcular_modulo_relativo(x, y, centro_real=0, centro_imaginario=0):
    """
    Calcula la distancia entre un punto del plano
    complejo y un centro determinado.
    """
    return np.sqrt(
        (x - centro_real)**2 +
        (y - centro_imaginario)**2
    )


def pertenece_a_corona(
    x, y,
    radio_interno,
    radio_externo,
    centro_real=0,
    centro_imaginario=0
):
    """Comprueba si un punto pertenece a una corona circular."""

    if radio_interno < 0 or radio_externo < radio_interno:
        raise ValueError("Los radios no son válidos.")

    distancia = calcular_modulo_relativo(
        x, y, centro_real, centro_imaginario
    )

    return (distancia >= radio_interno) & (
        distancia <= radio_externo
    )


def pertenece_a_semiplano_imaginario(y, limite, relacion=">="):
    """Comprueba si un punto cumple una desigualdad imaginaria."""

    if relacion == ">=":
        return y >= limite
    elif relacion == "<=":
        return y <= limite
    elif relacion == ">":
        return y > limite
    elif relacion == "<":
        return y < limite

    raise ValueError("Relación no válida.")


def generar_malla(limite=5, puntos=300):
    """Genera las coordenadas para representar el plano complejo."""

    reales = np.linspace(-limite, limite, puntos)
    imaginarios = np.linspace(-limite, limite, puntos)

    X, Y = np.meshgrid(reales, imaginarios)

    return X, Y


def evaluar_region_corona_semiplano(
    radio_interno=1,
    radio_externo=3,
    centro_real=1,
    centro_imaginario=1,
    limite_imaginario=1,
    relacion=">=",
    limite=5,
    puntos=300
):
    """
    Evalúa la intersección de una corona circular
    con un semiplano del plano complejo.
    """

    X, Y = generar_malla(limite, puntos)

    corona = pertenece_a_corona(
        X, Y,
        radio_interno,
        radio_externo,
        centro_real,
        centro_imaginario
    )

    semiplano = pertenece_a_semiplano_imaginario(
        Y, limite_imaginario, relacion
    )

    region = corona & semiplano

    return X, Y, region
