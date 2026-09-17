COMMANDS = frozenset({
    'CARGAR',
    'MOSTRAR',
    'CALCULAR',
    'FILTRAR',
    'ORDENAR',
    'AGRUPAR',
    'GRAFICAR',
    'EXPORTAR',
})

STAT_FUNCTIONS = frozenset({
    'PROMEDIO',
    'MEDIANA',
    'MODA',
    'DESVIACION',
    'VARIANZA',
    'CONTEO',
    'SUMA',
    'MINIMO',
    'MAXIMO',
    'CORRELACION',
})

CHART_TYPES = frozenset({
    'BARRAS',
    'LINEAS',
    'PASTEL',
    'DISPERSION',
    'HISTOGRAMA',
})

PREPOSITIONS = frozenset({
    'DE',
    'POR',
})

MODIFIERS = frozenset({
    'ASCENDENTE',
    'DESCENDENTE',
})

LOGICAL_OPERATORS = frozenset({
    'Y',
    'O',
    'NO',
})

LANGUAGE_OBJECTS = frozenset({
    'DATOS',
    'COLUMNAS',
    'REGISTROS',
})

RELATIONAL_OPERATORS = frozenset({
    'MAYOR',
    'MENOR',
    'MAYOR_IGUAL',
    'MENOR_IGUAL',
    'IGUAL',
    'DIFERENTE',
})

ARITHMETIC_OPERATORS = frozenset({
    'MAS',
    'MENOS',
    'MULTIPLICAR',
    'DIVIDIR',
    'MODULO',
})

ASSIGNMENTS = frozenset({
    'ASIGNAR',
})

LITERALS = frozenset({
    'ENTERO',
    'FLOTANTE',
    'CADENA',
})

IDENTIFIERS = frozenset({
    'ID',
})

SEPARATORS = frozenset({
    'PUNTO_COMA',
    'COMA',
    'LPAREN',
    'RPAREN',
})

OTHERS = frozenset({
    'NEWLINE',
    'ERROR',
    'EOF',
})

# Mapeo centralizado: lexema en minúsculas -> tipo de token.
# El Scanner usa este diccionario para reconocer palabras reservadas automáticamente.
KEYWORD_LEXEMES = {
    'cargar': 'CARGAR',
    'mostrar': 'MOSTRAR',
    'calcular': 'CALCULAR',
    'filtrar': 'FILTRAR',
    'ordenar': 'ORDENAR',
    'agrupar': 'AGRUPAR',
    'graficar': 'GRAFICAR',
    'exportar': 'EXPORTAR',
    'promedio': 'PROMEDIO',
    'mediana': 'MEDIANA',
    'moda': 'MODA',
    'desviacion': 'DESVIACION',
    'varianza': 'VARIANZA',
    'conteo': 'CONTEO',
    'suma': 'SUMA',
    'minimo': 'MINIMO',
    'maximo': 'MAXIMO',
    'correlacion': 'CORRELACION',
    'barras': 'BARRAS',
    'lineas': 'LINEAS',
    'pastel': 'PASTEL',
    'dispersion': 'DISPERSION',
    'histograma': 'HISTOGRAMA',
    'de': 'DE',
    'por': 'POR',
    'ascendente': 'ASCENDENTE',
    'descendente': 'DESCENDENTE',
    'y': 'Y',
    'o': 'O',
    'no': 'NO',
    'datos': 'DATOS',
    'columnas': 'COLUMNAS',
    'registros': 'REGISTROS',
}

TOKEN_TYPES = {
    'COMMANDS': COMMANDS,
    'STAT_FUNCTIONS': STAT_FUNCTIONS,
    'CHART_TYPES': CHART_TYPES,
    'PREPOSITIONS': PREPOSITIONS,
    'MODIFIERS': MODIFIERS,
    'LOGICAL_OPERATORS': LOGICAL_OPERATORS,
    'LANGUAGE_OBJECTS': LANGUAGE_OBJECTS,
    'RELATIONAL_OPERATORS': RELATIONAL_OPERATORS,
    'ARITHMETIC_OPERATORS': ARITHMETIC_OPERATORS,
    'ASSIGNMENTS': ASSIGNMENTS,
    'LITERALS': LITERALS,
    'IDENTIFIERS': IDENTIFIERS,
    'SEPARATORS': SEPARATORS,
    'OTHERS': OTHERS,
}

ALL_TOKEN_TYPES = frozenset().union(*TOKEN_TYPES.values())
