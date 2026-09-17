"""
Nodos del Árbol de Sintaxis Abstracta (AST) para StatScript.

Cada clase representa un tipo de construcción del lenguaje.
El parser construye estas estructuras al analizar la lista de tokens.
"""

from dataclasses import dataclass, field
from typing import List, Any, Optional


@dataclass
class NodoAST:
    """Nodo base del árbol de sintaxis abstracta."""
    pass


# ── Nodo raíz ──

@dataclass
class Programa(NodoAST):
    """Representa un programa completo de StatScript (lista de sentencias)."""
    sentencias: List[NodoAST] = field(default_factory=list)


# ── Sentencias (comandos) ──

@dataclass
class CargarStmt(NodoAST):
    archivo: str = ""

@dataclass
class MostrarStmt(NodoAST):
    objetivo: str = ""

@dataclass
class CalcularStmt(NodoAST):
    funcion: str = ""
    columna: str = ""

@dataclass
class FiltrarStmt(NodoAST):
    condicion: Any = None

@dataclass
class OrdenarStmt(NodoAST):
    columna: str = ""
    orden: str = ""

@dataclass
class AgruparStmt(NodoAST):
    columna: str = ""

@dataclass
class GraficarStmt(NodoAST):
    tipo: str = ""
    columna: str = ""

@dataclass
class ExportarStmt(NodoAST):
    archivo: str = ""

@dataclass
class AsignacionStmt(NodoAST):
    nombre: str = ""
    expresion: Any = None


# ── Expresiones ──

@dataclass
class Condicion(NodoAST):
    izquierda: Any = None
    operador: str = ""
    derecha: Any = None

@dataclass
class CondicionCompuesta(NodoAST):
    izquierda: Any = None
    operador_logico: str = ""
    derecha: Any = None

@dataclass
class ExpresionBinaria(NodoAST):
    izquierda: Any = None
    operador: str = ""
    derecha: Any = None

@dataclass
class Literal(NodoAST):
    valor: Any = None
    tipo: str = ""

@dataclass
class Identificador(NodoAST):
    nombre: str = ""


# ── Impresión del AST ──

OPERADORES_SIMBOLO = {
    'MAYOR': '>', 'MENOR': '<', 'MAYOR_IGUAL': '>=', 'MENOR_IGUAL': '<=',
    'IGUAL': '==', 'DIFERENTE': '!=',
    'MAS': '+', 'MENOS': '-', 'MULTIPLICAR': '*', 'DIVIDIR': '/', 'MODULO': '%',
}


def imprimir_ast(nodo, indent=0):
    """Imprime el AST con indentación legible."""
    prefijo = "  " * indent

    if isinstance(nodo, Programa):
        print(f"{prefijo}Programa")
        for stmt in nodo.sentencias:
            imprimir_ast(stmt, indent + 1)

    elif isinstance(nodo, CargarStmt):
        print(f"{prefijo}CargarStmt(archivo=\"{nodo.archivo}\")")

    elif isinstance(nodo, MostrarStmt):
        print(f"{prefijo}MostrarStmt(objetivo=\"{nodo.objetivo}\")")

    elif isinstance(nodo, CalcularStmt):
        print(f"{prefijo}CalcularStmt(funcion=\"{nodo.funcion}\", columna=\"{nodo.columna}\")")

    elif isinstance(nodo, FiltrarStmt):
        print(f"{prefijo}FiltrarStmt")
        imprimir_ast(nodo.condicion, indent + 1)

    elif isinstance(nodo, OrdenarStmt):
        orden = nodo.orden if nodo.orden else "default"
        print(f"{prefijo}OrdenarStmt(columna=\"{nodo.columna}\", orden=\"{orden}\")")

    elif isinstance(nodo, AgruparStmt):
        print(f"{prefijo}AgruparStmt(columna=\"{nodo.columna}\")")

    elif isinstance(nodo, GraficarStmt):
        print(f"{prefijo}GraficarStmt(tipo=\"{nodo.tipo}\", columna=\"{nodo.columna}\")")

    elif isinstance(nodo, ExportarStmt):
        print(f"{prefijo}ExportarStmt(archivo=\"{nodo.archivo}\")")

    elif isinstance(nodo, AsignacionStmt):
        print(f"{prefijo}AsignacionStmt(nombre=\"{nodo.nombre}\")")
        imprimir_ast(nodo.expresion, indent + 1)

    elif isinstance(nodo, CondicionCompuesta):
        op = nodo.operador_logico.upper()
        if nodo.derecha is None:
            # Operador unario NO
            print(f"{prefijo}NegacionLogica(NO)")
            imprimir_ast(nodo.izquierda, indent + 1)
        else:
            print(f"{prefijo}CondicionCompuesta(op=\"{op}\")")
            imprimir_ast(nodo.izquierda, indent + 1)
            imprimir_ast(nodo.derecha, indent + 1)

    elif isinstance(nodo, Condicion):
        if nodo.operador == 'BOOL':
            izq = _valor_str(nodo.izquierda)
            print(f"{prefijo}Condicion({izq})")
        else:
            op_sym = OPERADORES_SIMBOLO.get(nodo.operador, nodo.operador)
            izq = _valor_str(nodo.izquierda)
            der = _valor_str(nodo.derecha)
            print(f"{prefijo}Condicion({izq} {op_sym} {der})")

    elif isinstance(nodo, ExpresionBinaria):
        op_sym = OPERADORES_SIMBOLO.get(nodo.operador, nodo.operador)
        print(f"{prefijo}ExpresionBinaria(op=\"{op_sym}\")")
        imprimir_ast(nodo.izquierda, indent + 1)
        imprimir_ast(nodo.derecha, indent + 1)

    elif isinstance(nodo, Literal):
        print(f"{prefijo}Literal({nodo.valor!r})")

    elif isinstance(nodo, Identificador):
        print(f"{prefijo}Identificador(\"{nodo.nombre}\")")

    else:
        print(f"{prefijo}{nodo}")


def _valor_str(nodo):
    """Convierte un nodo hoja a representación corta para impresión inline."""
    if isinstance(nodo, Identificador):
        return nodo.nombre
    elif isinstance(nodo, Literal):
        return repr(nodo.valor)
    return str(nodo)
