
import ast
import numpy as np
import operator


# Operaciones matemáticas permitidas
OPERADORES = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}

FUNCIONES = {
    "sin": np.sin,
    "cos": np.cos,
    "tan": np.tan,
    "exp": np.exp,
    "sqrt": np.sqrt,
    "log": np.log,
    "abs": np.abs,
}

CONSTANTES = {
    "pi": np.pi,
    "e": np.e,
}


def evaluar_nodo(nodo):

    if isinstance(nodo, ast.Expression):
        return evaluar_nodo(nodo.body)

    elif isinstance(nodo, ast.Constant):
        if isinstance(nodo.value, (int, float)):
            return nodo.value
        raise ValueError("Solo se permiten números.")

    elif isinstance(nodo, ast.Name):
        if nodo.id == "x":
            return x_actual
        if nodo.id in CONSTANTES:
            return CONSTANTES[nodo.id]
        raise ValueError(f"Nombre no permitido: {nodo.id}")

    elif isinstance(nodo, ast.BinOp):
        tipo = type(nodo.op)

        if tipo not in OPERADORES:
            raise ValueError("Operación no permitida.")

        izquierda = evaluar_nodo(nodo.left)
        derecha = evaluar_nodo(nodo.right)

        return OPERADORES[tipo](izquierda, derecha)

    elif isinstance(nodo, ast.UnaryOp):
        valor = evaluar_nodo(nodo.operand)

        if isinstance(nodo.op, ast.USub):
            return -valor
        if isinstance(nodo.op, ast.UAdd):
            return valor

        raise ValueError("Operación no permitida.")

    elif isinstance(nodo, ast.Call):
        if not isinstance(nodo.func, ast.Name):
            raise ValueError("Función no permitida.")

        nombre = nodo.func.id

        if nombre not in FUNCIONES:
            raise ValueError(f"Función no permitida: {nombre}")

        if nodo.keywords or len(nodo.args) != 1:
            raise ValueError("La función debe tener un solo argumento.")

        argumento = evaluar_nodo(nodo.args[0])

        return FUNCIONES[nombre](argumento)

    else:
        raise ValueError("Expresión matemática no válida.")


def crear_funcion(expresion):

    try:
        arbol = ast.parse(expresion, mode="eval")

        def funcion(x):
            global x_actual
            x_actual = np.asarray(x, dtype=float)
            resultado = evaluar_nodo(arbol)
            return np.asarray(resultado, dtype=float)

        return funcion

    except Exception as error:
        raise ValueError(
            f"No se pudo interpretar la función: {error}"
        )
