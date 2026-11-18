
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sympy as sp

from complejos.operaciones import (
    crear_complejo,
    sumar,
    restar,
    multiplicar,
    dividir,
    potencia,
    obtener_conjugado,
    obtener_modulo,
    obtener_argumento,
    convertir_a_texto,
    obtener_raices
)

from complejos.regiones import (
    calcular_modulo_relativo,
    pertenece_a_corona,
    pertenece_a_semiplano_imaginario,
    generar_malla,
    evaluar_region_corona_semiplano
)
from complejos.dominios import (
    z,
    analizar_funcion,
    obtener_dominio,
    explicar_dominio,
    evaluar_funcion
)

from complejos.transformaciones import (
    transformar_recta_imaginaria,
    obtener_ecuacion_parabola
)


def mostrar_interfaz_complejos():

    st.title("Números complejos")
    st.caption(
        "Aprende, calcula y visualiza los conceptos "
        "fundamentales de los números complejos."
    )

    seccion = st.sidebar.selectbox(
        "Contenido de números complejos",
        [
            "Introducción y teoría",
            "Operaciones",
            "Raíces complejas",
            "Regiones del plano",
            "Dominios de funciones",
            "Transformaciones"
        ]
    )

    # =====================================
    # INTRODUCCIÓN Y TEORÍA
    # =====================================

    if seccion == "Introducción y teoría":

        st.header("¿Qué son los números complejos?")

        st.write(
            "Los números complejos amplían los números reales "
            "y permiten resolver ecuaciones que no tienen "
            "solución dentro de los números reales."
        )

        st.latex(r"z=a+bi")

        st.write(
            "Donde a es la parte real, b es la parte imaginaria "
            "e i es la unidad imaginaria."
        )

        st.latex(r"i^2=-1")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Ejemplo")

            st.latex(r"z=3+4i")

            st.write("Parte real: 3")
            st.write("Parte imaginaria: 4")

        with col2:
            st.subheader("Conceptos importantes")

            st.latex(r"\overline{z}=a-bi")
            st.write("Conjugado")

            st.latex(r"|z|=\sqrt{a^2+b^2}")
            st.write("Módulo")

            st.latex(r"\arg(z)=\theta")
            st.write("Argumento")

        st.divider()

        st.subheader("Representación en el plano complejo")

        real = st.number_input(
            "Parte real",
            value=3.0,
            key="teoria_real"
        )

        imaginario = st.number_input(
            "Parte imaginaria",
            value=4.0,
            key="teoria_imaginario"
        )

        figura = go.Figure()

        figura.add_trace(
            go.Scatter(
                x=[0, real],
                y=[0, imaginario],
                mode="lines+markers",
                name="Número complejo"
            )
        )

        figura.add_trace(
            go.Scatter(
                x=[real],
                y=[imaginario],
                mode="markers+text",
                text=[f"{real}+{imaginario}i"],
                textposition="top right",
                name="z"
            )
        )

        figura.update_layout(
            title="Plano complejo",
            xaxis_title="Parte real",
            yaxis_title="Parte imaginaria",
            template="plotly_white",
            height=500
        )

        figura.update_yaxes(scaleanchor="x", scaleratio=1)

        st.plotly_chart(figura, use_container_width=True)

        numero = crear_complejo(real, imaginario)

        st.info(
            f"Número representado: {convertir_a_texto(numero)}"
        )

    # =====================================
    # OPERACIONES
    # =====================================

    elif seccion == "Operaciones":

        st.header("Calculadora de números complejos")

        st.write(
            "Introduce las partes reales e imaginarias "
            "de dos números complejos."
        )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Primer número")

            real1 = st.number_input(
                "Parte real de z₁",
                value=2.0
            )

            imag1 = st.number_input(
                "Parte imaginaria de z₁",
                value=2.0
            )

        with col2:
            st.subheader("Segundo número")

            real2 = st.number_input(
                "Parte real de z₂",
                value=1.0
            )

            imag2 = st.number_input(
                "Parte imaginaria de z₂",
                value=-1.0
            )

        z1 = crear_complejo(real1, imag1)
        z2 = crear_complejo(real2, imag2)

        st.divider()

        st.subheader("Resultados")

        resultados = [
            ("Suma", sumar(z1, z2)),
            ("Resta", restar(z1, z2)),
            ("Multiplicación", multiplicar(z1, z2))
        ]

        for nombre, resultado in resultados:
            st.write(
                f"**{nombre}:** {convertir_a_texto(resultado)}"
            )

        try:
            resultado_division = dividir(z1, z2)

            st.write(
                f"**División:** "
                f"{convertir_a_texto(resultado_division)}"
            )

        except ValueError as error:
            st.warning(str(error))

        st.divider()

        st.subheader("Propiedades de z₁")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Módulo",
            f"{obtener_modulo(z1):.4f}"
        )

        col2.metric(
            "Argumento (rad)",
            f"{obtener_argumento(z1):.4f}"
        )

        col3.metric(
            "Conjugado",
            convertir_a_texto(obtener_conjugado(z1))
        )

        exponente = st.number_input(
            "Exponente para z₁",
            min_value=0,
            max_value=20,
            value=2,
            step=1
        )

        st.write(
            "**Potencia:**",
            convertir_a_texto(potencia(z1, int(exponente)))
        )

   
   
  
    # =====================================
    # RAÍCES COMPLEJAS
    # =====================================

    elif seccion == "Raíces complejas":

        st.header("Calculadora interactiva de raíces n-ésimas")

        st.write(
            "Modifica el número complejo y el índice de la raíz. "
            "La aplicación calculará las raíces, explicará sus "
            "propiedades y actualizará la representación gráfica."
        )

        st.latex(
            r"w_k=\sqrt[n]{|z|}\left["
            r"\cos\left(\frac{\theta+2k\pi}{n}\right)"
            r"+i\sin\left(\frac{\theta+2k\pi}{n}\right)"
            r"\right]"
        )

        st.divider()

        # ENTRADA DE DATOS
        st.subheader("1. Configura el número complejo")

        col1, col2, col3 = st.columns(3)

        with col1:
            real = st.number_input(
                "Parte real",
                value=0.0,
                step=1.0,
                key="raiz_real"
            )

        with col2:
            imaginario = st.number_input(
                "Parte imaginaria",
                value=8.0,
                step=1.0,
                key="raiz_imag"
            )

        with col3:
            indice = st.number_input(
                "Índice de la raíz",
                min_value=1,
                max_value=20,
                value=3,
                step=1,
                key="raiz_indice"
            )

        numero = crear_complejo(real, imaginario)
        indice = int(indice)

        modulo = abs(numero)

        st.divider()

        # PROPIEDADES DEL NÚMERO
        st.subheader("2. Propiedades del número original")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Número complejo",
                convertir_a_texto(numero)
            )

        with c2:
            st.metric("Módulo", f"{modulo:.5f}")

        with c3:
            if modulo != 0:
                argumento = np.angle(numero)
                if argumento < 0:
                    argumento += 2 * np.pi

                st.metric(
                    "Argumento (rad)",
                    f"{argumento:.5f}"
                )
            else:
                st.metric("Argumento (rad)", "No definido")

        st.divider()

        # CÁLCULO DE RAÍCES
        st.subheader("3. Resultados de las raíces")

        raices = obtener_raices(numero, indice)

        resultados = []

        for i, raiz in enumerate(raices):

            comprobacion = raiz ** indice
            error = abs(comprobacion - numero)

            resultados.append({
                "Raíz": i + 1,
                "Parte real": raiz.real,
                "Parte imaginaria": raiz.imag,
                "Resultado": convertir_a_texto(raiz),
                "Comprobación": convertir_a_texto(comprobacion),
                "Error": error
            })

            with st.expander(
                f"Raíz {i + 1}: {convertir_a_texto(raiz)}"
            ):

                st.write("**Valor de la raíz:**")

                st.latex(
                    rf"w_{{{i}}}={convertir_a_texto(raiz)}"
                )

                st.write("**Comprobación:**")

                st.latex(
                    rf"w_{{{i}}}^{{{indice}}}="
                    rf"{convertir_a_texto(comprobacion)}"
                )

                st.write(f"Error numérico: {error:.12f}")

                if np.isclose(comprobacion, numero):
                    st.success("La comprobación es correcta.")
                else:
                    st.warning("Revisa el resultado de esta raíz.")

        st.divider()

        # DESARROLLO PASO A PASO
        st.subheader("4. Desarrollo paso a paso")

        st.write(
            "Aprende a calcular las raíces n-ésimas "
            "utilizando la fórmula de De Moivre."
        )

        if modulo == 0:

            st.info(
                "El número complejo es cero. Todas sus raíces "
                "son cero y su argumento no está definido."
            )

        else:

            # PASO 1
            st.markdown("### Paso 1. Identificar el número complejo")

            st.write(
                "Todo número complejo se puede expresar "
                "en la forma z = a + bi."
            )

            st.latex(
                rf"z={convertir_a_texto(numero)}"
            )

            # PASO 2
            st.markdown("### Paso 2. Calcular el módulo")

            st.write(
                "El módulo representa la distancia del número "
                "complejo al origen del plano."
            )

            st.latex(r"r=|z|=\sqrt{a^2+b^2}")

            suma_cuadrados = real**2 + imaginario**2

            st.write("Sustituimos la parte real y la imaginaria:")

            st.latex(
                rf"r=\sqrt{{({real})^2+({imaginario})^2}}"
            )

            st.latex(
                rf"r=\sqrt{{{suma_cuadrados:.5f}}}"
                rf"={modulo:.5f}"
            )

            # PASO 3
            st.markdown("### Paso 3. Calcular el argumento")

            st.write(
                "El argumento es el ángulo que forma el número "
                "complejo con el eje real positivo."
            )

            argumento = np.angle(numero)

            if argumento < 0:
                argumento += 2 * np.pi

            st.latex(
                rf"\theta=\operatorname{{arg}}(z)"
                rf"={argumento:.5f}\text{{ rad}}"
            )

            st.latex(
                rf"\theta={np.degrees(argumento):.2f}^\circ"
            )

            # PASO 4
            st.markdown("### Paso 4. Aplicar la fórmula de De Moivre")

            st.write(
                "Para encontrar las raíces n-ésimas, "
                "utilizamos la siguiente expresión:"
            )

            st.latex(
                r"w_k=\sqrt[n]{r}\left["
                r"\cos\left(\frac{\theta+2k\pi}{n}\right)"
                r"+i\sin\left(\frac{\theta+2k\pi}{n}\right)"
                r"\right]"
            )

            radio_raiz = modulo ** (1 / indice)

            st.write("Calculamos la raíz n-ésima del módulo:")

            st.latex(
                rf"\sqrt[{indice}]{{{modulo:.5f}}}"
                rf"={radio_raiz:.5f}"
            )

            # PASO 5
            st.markdown("### Paso 5. Calcular cada raíz")

            st.write(
                f"Calculamos las raíces utilizando "
                f"k = 0, 1, ..., {indice - 1}."
            )

            def formato_trigonometrico(valor):

                if np.isclose(valor, 0, atol=1e-10):
                    return "0"

                if np.isclose(valor, 1, atol=1e-10):
                    return "1"

                if np.isclose(valor, -1, atol=1e-10):
                    return "-1"

                return f"{valor:.5f}"

            for k in range(indice):

                angulo_k = (
                    argumento + 2 * k * np.pi
                ) / indice

                grados_k = np.degrees(angulo_k)

                coseno = np.cos(angulo_k)
                seno = np.sin(angulo_k)

                parte_real = radio_raiz * coseno
                parte_imaginaria = radio_raiz * seno

                raiz_actual = complex(
                    parte_real,
                    parte_imaginaria
                )

                with st.expander(
                    f"Desarrollo de la raíz {k + 1}",
                    expanded=(indice <= 3)
                ):

                    st.write("**1. Calculamos el ángulo:**")

                    st.latex(
                        rf"\alpha_{{{k}}}="
                        rf"\frac{{{argumento:.5f}+2({k})\pi}}"
                        rf"{{{indice}}}"
                    )

                    st.latex(
                        rf"\alpha_{{{k}}}={angulo_k:.5f}"
                        rf"\text{{ rad}}"
                    )

                    st.write(
                        f"Ángulo en grados: {grados_k:.2f}°"
                    )

                    st.write("**2. Evaluamos el coseno y el seno:**")

                    st.latex(
                        rf"\cos({angulo_k:.5f})="
                        rf"{formato_trigonometrico(coseno)}"
                    )

                    st.latex(
                        rf"\sin({angulo_k:.5f})="
                        rf"{formato_trigonometrico(seno)}"
                    )

                    st.write("**3. Calculamos la parte real:**")

                    st.latex(
                        rf"\operatorname{{Re}}(w_{{{k}}})="
                        rf"{radio_raiz:.5f}"
                        rf"\cdot {formato_trigonometrico(coseno)}"
                        rf"={parte_real:.5f}"
                    )

                    st.write("**4. Calculamos la parte imaginaria:**")

                    st.latex(
                        rf"\operatorname{{Im}}(w_{{{k}}})="
                        rf"{radio_raiz:.5f}"
                        rf"\cdot {formato_trigonometrico(seno)}"
                        rf"={parte_imaginaria:.5f}"
                    )

                    st.write("**5. Resultado de la raíz:**")

                    st.latex(
                        rf"w_{{{k}}}="
                        rf"{convertir_a_texto(raiz_actual)}"
                    )

                    st.success(
                        "Resultado: "
                        + convertir_a_texto(raices[k])
                    )

            # PASO 6
            st.markdown("### Paso 6. Comprobar las soluciones")

            st.write(
                "Elevamos cada raíz al índice correspondiente. "
                "El resultado debe ser el número complejo original."
            )

            for k, raiz in enumerate(raices):

                comprobacion = raiz ** indice

                st.latex(
                    rf"(w_{{{k}}})^{{{indice}}}"
                    rf"={convertir_a_texto(comprobacion)}"
                )

                if np.isclose(comprobacion, numero):
                    st.success(
                        f"Raíz {k + 1}: comprobación correcta."
                    )
                else:
                    st.warning(
                        f"Raíz {k + 1}: revisa el resultado."
                    )

        st.divider()

        # TABLA DE RESULTADOS
        st.subheader("5. Tabla de todas las raíces")

        st.dataframe(
            resultados,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # REPRESENTACIÓN GRÁFICA
        st.subheader("6. Representación en el plano complejo")

        figura = go.Figure()

        radio = modulo ** (1 / indice)

        angulos = np.linspace(0, 2 * np.pi, 300)

        figura.add_trace(
            go.Scatter(
                x=radio * np.cos(angulos),
                y=radio * np.sin(angulos),
                mode="lines",
                name="Circunferencia de las raíces",
                line=dict(dash="dash")
            )
        )

        for raiz in raices:

            figura.add_trace(
                go.Scatter(
                    x=[0, raiz.real],
                    y=[0, raiz.imag],
                    mode="lines",
                    showlegend=False,
                    line=dict(width=1)
                )
            )

        figura.add_trace(
            go.Scatter(
                x=[r.real for r in raices],
                y=[r.imag for r in raices],
                mode="markers+text",
                text=[
                    f"Raíz {i + 1}"
                    for i in range(len(raices))
                ],
                textposition="top center",
                marker=dict(size=12),
                name="Raíces"
            )
        )

        figura.add_trace(
            go.Scatter(
                x=[0],
                y=[0],
                mode="markers",
                marker=dict(size=8),
                name="Origen"
            )
        )

        figura.update_layout(
            title="Distribución de las raíces n-ésimas",
            xaxis_title="Parte real",
            yaxis_title="Parte imaginaria",
            template="plotly_white",
            height=550,
            hovermode="closest"
        )

        figura.update_xaxes(
            zeroline=True,
            zerolinewidth=2
        )

        figura.update_yaxes(
            zeroline=True,
            zerolinewidth=2,
            scaleanchor="x",
            scaleratio=1
        )

        st.plotly_chart(
            figura,
            use_container_width=True
        )

        st.info(
            "Las raíces se distribuyen uniformemente alrededor "
            "de una circunferencia. Puedes modificar el número "
            "complejo y el índice para observar cómo cambian "
            "los resultados y su representación."
        )



 
    # =====================================
    # REGIONES DEL PLANO COMPLEJO
    # =====================================

    elif seccion == "Regiones del plano":

        st.header("Regiones del plano complejo")

        st.write(
            "Aprende a identificar, construir y representar "
            "regiones del plano complejo mediante desigualdades."
        )

        st.latex(r"z=x+yi")

        st.info(
            "Cada punto del plano representa un número complejo. "
            "El eje horizontal corresponde a la parte real y "
            "el eje vertical a la parte imaginaria."
        )

        # INTRODUCCIÓN
        st.subheader("1. ¿Qué es una región del plano complejo?")

        st.write(
            "Una región es un conjunto de puntos del plano complejo "
            "que cumplen una o varias condiciones matemáticas."
        )

        st.write(
            "Por ejemplo, podemos seleccionar todos los puntos "
            "cuya distancia a un centro sea menor o igual que un radio."
        )

        st.latex(r"|z-z_0|\leq r")

        st.write(
            "Esta expresión representa un disco: todos los puntos "
            "que están dentro de una circunferencia, incluyendo "
            "su frontera."
        )

        st.divider()

        # SELECTOR DE REGIONES
        st.subheader("2. Selecciona el tipo de región")

        tipo_region = st.selectbox(
            "¿Qué región quieres estudiar?",
            [
                "Disco circular",
                "Circunferencia",
                "Corona circular",
                "Semiplano imaginario",
                "Intersección de regiones"
            ]
        )

        st.divider()

        # CONFIGURACIÓN
        st.subheader("3. Configura la región")

        # Valores iniciales
        centro_real = 0.0
        centro_imaginario = 0.0
        radio_externo = 0.0
        radio_interno = 0.0
        limite_imaginario = 0.0
        relacion = ">="

        # CONFIGURACIÓN CIRCULAR
        if tipo_region != "Semiplano imaginario":

            col1, col2 = st.columns(2)

            with col1:
                centro_real = st.number_input(
                    "Centro: parte real",
                    value=0.0,
                    step=0.5,
                    key="region_centro_real"
                )

            with col2:
                centro_imaginario = st.number_input(
                    "Centro: parte imaginaria",
                    value=0.0,
                    step=0.5,
                    key="region_centro_imag"
                )

            radio_externo = st.slider(
                "Radio externo",
                min_value=0.5,
                max_value=8.0,
                value=3.0,
                step=0.5,
                key="region_radio_externo"
            )

        # RADIO INTERNO
        if tipo_region in [
            "Corona circular",
            "Intersección de regiones"
        ]:

            radio_interno = st.slider(
                "Radio interno",
                min_value=0.0,
                max_value=7.5,
                value=1.0,
                step=0.5,
                key="region_radio_interno"
            )

        # CONFIGURACIÓN DEL SEMIPLANO
        if tipo_region in [
            "Semiplano imaginario",
            "Intersección de regiones"
        ]:

            limite_imaginario = st.number_input(
                "Límite de la parte imaginaria",
                value=0.0,
                step=0.5,
                key="region_limite_imaginario"
            )

            relacion = st.selectbox(
                "Desigualdad",
                [">", ">=", "<", "<="],
                key="region_desigualdad"
            )

        limite_grafica = st.slider(
            "Tamaño de la gráfica",
            min_value=3,
            max_value=12,
            value=6,
            key="region_tamano_grafica"
        )

        # VALIDACIÓN
        if (
            tipo_region in [
                "Corona circular",
                "Intersección de regiones"
            ]
            and radio_interno >= radio_externo
        ):

            st.error(
                "El radio interno debe ser menor que el radio externo."
            )

        else:

            st.divider()

            # CONSTRUCCIÓN DE LA REGIÓN
            st.subheader("4. Representación gráfica")

            X, Y = generar_malla(
                limite=limite_grafica,
                puntos=300
            )

            distancia = calcular_modulo_relativo(
                X,
                Y,
                centro_real,
                centro_imaginario
            )

            if tipo_region == "Disco circular":

                region = distancia <= radio_externo

                explicacion = (
                    "Se representan los puntos cuya distancia "
                    "al centro es menor o igual al radio."
                )

                formula = r"|z-z_0|\leq R"

            elif tipo_region == "Circunferencia":

                region = np.isclose(
                    distancia,
                    radio_externo,
                    atol=0.04
                )

                explicacion = (
                    "Se representan los puntos situados sobre "
                    "la circunferencia. No se incluye el interior."
                )

                formula = r"|z-z_0|=R"

            elif tipo_region == "Corona circular":

                region = (
                    (distancia >= radio_interno) &
                    (distancia <= radio_externo)
                )

                explicacion = (
                    "Se representan los puntos que están entre "
                    "el radio interno y el radio externo."
                )

                formula = r"r_1\leq |z-z_0|\leq r_2"

            elif tipo_region == "Semiplano imaginario":

                region = pertenece_a_semiplano_imaginario(
                    Y,
                    limite_imaginario,
                    relacion
                )

                explicacion = (
                    "Se representan los puntos que cumplen "
                    "la desigualdad sobre la parte imaginaria."
                )

                formula = (
                    rf"\operatorname{{Im}}(z)"
                    rf"{relacion}{limite_imaginario}"
                )

            else:

                corona = pertenece_a_corona(
                    X,
                    Y,
                    radio_interno,
                    radio_externo,
                    centro_real,
                    centro_imaginario
                )

                semiplano = pertenece_a_semiplano_imaginario(
                    Y,
                    limite_imaginario,
                    relacion
                )

                region = corona & semiplano

                explicacion = (
                    "Se representa la intersección entre una corona "
                    "circular y un semiplano imaginario."
                )

                formula = (
                    rf"{radio_interno}\leq |z-z_0|"
                    rf"\leq {radio_externo},\quad "
                    rf"\operatorname{{Im}}(z){relacion}"
                    rf"{limite_imaginario}"
                )

            # GRÁFICA
            figura = go.Figure()

            figura.add_trace(
                go.Heatmap(
                    x=X[0],
                    y=Y[:, 0],
                    z=region.astype(int),
                    colorscale=[
                        [0, "white"],
                        [1, "royalblue"]
                    ],
                    showscale=False,
                    hovertemplate=(
                        "Parte real: %{x:.2f}<br>"
                        "Parte imaginaria: %{y:.2f}"
                        "<extra></extra>"
                    )
                )
            )

            angulos = np.linspace(0, 2 * np.pi, 400)

            if tipo_region != "Semiplano imaginario":

                figura.add_trace(
                    go.Scatter(
                        x=centro_real + radio_externo * np.cos(angulos),
                        y=centro_imaginario + radio_externo * np.sin(angulos),
                        mode="lines",
                        name="Radio externo",
                        line=dict(color="black", dash="dash")
                    )
                )

            if tipo_region in [
                "Corona circular",
                "Intersección de regiones"
            ]:

                figura.add_trace(
                    go.Scatter(
                        x=centro_real + radio_interno * np.cos(angulos),
                        y=centro_imaginario + radio_interno * np.sin(angulos),
                        mode="lines",
                        name="Radio interno",
                        line=dict(color="red", dash="dash")
                    )
                )

            if tipo_region in [
                "Semiplano imaginario",
                "Intersección de regiones"
            ]:

                figura.add_hline(
                    y=limite_imaginario,
                    line_dash="dot",
                    line_color="red",
                    annotation_text="Límite del semiplano"
                )

            if tipo_region != "Semiplano imaginario":

                figura.add_trace(
                    go.Scatter(
                        x=[centro_real],
                        y=[centro_imaginario],
                        mode="markers",
                        name="Centro",
                        marker=dict(color="black", size=10)
                    )
                )

            figura.update_layout(
                title=tipo_region,
                xaxis_title="Parte real (x)",
                yaxis_title="Parte imaginaria (y)",
                template="plotly_white",
                height=600
            )

            figura.update_yaxes(
                scaleanchor="x",
                scaleratio=1
            )

            st.plotly_chart(
                figura,
                use_container_width=True
            )

            # EXPLICACIÓN MATEMÁTICA
            st.subheader("5. Interpretación matemática")

            st.latex(formula)

            st.write(explicacion)

            if tipo_region != "Semiplano imaginario":

                st.write(
                    "El centro de la región es el número complejo:"
                )

                st.latex(
                    rf"z_0={centro_real}+({centro_imaginario})i"
                )

            # PUNTO DE PRUEBA
            st.divider()

            st.subheader(
                "6. Comprueba si un punto pertenece a la región"
            )

            cp1, cp2 = st.columns(2)

            with cp1:
                punto_real = st.number_input(
                    "Parte real del punto",
                    value=1.0,
                    step=0.5,
                    key="prueba_region_real"
                )

            with cp2:
                punto_imaginario = st.number_input(
                    "Parte imaginaria del punto",
                    value=1.0,
                    step=0.5,
                    key="prueba_region_imag"
                )

            distancia_punto = calcular_modulo_relativo(
                punto_real,
                punto_imaginario,
                centro_real,
                centro_imaginario
            )

            if tipo_region == "Disco circular":

                pertenece = distancia_punto <= radio_externo

            elif tipo_region == "Circunferencia":

                pertenece = np.isclose(
                    distancia_punto,
                    radio_externo,
                    atol=0.04
                )

            elif tipo_region == "Corona circular":

                pertenece = (
                    radio_interno <= distancia_punto <= radio_externo
                )

            elif tipo_region == "Semiplano imaginario":

                pertenece = pertenece_a_semiplano_imaginario(
                    punto_imaginario,
                    limite_imaginario,
                    relacion
                )

            else:

                pertenece = (
                    radio_interno <= distancia_punto <= radio_externo
                    and pertenece_a_semiplano_imaginario(
                        punto_imaginario,
                        limite_imaginario,
                        relacion
                    )
                )

            st.write(
                f"Punto evaluado: "
                f"{punto_real} + ({punto_imaginario})i"
            )

            if tipo_region != "Semiplano imaginario":

                st.write(
                    f"Distancia al centro: {distancia_punto:.5f}"
                )

            if pertenece:
                st.success(
                    "El punto pertenece a la región seleccionada."
                )
            else:
                st.error(
                    "El punto no pertenece a la región seleccionada."
                )


    # =====================================
    # DOMINIOS DE FUNCIONES COMPLEJAS
    # =====================================

    elif seccion == "Dominios de funciones":

        st.header("Dominio de funciones complejas")

        st.write(
            "Introduce una función racional compleja y "
            "calcula automáticamente su dominio."
        )

        st.info(
            "Puedes utilizar z como variable, I para la unidad "
            "imaginaria y ** para indicar potencias."
        )

        # 1. CONSTRUIR LA FUNCION
        st.subheader("1. Construye tu función")

        numerador_texto = st.text_input(
            "Numerador",
            value="z + 2",
            key="dominio_numerador"
        )

        denominador_texto = st.text_input(
            "Denominador",
            value="z**3 + 9*z",
            key="dominio_denominador"
        )

        st.write("Función introducida:")

        st.latex(r"f(z)=\frac{N(z)}{D(z)}")

        st.divider()

        # 2. CALCULAR EL DOMINIO
        if st.button("Calcular dominio", key="calcular_dominio"):

            try:
                numerador = sp.sympify(
                    numerador_texto,
                    locals={"z": z, "I": sp.I, "i": sp.I}
                )

                denominador = sp.sympify(
                    denominador_texto,
                    locals={"z": z, "I": sp.I, "i": sp.I}
                )

                resultado = analizar_funcion(
                    numerador,
                    denominador
                )

                st.session_state["resultado_dominio"] = resultado

            except Exception as error:
                st.error(
                    f"No se pudo analizar la función: {error}"
                )

        # 3. MOSTRAR LOS RESULTADOS
        if "resultado_dominio" in st.session_state:

            resultado = st.session_state["resultado_dominio"]

            st.divider()

            st.subheader("2. Función analizada")

            st.latex(
                sp.latex(resultado["funcion"])
            )

            # FACTORIZACION
            st.subheader("3. Factorización del denominador")

            denominador_factorizado = sp.factor(
                resultado["denominador"]
            )

            st.latex(
                sp.latex(denominador_factorizado)
            )

            st.write(
                "Igualamos el denominador a cero para encontrar "
                "los puntos excluidos."
            )

            st.latex(
                sp.latex(resultado["denominador"]) + "=0"
            )

            # PUNTOS EXCLUIDOS
            st.subheader("4. Análisis del dominio")

            excluidos = resultado["puntos_excluidos"]

            if excluidos:

                st.write("Puntos excluidos:")

                for punto in excluidos:
                    st.latex(
                        "z=" + sp.latex(punto)
                    )

                puntos_latex = ", ".join(
                    sp.latex(punto) for punto in excluidos
                )

                st.success(
                    "El dominio se ha calculado correctamente."
                )

                st.latex(
                    r"D_f=\mathbb{C}\setminus\{" +
                    puntos_latex +
                    r"\}"
                )

            else:

                st.success(
                    "No se encontraron restricciones por denominador."
                )

                st.latex(
                    r"D_f=\mathbb{C}"
                )

            # EXPLICACION
            st.subheader("5. Explicación del resultado")

            for paso in explicar_dominio(resultado):
                st.write(paso)

            # GRAFICA DEL PLANO COMPLEJO
            st.divider()

            st.subheader(
                "6. Representación en el plano complejo"
            )

            puntos_x = []
            puntos_y = []
            etiquetas = []

            # Convertir los puntos excluidos en coordenadas
            for punto in excluidos:

                numero = complex(sp.N(punto))

                puntos_x.append(numero.real)
                puntos_y.append(numero.imag)

                etiquetas.append(
                    f"z = {sp.sstr(punto)}"
                )

            # Determinar el tamaño de la gráfica
            limite = max(
                [abs(valor) for valor in puntos_x] +
                [abs(valor) for valor in puntos_y] +
                [3]
            ) + 2

            figura = go.Figure()

            # Dibujar los puntos excluidos
            if puntos_x:

                figura.add_trace(
                    go.Scatter(
                        x=puntos_x,
                        y=puntos_y,
                        mode="markers+text",
                        text=etiquetas,
                        textposition="top center",
                        name="Puntos excluidos",
                        marker=dict(
                            color="red",
                            size=13,
                            symbol="x"
                        )
                    )
                )

            # Ejes del plano complejo
            figura.add_hline(
                y=0,
                line_color="gray",
                line_width=1
            )

            figura.add_vline(
                x=0,
                line_color="gray",
                line_width=1
            )

            # Configuración visual
            figura.update_layout(
                title="Puntos excluidos del dominio",
                xaxis_title="Parte real",
                yaxis_title="Parte imaginaria",
                xaxis=dict(
                    range=[-limite, limite],
                    zeroline=False,
                    gridcolor="lightgray"
                ),
                yaxis=dict(
                    range=[-limite, limite],
                    zeroline=False,
                    gridcolor="lightgray",
                    scaleanchor="x",
                    scaleratio=1
                ),
                template="plotly_white",
                height=550
            )

            st.plotly_chart(
                figura,
                use_container_width=True
            )

            if puntos_x:

                st.caption(
                    "Los puntos rojos representan valores de z "
                    "que no pertenecen al dominio de la función."
                )

            else:

                st.success(
                    "No hay puntos excluidos para representar."
                )

            # =====================================
            # 7. EVALUAR UN NUMERO COMPLEJO
            # =====================================

            st.divider()

            st.subheader("7. Evaluar un número complejo")

            st.write(
                "Introduce un número complejo para comprobar "
                "si pertenece al dominio y evaluar la función."
            )

            col1, col2 = st.columns(2)

            with col1:
                parte_real = st.number_input(
                    "Parte real",
                    value=1.0,
                    key="dominio_parte_real"
                )

            with col2:
                parte_imaginaria = st.number_input(
                    "Parte imaginaria",
                    value=2.0,
                    key="dominio_parte_imaginaria"
                )

            if st.button(
                "Evaluar número complejo",
                key="evaluar_numero_dominio"
            ):

                try:

                    valor = (
                        sp.Float(parte_real)
                        + sp.Float(parte_imaginaria) * sp.I
                    )

                    resultado_evaluacion = evaluar_funcion(
                        resultado,
                        valor
                    )

                    st.success(
                        "El número complejo pertenece al dominio."
                    )

                    st.write("Número introducido:")

                    st.latex(
                        "z=" + sp.latex(valor)
                    )

                    st.write("Resultado de la función:")

                    st.latex(
                        "f(z)=" + sp.latex(resultado_evaluacion)
                    )

                except ValueError:

                    st.error(
                        "El número introducido está excluido "
                        "del dominio de la función."
                    )

                except Exception as error:

                    st.error(
                        f"No se pudo evaluar el número: {error}"
                    )

    # =====================================
    # TRANSFORMACIONES
    # =====================================

    elif seccion == "Transformaciones":

        st.header("Transformaciones complejas")

        st.write(
            "Observa cómo una transformación modifica "
            "los puntos del plano complejo."
        )

        st.latex(r"w=z^2")

        valor = st.number_input(
            "Valor de la parte imaginaria de z",
            value=2.0
        )

        z_original, w_transformado = transformar_recta_imaginaria(
            valor=valor
        )

        figura = go.Figure()

        figura.add_trace(
            go.Scatter(
                x=z_original.real,
                y=z_original.imag,
                mode="lines",
                name="Recta original z"
            )
        )

        figura.add_trace(
            go.Scatter(
                x=w_transformado.real,
                y=w_transformado.imag,
                mode="lines",
                name="Imagen w = z²"
            )
        )

        figura.update_layout(
            title="Transformación del plano complejo",
            xaxis_title="Parte real",
            yaxis_title="Parte imaginaria",
            template="plotly_white",
            height=550
        )

        st.plotly_chart(figura, use_container_width=True)

        ecuacion = obtener_ecuacion_parabola(valor)

        st.subheader("Ecuación de la curva resultante")

        st.latex(
            rf"v^2={ecuacion['coeficiente']}"
            rf"(u+{ecuacion['desplazamiento']})"
        )

        st.info(
            "La recta horizontal original se transforma "
            "en una parábola en el plano de w."
        )
