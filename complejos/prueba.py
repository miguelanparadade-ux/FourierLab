
from operaciones import *

z1 = crear_complejo(2, 2)
z2 = crear_complejo(1, -1)

print("Número z1:", convertir_a_texto(z1))
print("Número z2:", convertir_a_texto(z2))

print("\nSUMA:", convertir_a_texto(sumar(z1, z2)))
print("RESTA:", convertir_a_texto(restar(z1, z2)))
print("MULTIPLICACIÓN:", convertir_a_texto(multiplicar(z1, z2)))
print("DIVISIÓN:", convertir_a_texto(dividir(z1, z2)))

print("\nCONJUGADO DE z1:", convertir_a_texto(obtener_conjugado(z1)))
print("MÓDULO DE z1:", obtener_modulo(z1))
print("ARGUMENTO DE z1:", obtener_argumento(z1))
print("FORMA POLAR:", obtener_forma_polar(z1))
print("FORMA EXPONENCIAL:", obtener_forma_exponencial(z1))


print("\nRAÍCES CÚBICAS DE 8i:")

raices = obtener_raices(8j, 3)

for indice, raiz in enumerate(raices, start=1):
    print(
        f"Raíz {indice}: {convertir_a_texto(raiz)}"
    )
    print(
        f"Comprobación: {convertir_a_texto(raiz ** 3)}"
    )


from regiones import evaluar_region_corona_semiplano

print("\nPRUEBA DE REGIONES COMPLEJAS:")

X, Y, region = evaluar_region_corona_semiplano(
    radio_interno=1,
    radio_externo=3,
    centro_real=1,
    centro_imaginario=1,
    limite_imaginario=1,
    relacion=">="
)

print("Dimensiones de la región:", region.shape)
print("Cantidad de puntos dentro de la región:", region.sum())

puntos_prueba = [
    (1, 2),
    (2, 2),
    (1, 0),
    (5, 5)
]

for x, y in puntos_prueba:
    pertenece = (
        (x - 1)**2 + (y - 1)**2 >= 1
        and
        (x - 1)**2 + (y - 1)**2 <= 9
        and
        y >= 1
    )

    print(
        f"Punto ({x}, {y}): "
        f"{'Pertenece' if pertenece else 'No pertenece'}"
    )


from dominios import (
    z,
    analizar_funcion,
    obtener_dominio,
    evaluar_funcion,
    explicar_dominio
)

print("\nANÁLISIS DEL DOMINIO:")

resultado = analizar_funcion(
    numerador=z + 2,
    denominador=z**3 + 9*z
)

print("Función:", resultado["funcion"])
print("Puntos excluidos:", obtener_dominio(resultado))

print("\nPROCEDIMIENTO:")

for paso in explicar_dominio(resultado):
    print(paso)

print("\nEVALUACIÓN:")

print("f(1):", evaluar_funcion(resultado, 1))


from transformaciones import (
    transformar_recta_imaginaria,
    obtener_coordenadas,
    obtener_ecuacion_parabola
)

print("\nTRANSFORMACIONES COMPLEJAS:")

z, w = transformar_recta_imaginaria(valor=2)

coordenadas = obtener_coordenadas(z, w)

print("Primer punto original:", z[0])
print("Primer punto transformado:", w[0])

print("Ecuación de la parábola:")
print(obtener_ecuacion_parabola(2)["ecuacion"])

print("Cantidad de puntos transformados:", len(w))
