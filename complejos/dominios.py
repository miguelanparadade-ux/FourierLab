
import sympy as sp

z = sp.symbols("z")


def analizar_funcion(numerador, denominador=1):
    """
    Analiza una función racional compleja:
    f(z) = numerador / denominador.
    """

    numerador = sp.sympify(numerador)
    denominador = sp.sympify(denominador)

    if denominador == 0:
        raise ValueError("El denominador no puede ser cero.")

    funcion = numerador / denominador

    restricciones = sp.solve(
        sp.Eq(denominador, 0),
        z
    )

    return {
        "funcion": funcion,
        "numerador": numerador,
        "denominador": denominador,
        "puntos_excluidos": restricciones
    }


def obtener_dominio(resultado):
    """Devuelve los puntos que deben excluirse del dominio."""

    excluidos = resultado["puntos_excluidos"]

    if not excluidos:
        return "La función no presenta restricciones por denominador."

    return excluidos


def evaluar_funcion(resultado, valor):
    """Evalúa la función en un número complejo."""

    puntos_excluidos = resultado["puntos_excluidos"]

    if any(sp.simplify(valor - punto) == 0 for punto in puntos_excluidos):
        raise ValueError("El punto pertenece a las exclusiones del dominio.")

    funcion = resultado["funcion"]

    return sp.simplify(funcion.subs(z, valor))


def explicar_dominio(resultado):
    """Genera una explicación básica del dominio."""

    excluidos = resultado["puntos_excluidos"]

    explicacion = [
        "1. Identificamos el denominador de la función.",
        "2. Igualamos el denominador a cero.",
        "3. Resolvemos la ecuación para encontrar los puntos excluidos."
    ]

    if excluidos:
        explicacion.append(
            f"4. Los puntos excluidos son: {excluidos}"
        )
    else:
        explicacion.append(
            "4. No se encontraron puntos excluidos."
        )

    return explicacion
