
import cmath


def crear_complejo(real, imaginario):
    """Construye un número complejo a partir de sus componentes."""
    return complex(real, imaginario)


def sumar(z1, z2):
    return z1 + z2


def restar(z1, z2):
    return z1 - z2


def multiplicar(z1, z2):
    return z1 * z2


def dividir(z1, z2):
    if z2 == 0:
        raise ValueError("No se puede dividir entre cero.")
    return z1 / z2


def potencia(z, exponente):
    return z ** exponente


def obtener_conjugado(z):
    return z.conjugate()


def obtener_modulo(z):
    return abs(z)


def obtener_argumento(z):
    return cmath.phase(z)


def obtener_forma_polar(z):
    modulo = abs(z)
    argumento = cmath.phase(z)
    return modulo, argumento


def obtener_forma_exponencial(z):
    modulo, argumento = obtener_forma_polar(z)
    return f"{modulo:.4f} * e^(i * {argumento:.4f})"


def obtener_partes(z):
    return z.real, z.imag


def convertir_a_texto(z):
    """Presenta el número complejo en forma binómica."""
    real = z.real
    imaginario = z.imag

    if abs(imaginario) < 1e-12:
        return f"{real:g}"

    if abs(real) < 1e-12:
        return f"{imaginario:g}i"

    signo = "+" if imaginario >= 0 else "-"
    return f"{real:g} {signo} {abs(imaginario):g}i"


def obtener_raices(z, n):
    """Calcula las n raíces complejas de z."""

    if not isinstance(n, int) or n < 1:
        raise ValueError("El índice debe ser un entero positivo.")

    if z == 0:
        return [0j] * n

    modulo = abs(z)
    argumento = cmath.phase(z)

    raices = []

    for k in range(n):
        angulo = (argumento + 2 * cmath.pi * k) / n
        modulo_raiz = modulo ** (1 / n)

        raiz = modulo_raiz * (
            cmath.cos(angulo) + 1j * cmath.sin(angulo)
        )

        raices.append(raiz)

    return raices
