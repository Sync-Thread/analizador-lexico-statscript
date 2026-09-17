from dataclasses import dataclass
from typing import Any

from tokens import (
    TOKEN_TYPES,
    ALL_TOKEN_TYPES,
    COMMANDS,
    STAT_FUNCTIONS,
    CHART_TYPES,
    PREPOSITIONS,
    MODIFIERS,
    LOGICAL_OPERATORS,
    LANGUAGE_OBJECTS,
    RELATIONAL_OPERATORS,
    ARITHMETIC_OPERATORS,
    ASSIGNMENTS,
    LITERALS,
    IDENTIFIERS,
    SEPARATORS,
    OTHERS,
)


@dataclass
class Token:
    type: str
    value: Any
    line: int
    column: int
    position: int
    error_message: str = None

    def __str__(self) -> str:
        return f"Token({self.type}, {repr(self.value)}, linea={self.line}, col={self.column})"

    def __repr__(self) -> str:
        return (
            f"Token(type={self.type}, value={self.value!r}, "
            f"linea={self.line}, columna={self.column}, posicion={self.position})"
        )

    def __eq__(self, other) -> bool:
        return isinstance(other, Token) and self.type == other.type and self.value == other.value

    def is_(self, token_type: str, *, validate: bool = False) -> bool:
        if validate and token_type not in ALL_TOKEN_TYPES:
            raise ValueError(f"Token type inválido: {token_type!r}")
        return self.type == token_type

    def is_type(self, token_type: str) -> bool:
        return self.type == token_type

    def is_any(self, *token_types: str, validate: bool = False) -> bool:
        if validate:
            invalid = [t for t in token_types if t not in ALL_TOKEN_TYPES]
            if invalid:
                raise ValueError(f"Token types inválidos: {invalid!r}")
        return self.type in token_types

    def is_valid_type(self) -> bool:
        return self.type in ALL_TOKEN_TYPES

    def has_value(self, value: Any) -> bool:
        return self.value == value

    def matches(self, token_type: str, value: Any = None) -> bool:
        if value is None:
            return self.is_(token_type)
        return self.is_(token_type) and self.has_value(value)

    # Categorías

    def is_command(self) -> bool: return self.type in COMMANDS
    def is_stat_function(self) -> bool: return self.type in STAT_FUNCTIONS
    def is_chart_type(self) -> bool: return self.type in CHART_TYPES
    def is_preposition(self) -> bool: return self.type in PREPOSITIONS
    def is_modifier(self) -> bool: return self.type in MODIFIERS
    def is_logical_operator(self) -> bool: return self.type in LOGICAL_OPERATORS
    def is_language_object(self) -> bool: return self.type in LANGUAGE_OBJECTS
    def is_relational_operator(self) -> bool: return self.type in RELATIONAL_OPERATORS
    def is_arithmetic_operator(self) -> bool: return self.type in ARITHMETIC_OPERATORS
    def is_assignment(self) -> bool: return self.type in ASSIGNMENTS
    def is_literal(self) -> bool: return self.type in LITERALS
    def is_id(self) -> bool: return self.type in IDENTIFIERS
    def is_separator(self) -> bool: return self.type in SEPARATORS
    def is_other(self) -> bool: return self.type in OTHERS

    # Comandos
    def is_cargar(self) -> bool: return self.is_("CARGAR")
    def is_mostrar(self) -> bool: return self.is_("MOSTRAR")
    def is_calcular(self) -> bool: return self.is_("CALCULAR")
    def is_filtrar(self) -> bool: return self.is_("FILTRAR")
    def is_ordenar(self) -> bool: return self.is_("ORDENAR")
    def is_agrupar(self) -> bool: return self.is_("AGRUPAR")
    def is_graficar(self) -> bool: return self.is_("GRAFICAR")
    def is_exportar(self) -> bool: return self.is_("EXPORTAR")

    # Funciones estadísticas
    def is_promedio(self) -> bool: return self.is_("PROMEDIO")
    def is_mediana(self) -> bool: return self.is_("MEDIANA")
    def is_moda(self) -> bool: return self.is_("MODA")
    def is_desviacion(self) -> bool: return self.is_("DESVIACION")
    def is_varianza(self) -> bool: return self.is_("VARIANZA")
    def is_conteo(self) -> bool: return self.is_("CONTEO")
    def is_suma(self) -> bool: return self.is_("SUMA")
    def is_minimo(self) -> bool: return self.is_("MINIMO")
    def is_maximo(self) -> bool: return self.is_("MAXIMO")
    def is_correlacion(self) -> bool: return self.is_("CORRELACION")

    # Tipos de gráfica
    def is_barras(self) -> bool: return self.is_("BARRAS")
    def is_lineas(self) -> bool: return self.is_("LINEAS")
    def is_pastel(self) -> bool: return self.is_("PASTEL")
    def is_dispersion(self) -> bool: return self.is_("DISPERSION")
    def is_histograma(self) -> bool: return self.is_("HISTOGRAMA")

    # Preposiciones
    def is_de(self) -> bool: return self.is_("DE")
    def is_por(self) -> bool: return self.is_("POR")

    # Modificadores
    def is_ascendente(self) -> bool: return self.is_("ASCENDENTE")
    def is_descendente(self) -> bool: return self.is_("DESCENDENTE")

    # Operadores lógicos
    def is_y(self) -> bool: return self.is_("Y")
    def is_o(self) -> bool: return self.is_("O")
    def is_no(self) -> bool: return self.is_("NO")

    # Objetos del lenguaje
    def is_datos(self) -> bool: return self.is_("DATOS")
    def is_columnas(self) -> bool: return self.is_("COLUMNAS")
    def is_registros(self) -> bool: return self.is_("REGISTROS")

    # Operadores relacionales
    def is_mayor(self) -> bool: return self.is_("MAYOR")
    def is_menor(self) -> bool: return self.is_("MENOR")
    def is_mayor_igual(self) -> bool: return self.is_("MAYOR_IGUAL")
    def is_menor_igual(self) -> bool: return self.is_("MENOR_IGUAL")
    def is_igual(self) -> bool: return self.is_("IGUAL")
    def is_diferente(self) -> bool: return self.is_("DIFERENTE")

    # Operadores aritméticos
    def is_mas(self) -> bool: return self.is_("MAS")
    def is_menos(self) -> bool: return self.is_("MENOS")
    def is_multiplicar(self) -> bool: return self.is_("MULTIPLICAR")
    def is_dividir(self) -> bool: return self.is_("DIVIDIR")
    def is_modulo(self) -> bool: return self.is_("MODULO")

    # Literales
    def is_entero(self) -> bool: return self.is_("ENTERO")
    def is_flotante(self) -> bool: return self.is_("FLOTANTE")
    def is_cadena(self) -> bool: return self.is_("CADENA")

    # Separadores
    def is_punto_coma(self) -> bool: return self.is_("PUNTO_COMA")
    def is_coma(self) -> bool: return self.is_("COMA")
    def is_lparen(self) -> bool: return self.is_("LPAREN")
    def is_rparen(self) -> bool: return self.is_("RPAREN")

    # Otros
    def is_newline(self) -> bool: return self.is_("NEWLINE")
    def is_error(self) -> bool: return self.is_("ERROR")
    def is_eof(self) -> bool: return self.is_("EOF")
