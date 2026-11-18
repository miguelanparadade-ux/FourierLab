
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from complejos.interfaz import mostrar_interfaz_complejos

from ejercicios.ejercicios import obtener_ejercicios
from fourier.funciones import crear_funcion

from fourier.fourier_general import (
    calcular_coeficientes,
    evaluar_serie_fourier
)

from fourier.fourier_seno_coseno import (
    calcular_serie_coseno,
    evaluar_serie_coseno,
    calcular_serie_seno,
    evaluar_serie_seno
)

from fourier.fourier_compleja import (
    calcular_serie_compleja,
    evaluar_serie_compleja
)


# ==========================================
# FUNCION PARA EDITAR COEFICIENTES
# ==========================================

def evaluar_serie_manual(x, a, b, a0, an, bn):

    L = b - a
    x = np.asarray(x, dtype=float)

    resultado = np.full_like(x, a0 / 2, dtype=float)

    for n in range(1, len(an) + 1):

        angulo = 2 * np.pi * n * (x - a) / L

        resultado += (
            an[n - 1] * np.cos(angulo)
            + bn[n - 1] * np.sin(angulo)
        )

    return resultado


# ==========================================
# CONFIGURACION GENERAL
# ==========================================


st.set_page_config(
    page_title="FourierLab",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# MENU PRINCIPAL DE FOURIERLAB
# ==========================================

from complejos.interfaz import mostrar_interfaz_complejos

modulo = st.sidebar.selectbox(
    "Módulo de aprendizaje",
    ["Series de Fourier", "Números complejos"]
)

if modulo == "Números complejos":
    mostrar_interfaz_complejos()
    st.stop()


st.title("FourierLab")
st.subheader("Calculadora interactiva de series de Fourier")

st.markdown(
    """
    Calcula, modifica y visualiza series de Fourier.
    Puedes utilizar los ejercicios del taller o definir
    una función matemática personalizada.
    """
)


# ==========================================
# MENU LATERAL
# ==========================================

st.sidebar.title("Configuración")

modo = st.sidebar.selectbox(
    "Modo de trabajo",
    ["Ejercicios del taller", "Función personalizada"]
)

ejercicios = obtener_ejercicios()
funcion = None
nombre = "Personalizada"



# ==========================================
# EJERCICIOS DEL TALLER
# ==========================================

if modo == "Ejercicios del taller":

    nombre = st.sidebar.selectbox(
        "Selecciona un ejercicio",
        list(ejercicios.keys())
    )

    ejercicio = ejercicios[nombre]

    funcion = ejercicio["funcion"]
    tipo = ejercicio["tipo"]

    a = float(ejercicio["a"])
    b = float(ejercicio["b"])

    st.info(f"Ejercicio seleccionado: {nombre}")
    st.write(ejercicio["descripcion"])

    a = st.sidebar.number_input(
        "Límite inferior",
        value=a,
        format="%.4f",
        key="limite_inferior_ejercicio"
    )

    b = st.sidebar.number_input(
        "Límite superior",
        value=b,
        format="%.4f",
        key="limite_superior_ejercicio"
    )


# ==========================================
# FUNCION PERSONALIZADA
# ==========================================

else:

    st.sidebar.subheader("Define tu función")

    expresion = st.sidebar.text_input(
        "Escribe una función de x",
        value="x**2"
    )

    tipo = st.sidebar.selectbox(
        "Tipo de serie",
        ["tradicional", "seno", "coseno", "compleja"]
    )

    a = st.sidebar.number_input(
        "Límite inferior",
        value=-3.1416,
        format="%.4f",
        key="limite_inferior_personalizado"
    )

    b = st.sidebar.number_input(
        "Límite superior",
        value=3.1416,
        format="%.4f",
        key="limite_superior_personalizado"
    )

    try:
        funcion = crear_funcion(expresion)
        st.sidebar.success("Función interpretada correctamente.")

    except Exception as error:
        st.sidebar.error(f"Error en la función: {error}")
        funcion = None

    nombre = "Personalizada: " + expresion


# ==========================================
# CONFIGURACION DE ARMONICOS
# ==========================================

st.sidebar.divider()

N = st.sidebar.slider(
    "Número de armónicos",
    min_value=1,
    max_value=50,
    value=10
)


# ==========================================
# MODO DE CALCULO
# ==========================================

modo_coeficientes = "Automático"

if tipo == "tradicional":

    modo_coeficientes = st.sidebar.radio(
        "Método de trabajo",
        [
            "Automático",
            "Manual: editar coeficientes"
        ]
    )

mostrar_original = st.sidebar.checkbox(
    "Mostrar función original",
    value=True
)


# ==========================================
# CONFIGURACION ACTUAL
# ==========================================

st.divider()

st.header("Configuración actual")

col1, col2, col3 = st.columns(3)

col1.metric("Tipo de serie", tipo.capitalize())
col2.metric("Límite inferior", f"{a:.4f}")
col3.metric("Límite superior", f"{b:.4f}")

st.write(f"**Número de armónicos:** {N}")
st.write(f"**Método:** {modo_coeficientes}")


# ==========================================
# CALCULOS
# ==========================================

st.divider()

st.header("Resultados matemáticos")

if funcion is None:

    st.warning("Corrige la función matemática para continuar.")

elif b <= a:

    st.error("El límite superior debe ser mayor que el inferior.")

else:

    try:

        x = np.linspace(a, b, 1200)

        valores_originales = np.asarray(
            funcion(x),
            dtype=float
        )

        figura = go.Figure()

        if mostrar_original:

            figura.add_trace(
                go.Scatter(
                    x=x,
                    y=valores_originales,
                    mode="lines",
                    name="Función original",
                    line=dict(width=3)
                )
            )

        # ==================================
        # FOURIER TRADICIONAL
        # ==================================

        if tipo == "tradicional":

            # Primero calculamos los coeficientes automáticos.
            coeficientes_auto = calcular_coeficientes(
                funcion, a, b, N
            )

            if modo_coeficientes == "Automático":

                coeficientes = coeficientes_auto

                aproximacion = evaluar_serie_fourier(
                    x, coeficientes
                )

                st.subheader("Coeficientes calculados automáticamente")

            else:

                st.subheader("Editor manual de coeficientes")

                st.info(
                    "Modifica los valores de a₀, an y bn. "
                    "La gráfica cambiará automáticamente."
                )

                st.latex(
                    r"S_N(x)=\frac{a_0}{2}+"
                    r"\sum_{n=1}^{N}"
                    r"\left[a_n\cos\left(\frac{2\pi n(x-a)}{L}\right)"
                    r"+b_n\sin\left(\frac{2\pi n(x-a)}{L}\right)\right]"
                )

                st.write(
                    "Los valores iniciales corresponden al cálculo "
                    "automático de la función seleccionada."
                )

                identificador = f"{nombre}_{a}_{b}"

                a0_manual = st.number_input(
                    "Coeficiente a₀",
                    value=float(coeficientes_auto["a0"]),
                    format="%.6f",
                    key=f"a0_{identificador}"
                )

                st.markdown("### Coeficientes por armónico")

                an_manual = []
                bn_manual = []

                for n in range(1, N + 1):

                    col_n, col_an, col_bn = st.columns(3)

                    col_n.write(f"**Armónico {n}**")

                    valor_an = col_an.number_input(
                        f"a{n}",
                        value=float(coeficientes_auto["an"][n - 1]),
                        format="%.6f",
                        key=f"an_{identificador}_{n}"
                    )

                    valor_bn = col_bn.number_input(
                        f"b{n}",
                        value=float(coeficientes_auto["bn"][n - 1]),
                        format="%.6f",
                        key=f"bn_{identificador}_{n}"
                    )

                    an_manual.append(valor_an)
                    bn_manual.append(valor_bn)

                aproximacion = evaluar_serie_manual(
                    x,
                    a,
                    b,
                    a0_manual,
                    an_manual,
                    bn_manual
                )

                coeficientes = {
                    "a0": a0_manual,
                    "an": an_manual,
                    "bn": bn_manual,
                    "N": N,
                    "a": a,
                    "b": b,
                    "L": b - a
                }

                st.success(
                    "Coeficientes manuales aplicados a la gráfica."
                )

            figura.add_trace(
                go.Scatter(
                    x=x,
                    y=aproximacion,
                    mode="lines",
                    name=f"Serie de Fourier N={N}",
                    line=dict(width=3, dash="dash")
                )
            )

            st.markdown("### Tabla de coeficientes")

            st.write(f"**a₀ = {coeficientes['a0']:.8f}**")

            filas = []

            for i in range(N):

                filas.append({
                    "Armónico": i + 1,
                    "Coeficiente an": coeficientes["an"][i],
                    "Coeficiente bn": coeficientes["bn"][i]
                })

            st.dataframe(
                filas,
                use_container_width=True
            )

        # ==================================
        # SERIE DE COSENOS
        # ==================================

        elif tipo == "coseno":

            coeficientes = calcular_serie_coseno(
                funcion, a, b, N
            )

            aproximacion = evaluar_serie_coseno(
                x, coeficientes
            )

            figura.add_trace(
                go.Scatter(
                    x=x,
                    y=aproximacion,
                    mode="lines",
                    name=f"Serie de cosenos N={N}",
                    line=dict(width=3, dash="dash")
                )
            )

            st.subheader("Coeficientes de cosenos")
            st.write(f"a₀ = {coeficientes['a0']:.8f}")

            st.dataframe(
                [
                    {
                        "Armónico": i + 1,
                        "Coeficiente an": valor
                    }
                    for i, valor in enumerate(coeficientes["an"])
                ],
                use_container_width=True
            )

        # ==================================
        # SERIE DE SENOS
        # ==================================

        elif tipo == "seno":

            coeficientes = calcular_serie_seno(
                funcion, a, b, N
            )

            aproximacion = evaluar_serie_seno(
                x, coeficientes
            )

            figura.add_trace(
                go.Scatter(
                    x=x,
                    y=aproximacion,
                    mode="lines",
                    name=f"Serie de senos N={N}",
                    line=dict(width=3, dash="dash")
                )
            )

            st.subheader("Coeficientes de senos")

            st.dataframe(
                [
                    {
                        "Armónico": i + 1,
                        "Coeficiente bn": valor
                    }
                    for i, valor in enumerate(coeficientes["bn"])
                ],
                use_container_width=True
            )

        # ==================================
        # SERIE COMPLEJA
        # ==================================

        elif tipo == "compleja":

            coeficientes = calcular_serie_compleja(
                funcion, a, b, N
            )

            aproximacion = evaluar_serie_compleja(
                x, coeficientes
            )

            figura.add_trace(
                go.Scatter(
                    x=x,
                    y=aproximacion,
                    mode="lines",
                    name=f"Serie compleja N={N}",
                    line=dict(width=3, dash="dash")
                )
            )

            st.subheader("Coeficientes complejos")

            st.dataframe(
                [
                    {
                        "Armónico": n,
                        "Coeficiente cn": str(valor)
                    }
                    for n, valor in coeficientes["cn"].items()
                ],
                use_container_width=True
            )

        # ==================================
        # GRAFICA
        # ==================================

        figura.update_layout(
            title="Visualización interactiva de Fourier",
            xaxis_title="x",
            yaxis_title="f(x)",
            template="plotly_white",
            height=650,
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="left",
                x=0
            )
        )

        figura.update_xaxes(showgrid=True)
        figura.update_yaxes(showgrid=True)

        st.plotly_chart(
            figura,
            use_container_width=True
        )

        # ==================================
        # ANALISIS
        # ==================================

        st.divider()

        st.subheader("Análisis de la aproximación")

        st.write(
            f"Se utilizaron {N} armónicos en el intervalo "
            f"[{a:.4f}, {b:.4f}]."
        )

        if tipo == "tradicional" and modo_coeficientes.startswith("Manual"):

            st.write(
                "La gráfica representa la serie construida con "
                "los coeficientes que se encuentran actualmente "
                "en el editor manual."
            )

        else:

            st.write(
                "La gráfica representa la aproximación obtenida "
                "mediante los coeficientes calculados automáticamente."
            )

        st.write(
            "En funciones con discontinuidades puede aparecer "
            "el fenómeno de Gibbs."
        )

    except Exception as error:

        st.error(f"Error durante el cálculo: {error}")
