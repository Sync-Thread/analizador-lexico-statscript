# StatScript — Analizador Léxico

Analizador léxico y sintáctico para **StatScript**, un lenguaje personalizado diseñado para el análisis estadístico de datos tabulares (CSV).

---

## Información del Curso

| Campo           | Valor                              |
| --------------- | ---------------------------------- |
| **Materia**     | Programación de Sistemas de Base I |
| **Institución** | Universidad Autónoma de Tamaulipas |
| **Semestre**    | 8vo Semestre                       |
| **Profesor**    | Muñoz Quintero Dante Adolfo        |

## Integrantes del Equipo

| Nombre                          | Matrícula  |
| ------------------------------- | ---------- |
| Cabrales Cruz Raciel Julian     | 2223330141 |
| Guzmán Sánchez Alex Arath       | 2223330162 |
| Muñoz Perales Luis Gonzalo      | 2193283019 |
| Saenz Rico Perez Marco Fernando | 2223330190 |

---

## Descripción del Lenguaje

**StatScript** es un lenguaje de dominio específico (DSL) orientado al análisis estadístico de datos tabulares. Permite cargar archivos CSV, calcular métricas estadísticas (promedio, mediana, moda, desviación estándar, etc.), filtrar y ordenar registros, agrupar datos por categorías, y generar gráficas de distintos tipos.

### Características principales

- Sintaxis en español, intuitiva y declarativa
- 8 comandos principales: `cargar`, `mostrar`, `calcular`, `filtrar`, `ordenar`, `agrupar`, `graficar`, `exportar`
- 10 funciones estadísticas integradas
- 5 tipos de gráficas: `barras`, `lineas`, `pastel`, `dispersion`, `histograma`
- Operadores relacionales, aritméticos y lógicos
- Comentarios de línea (`--`) y de bloque (`<-- ... -->`)
- Literales: enteros, flotantes y cadenas de texto
- Parser recursivo descendente con generación de AST (propuesta actual, no definitiva)

### Ejemplo de código StatScript

```
-- Análisis de ventas trimestrales
cargar "ventas_2024.csv";

calcular promedio de precio;
calcular desviacion de precio;

filtrar precio > 100 y categoria == "electrónica";
ordenar precio descendente;
agrupar por departamento;

graficar barras de ventas;
exportar "reporte_final.csv";
```

---

## Tokens Reconocidos

| Categoría                   | Tokens                                                                                                       | Patrón / Descripción                            |
| --------------------------- | ------------------------------------------------------------------------------------------------------------ | ----------------------------------------------- |
| **Comandos**                | `cargar`, `mostrar`, `calcular`, `filtrar`, `ordenar`, `agrupar`, `graficar`, `exportar`                     | Palabras reservadas — instrucciones principales |
| **Funciones estadísticas**  | `promedio`, `mediana`, `moda`, `desviacion`, `varianza`, `conteo`, `suma`, `minimo`, `maximo`, `correlacion` | Palabras reservadas — cálculos estadísticos     |
| **Tipos de gráfica**        | `barras`, `lineas`, `pastel`, `dispersion`, `histograma`                                                     | Palabras reservadas — visualizaciones           |
| **Preposiciones**           | `de`, `por`                                                                                                  | Palabras reservadas — conectores sintácticos    |
| **Modificadores**           | `ascendente`, `descendente`                                                                                  | Palabras reservadas — orden de clasificación    |
| **Operadores lógicos**      | `y`, `o`, `no`                                                                                               | Palabras reservadas — operadores booleanos      |
| **Objetos del lenguaje**    | `datos`, `columnas`, `registros`                                                                             | Palabras reservadas — elementos referenciables  |
| **Operadores aritméticos**  | `+`, `-`, `*`, `/`, `%`                                                                                      | Operaciones matemáticas                         |
| **Operadores relacionales** | `>`, `<`, `>=`, `<=`, `==`, `!=`                                                                             | Comparaciones                                   |
| **Asignación**              | `=`                                                                                                          | Asignación de valores                           |
| **Delimitadores**           | `;`, `,`, `(`, `)`                                                                                           | Separadores y agrupadores                       |
| **Literales**               | Enteros, flotantes, cadenas (`"..."`)                                                                        | `\d+`, `\d+\.\d+`, `"[^"]*"`                    |
| **Identificadores**         | Nombres de variables/columnas                                                                                | `[a-zA-Z_][a-zA-Z0-9_]*`                        |
| **Comentarios**             | Línea: `--`, Bloque: `<-- ... -->`                                                                           | Se descartan (no generan tokens)                |

---

## Cómo Ejecutar

### Requisitos

- Python 3.10 o superior
- Sin dependencias externas

### Modo archivo (recomendado)

```bash
python src/main.py <archivo.sts>
```

### Modo interactivo

```bash
python src/main.py
```

Escribe tu código StatScript y presiona Enter en una línea vacía para analizar.

> **Nota:** El analizador sintáctico (parser) es una propuesta actual que se encuentra en fase de desarrollo. Su objetivo es validar la estructura de las sentencias y generar un árbol de sintaxis abstracta (AST), pero su implementación podría ajustarse en futuras iteraciones del proyecto.

---

## Ejemplos de Uso

### Entrada válida (`tests/valid/programa1.sts`)

```
cargar "ventas_2024.csv";
calcular promedio de precio;
filtrar precio > 100 y categoria == "electrónica";
ordenar precio descendente;
graficar barras de ventas;
exportar "reporte_ventas.csv";
```

### Salida esperada

```
Token List:
  1: (CARGAR, 'cargar')
  2: (CADENA, 'ventas_2024.csv')
  3: (PUNTO_COMA, ';')
  4: (CALCULAR, 'calcular')
  5: (PROMEDIO, 'promedio')
  6: (DE, 'de')
  7: (ID, 'precio')
  8: (PUNTO_COMA, ';')
  ...

Error List:
  Sin errores léxicos.
```

Si no se detectan errores léxicos, el sistema genera además el Árbol de Sintaxis Abstracta (AST):

```
Análisis Sintáctico (AST):

Programa
  CargarStmt(archivo="ventas_2024.csv")
  CalcularStmt(funcion="promedio", columna="precio")
  FiltrarStmt
    CondicionCompuesta(op="Y")
      Condicion(precio > 100)
      Condicion(categoria == 'electrónica')
  OrdenarStmt(columna="precio", orden="descendente")
  GraficarStmt(tipo="barras", columna="ventas")
  ExportarStmt(archivo="reporte_ventas.csv")

Error List (sintácticos):
  Sin errores sintácticos.
```

### Entrada con errores (`tests/invalid/errores1.sts`)

```
cargar $datos;
filtrar @edad > 30;
calcular #promedio de salario;
```

### Salida esperada

```
Token List:
  1: (CARGAR, 'cargar')
  2: (DATOS, 'datos')
  3: (PUNTO_COMA, ';')
  ...

Error List:
  Linea 5, Columna 8: Símbolo no reconocido '$'
  Linea 6, Columna 9: Símbolo no reconocido '@'
  Linea 7, Columna 10: Símbolo no reconocido '#'
```

---

## Estructura del Proyecto

```
analizador-lexico-statscript/
├── README.md
├── .gitignore
├── LICENSE
├── src/
│   ├── main.py              ← punto de entrada / ejecutable principal
│   ├── scanner.py           ← lógica central del analizador léxico
│   ├── tokens.py            ← definición de tipos de token y palabras reservadas
│   ├── token_model.py       ← modelo de datos del token y manejo de errores
│   ├── ast_nodes.py         ← nodos del árbol de sintaxis abstracta (AST)
│   └── parser.py            ← analizador sintáctico recursivo descendente
├── grammar/
│   └── statscript_rules.py  ← reglas léxicas formales
├── tests/
│   ├── valid/
│   │   ├── programa1.sts    ← programa válido (análisis de ventas)
│   │   └── programa2.sts    ← programa válido (análisis académico)
│   └── invalid/
│       ├── errores1.sts     ← errores: símbolos no reconocidos
│       └── errores2.sts     ← errores: IDs inválidos, cadenas/comentarios sin cerrar
├── docs/
│   └── entregable_final.pdf
└── capturas/
    └── captura01.png ... N
```
