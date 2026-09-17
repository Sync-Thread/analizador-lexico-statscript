"""
Parser recursivo descendente para StatScript.

Consume la lista de tokens generada por el Scanner y construye
un Árbol de Sintaxis Abstracta (AST). Implementa recuperación
de errores mediante sincronización al siguiente punto y coma.
"""

from typing import List, Optional
from token_model import Token
from ast_nodes import (
    Programa, CargarStmt, MostrarStmt, CalcularStmt, FiltrarStmt,
    OrdenarStmt, AgruparStmt, GraficarStmt, ExportarStmt, AsignacionStmt,
    Condicion, CondicionCompuesta, ExpresionBinaria, Literal, Identificador,
    NodoAST,
)


class ErrorSintactico(Exception):
    """Representa un error encontrado durante el análisis sintáctico."""

    def __init__(self, mensaje, token=None):
        self.mensaje = mensaje
        self.token = token
        if token:
            self.linea = token.line
            self.columna = token.column
        else:
            self.linea = 0
            self.columna = 0
        super().__init__(mensaje)

    def __str__(self):
        if self.token:
            return f"Linea {self.linea}, Columna {self.columna}: {self.mensaje}"
        return self.mensaje


# Conjuntos de tipos de token usados en las reglas gramaticales
FUNCIONES_ESTADISTICAS = {
    'PROMEDIO', 'MEDIANA', 'MODA', 'DESVIACION', 'VARIANZA',
    'CONTEO', 'SUMA', 'MINIMO', 'MAXIMO', 'CORRELACION',
}
TIPOS_GRAFICA = {'BARRAS', 'LINEAS', 'PASTEL', 'DISPERSION', 'HISTOGRAMA'}
OPS_RELACIONALES = {'MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL', 'IGUAL', 'DIFERENTE'}
OBJETOS_LENGUAJE = {'DATOS', 'COLUMNAS', 'REGISTROS'}


class Parser:
    """
    Analizador sintáctico para StatScript.

    Recibe una lista de tokens y produce un AST (Programa con sentencias).
    Los tokens NEWLINE y ERROR se filtran antes del análisis.
    """

    def __init__(self, tokens: List[Token]):
        # Filtrar tokens que no son relevantes para la sintaxis
        self.tokens = [t for t in tokens if t.type not in ('NEWLINE', 'ERROR')]
        self.pos = 0
        self.errores: List[ErrorSintactico] = []

    # ── API pública ──

    def parse(self) -> Programa:
        """Punto de entrada del parser. Retorna el AST completo."""
        programa = Programa()
        while not self._es_fin():
            try:
                stmt = self._sentencia()
                if stmt:
                    programa.sentencias.append(stmt)
            except ErrorSintactico as e:
                self.errores.append(e)
                self._sincronizar()
        return programa

    def tiene_errores(self) -> bool:
        return len(self.errores) > 0

    # ── Navegación sobre la lista de tokens ──

    def _actual(self) -> Token:
        """Retorna el token en la posición actual sin consumirlo."""
        return self.tokens[self.pos]

    def _es_fin(self) -> bool:
        """Verifica si se alcanzó el final de la lista de tokens."""
        return self.pos >= len(self.tokens) or self._actual().type == 'EOF'

    def _avanzar(self) -> Token:
        """Consume y retorna el token actual, avanzando la posición."""
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def _verificar(self, *tipos) -> bool:
        """Retorna True si el token actual es de alguno de los tipos indicados."""
        if self._es_fin():
            return False
        return self._actual().type in tipos

    def _consumir(self, *tipos) -> Optional[Token]:
        """Consume el token actual solo si su tipo coincide. Retorna None si no coincide."""
        if self._verificar(*tipos):
            return self._avanzar()
        return None

    def _esperar(self, tipo, mensaje="") -> Token:
        """Consume el token actual si coincide con el tipo esperado, o lanza error."""
        if self._verificar(tipo):
            return self._avanzar()
        actual = self._actual() if not self._es_fin() else None
        msg = mensaje or f"Se esperaba {tipo}"
        raise ErrorSintactico(msg, actual)

    def _esperar_id_o_objeto(self, mensaje="") -> Token:
        """Consume un ID o un objeto del lenguaje (datos, columnas, registros) como identificador."""
        if self._verificar('ID', *OBJETOS_LENGUAJE):
            return self._avanzar()
        actual = self._actual() if not self._es_fin() else None
        msg = mensaje or "Se esperaba un identificador"
        raise ErrorSintactico(msg, actual)

    def _sincronizar(self):
        """Avanza hasta el siguiente punto y coma para recuperarse de un error."""
        while not self._es_fin():
            if self._actual().type == 'PUNTO_COMA':
                self._avanzar()
                return
            self._avanzar()

    # ── Reglas gramaticales ──

    def _sentencia(self):
        """sentencia → comando PUNTO_COMA"""
        stmt = self._comando()
        self._esperar('PUNTO_COMA', "Se esperaba ';' al final de la sentencia")
        return stmt

    def _comando(self):
        """comando → cargar | mostrar | calcular | filtrar | ordenar | agrupar | graficar | exportar | asignacion"""
        if self._verificar('CARGAR'):
            return self._cargar()
        elif self._verificar('MOSTRAR'):
            return self._mostrar()
        elif self._verificar('CALCULAR'):
            return self._calcular()
        elif self._verificar('FILTRAR'):
            return self._filtrar()
        elif self._verificar('ORDENAR'):
            return self._ordenar()
        elif self._verificar('AGRUPAR'):
            return self._agrupar()
        elif self._verificar('GRAFICAR'):
            return self._graficar()
        elif self._verificar('EXPORTAR'):
            return self._exportar()
        elif self._verificar('ID'):
            return self._asignacion()
        else:
            raise ErrorSintactico(
                f"Sentencia no reconocida: '{self._actual().value}'",
                self._actual()
            )

    def _cargar(self):
        """cargar → CARGAR CADENA"""
        self._avanzar()
        archivo = self._esperar('CADENA', "Se esperaba el nombre del archivo entre comillas")
        return CargarStmt(archivo=archivo.value)

    def _mostrar(self):
        """mostrar → MOSTRAR (DATOS | COLUMNAS | REGISTROS | ID)"""
        self._avanzar()
        if self._verificar(*OBJETOS_LENGUAJE, 'ID'):
            obj = self._avanzar()
            return MostrarStmt(objetivo=obj.value)
        else:
            raise ErrorSintactico(
                "Se esperaba 'datos', 'columnas', 'registros' o un identificador",
                self._actual()
            )

    def _calcular(self):
        """calcular → CALCULAR funcion_estadistica DE identificador (COMA identificador)? (operador_arit expresion)?"""
        self._avanzar()
        if not self._verificar(*FUNCIONES_ESTADISTICAS):
            raise ErrorSintactico("Se esperaba una función estadística", self._actual())
        funcion = self._avanzar()
        self._esperar('DE', "Se esperaba 'de' después de la función estadística")
        columna = self._esperar_id_o_objeto("Se esperaba el nombre de la columna")
        columna_val = columna.value
        # Soporte para dos columnas separadas por coma (ej: correlacion de x, y)
        if self._verificar('COMA'):
            self._avanzar()
            segunda = self._esperar_id_o_objeto("Se esperaba la segunda columna")
            columna_val = f"{columna_val}, {segunda.value}"
        # Soporte para operación aritmética opcional (ej: calcular suma de x / 100)
        if self._verificar('MAS', 'MENOS', 'MULTIPLICAR', 'DIVIDIR', 'MODULO'):
            op = self._avanzar()
            der = self._factor()
            columna_val = f"{columna_val} {op.value} {_nodo_a_str(der)}"
        return CalcularStmt(funcion=funcion.value, columna=columna_val)

    def _filtrar(self):
        """filtrar → FILTRAR condicion"""
        self._avanzar()
        cond = self._condicion()
        return FiltrarStmt(condicion=cond)

    def _ordenar(self):
        """ordenar → ORDENAR identificador (ASCENDENTE | DESCENDENTE)?"""
        self._avanzar()
        columna = self._esperar_id_o_objeto("Se esperaba el nombre de la columna")
        orden = ""
        if self._verificar('ASCENDENTE', 'DESCENDENTE'):
            orden = self._avanzar().value
        return OrdenarStmt(columna=columna.value, orden=orden)

    def _agrupar(self):
        """agrupar → AGRUPAR POR identificador"""
        self._avanzar()
        self._esperar('POR', "Se esperaba 'por' después de 'agrupar'")
        columna = self._esperar_id_o_objeto("Se esperaba el nombre de la columna")
        return AgruparStmt(columna=columna.value)

    def _graficar(self):
        """graficar → GRAFICAR tipo_grafica DE identificador (COMA identificador)?"""
        self._avanzar()
        if not self._verificar(*TIPOS_GRAFICA):
            raise ErrorSintactico("Se esperaba un tipo de gráfica", self._actual())
        tipo = self._avanzar()
        self._esperar('DE', "Se esperaba 'de' después del tipo de gráfica")
        columna = self._esperar_id_o_objeto("Se esperaba el nombre de la columna")
        columna_val = columna.value
        # Soporte para dos columnas separadas por coma (ej: dispersion de x, y)
        if self._verificar('COMA'):
            self._avanzar()
            segunda = self._esperar_id_o_objeto("Se esperaba la segunda columna")
            columna_val = f"{columna_val}, {segunda.value}"
        return GraficarStmt(tipo=tipo.value, columna=columna_val)

    def _exportar(self):
        """exportar → EXPORTAR CADENA"""
        self._avanzar()
        archivo = self._esperar('CADENA', "Se esperaba el nombre del archivo entre comillas")
        return ExportarStmt(archivo=archivo.value)

    def _asignacion(self):
        """asignacion → ID ASIGNAR expresion"""
        nombre = self._avanzar()
        self._esperar('ASIGNAR', "Se esperaba '=' después del identificador")
        expr = self._expresion()
        return AsignacionStmt(nombre=nombre.value, expresion=expr)

    # ── Expresiones y condiciones ──

    def _condicion(self):
        """condicion → (NO)? comparacion ((Y | O) (NO)? comparacion)*"""
        # Soporte para operador unario NO (ej: filtrar no reprobado)
        negado = False
        if self._verificar('NO'):
            self._avanzar()
            negado = True
        izq = self._comparacion()
        if negado:
            izq = CondicionCompuesta(izquierda=izq, operador_logico='no', derecha=None)
        while self._verificar('Y', 'O'):
            op = self._avanzar()
            negado_der = False
            if self._verificar('NO'):
                self._avanzar()
                negado_der = True
            der = self._comparacion()
            if negado_der:
                der = CondicionCompuesta(izquierda=der, operador_logico='no', derecha=None)
            izq = CondicionCompuesta(
                izquierda=izq, operador_logico=op.value, derecha=der
            )
        return izq

    def _comparacion(self):
        """comparacion → identificador (operador_relacional valor)?"""
        izq_token = self._esperar_id_o_objeto("Se esperaba un identificador en la condición")
        izq = Identificador(nombre=izq_token.value)
        # Si hay operador relacional, es una comparación completa
        if self._verificar(*OPS_RELACIONALES):
            op = self._avanzar()
            der = self._valor()
            return Condicion(izquierda=izq, operador=op.type, derecha=der)
        # Si no hay operador, se interpreta como condición booleana simple (ej: filtrar no reprobado)
        return Condicion(izquierda=izq, operador='BOOL', derecha=None)

    def _valor(self):
        """valor → ENTERO | FLOTANTE | CADENA | ID"""
        if self._verificar('ENTERO', 'FLOTANTE'):
            t = self._avanzar()
            return Literal(valor=t.value, tipo=t.type.lower())
        elif self._verificar('CADENA'):
            t = self._avanzar()
            return Literal(valor=t.value, tipo='cadena')
        elif self._verificar('ID'):
            t = self._avanzar()
            return Identificador(nombre=t.value)
        else:
            raise ErrorSintactico("Se esperaba un valor (número, cadena o identificador)", self._actual())

    def _expresion(self):
        """expresion → termino ((MAS | MENOS) termino)*"""
        izq = self._termino()
        while self._verificar('MAS', 'MENOS'):
            op = self._avanzar()
            der = self._termino()
            izq = ExpresionBinaria(izquierda=izq, operador=op.type, derecha=der)
        return izq

    def _termino(self):
        """termino → factor ((MULTIPLICAR | DIVIDIR | MODULO) factor)*"""
        izq = self._factor()
        while self._verificar('MULTIPLICAR', 'DIVIDIR', 'MODULO'):
            op = self._avanzar()
            der = self._factor()
            izq = ExpresionBinaria(izquierda=izq, operador=op.type, derecha=der)
        return izq

    def _factor(self):
        """factor → ENTERO | FLOTANTE | CADENA | ID | LPAREN expresion RPAREN"""
        if self._verificar('ENTERO', 'FLOTANTE'):
            t = self._avanzar()
            return Literal(valor=t.value, tipo=t.type.lower())
        elif self._verificar('CADENA'):
            t = self._avanzar()
            return Literal(valor=t.value, tipo='cadena')
        elif self._verificar('ID'):
            t = self._avanzar()
            return Identificador(nombre=t.value)
        elif self._consumir('LPAREN'):
            expr = self._expresion()
            self._esperar('RPAREN', "Se esperaba ')' para cerrar la expresión")
            return expr
        else:
            raise ErrorSintactico(
                "Se esperaba un valor o una expresión entre paréntesis",
                self._actual()
            )


def _nodo_a_str(nodo):
    """Convierte un nodo AST hoja a su representación como cadena."""
    if isinstance(nodo, Identificador):
        return nodo.nombre
    elif isinstance(nodo, Literal):
        return str(nodo.valor)
    return str(nodo)

