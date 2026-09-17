# Reglas léxicas de StatScript
# Aquí defino las expresiones regulares que el scanner usa para
# reconocer cada tipo de token. El scanner (src/scanner.py) aplica
# estas mismas reglas pero de forma manual, carácter por carácter.

import re

# El orden importa: primero los patrones más específicos,
# luego los más generales. Así evito que, por ejemplo,
# un entero se confunda con la parte entera de un flotante.
#
# Prioridad:
#   1. Espacios y comentarios (los ignoro, no generan token)
#   2. Cadenas de texto
#   3. Flotantes antes que enteros
#   4. Identificadores / palabras clave
#   5. Operadores de dos caracteres (>=, <=, ==, !=)
#   6. Operadores de un carácter (+, -, *, /, %, =, >, <)
#   7. Delimitadores (; , ( ))
#   8. Cualquier otra cosa → ERROR

RULES = {
    # Cosas que simplemente descarto
    "WHITESPACE":       re.compile(r'[ \t\r]+'),
    "LINE_COMMENT":     re.compile(r'--[^\n]*'),
    "BLOCK_COMMENT":    re.compile(r'<--.*?-->', re.DOTALL),

    # Literales de valor
    "FLOTANTE":         re.compile(r'\d+\.\d+'),
    "ENTERO":           re.compile(r'\d+'),
    "CADENA":           re.compile(r'"[^"]*"'),

    # Identificadores: letra o '_' al inicio, luego letras/dígitos/'_'
    "IDENTIFIER":       re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*'),

    # Operadores de dos caracteres (van antes que los de uno solo)
    "MAYOR_IGUAL":      re.compile(r'>='),
    "MENOR_IGUAL":      re.compile(r'<='),
    "IGUAL":            re.compile(r'=='),
    "DIFERENTE":        re.compile(r'!='),

    # Operadores aritméticos y de comparación simples
    "MAS":              re.compile(r'\+'),
    "MENOS":            re.compile(r'-'),
    "MULTIPLICAR":      re.compile(r'\*'),
    "DIVIDIR":          re.compile(r'/'),
    "MODULO":           re.compile(r'%'),
    "ASIGNAR":          re.compile(r'='),
    "MAYOR":            re.compile(r'>'),
    "MENOR":            re.compile(r'<'),

    # Delimitadores
    "PUNTO_COMA":       re.compile(r';'),
    "COMA":             re.compile(r','),
    "LPAREN":           re.compile(r'\('),
    "RPAREN":           re.compile(r'\)'),
}

# Cuando el scanner lee un IDENTIFIER, revisa si está en esta lista.
# Si coincide (sin importar mayúsculas), lo reclasifica como palabra clave.
KEYWORDS = {
    # Comandos principales
    "cargar":       "CARGAR",
    "mostrar":      "MOSTRAR",
    "calcular":     "CALCULAR",
    "filtrar":      "FILTRAR",
    "ordenar":      "ORDENAR",
    "agrupar":      "AGRUPAR",
    "graficar":     "GRAFICAR",
    "exportar":     "EXPORTAR",

    # Funciones estadísticas
    "promedio":     "PROMEDIO",
    "mediana":      "MEDIANA",
    "moda":         "MODA",
    "desviacion":   "DESVIACION",
    "varianza":     "VARIANZA",
    "conteo":       "CONTEO",
    "suma":         "SUMA",
    "minimo":       "MINIMO",
    "maximo":       "MAXIMO",
    "correlacion":  "CORRELACION",

    # Tipos de gráfica
    "barras":       "BARRAS",
    "lineas":       "LINEAS",
    "pastel":       "PASTEL",
    "dispersion":   "DISPERSION",
    "histograma":   "HISTOGRAMA",

    # Preposiciones
    "de":           "DE",
    "por":          "POR",

    # Modificadores de orden
    "ascendente":   "ASCENDENTE",
    "descendente":  "DESCENDENTE",

    # Operadores lógicos
    "y":            "Y",
    "o":            "O",
    "no":           "NO",

    # Objetos del lenguaje
    "datos":        "DATOS",
    "columnas":     "COLUMNAS",
    "registros":    "REGISTROS",
}

# Patrón para detectar identificadores mal formados:
# cualquier cosa que empiece con dígitos y luego tenga letras, como 123abc o 3var
INVALID_IDENTIFIER = re.compile(r'\d+[a-zA-Z_][a-zA-Z0-9_]*')

# Todo lo que no encaje en ninguna regla de arriba se reporta como error léxico.
# Ejemplos de símbolos inválidos en StatScript: $, @, #, ~, `, \
