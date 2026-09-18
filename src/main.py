import sys
from scanner import Scanner
from parser import Parser, ErrorSintactico
from ast_nodes import imprimir_ast


def print_tokens(tokens):
    """Imprime la lista de tokens numerada, excluyendo errores, NEWLINE y EOF."""
    valid = [t for t in tokens if not t.is_error() and not t.is_newline() and not t.is_eof()]
    if not valid:
        print("  (sin tokens)")
        return
    for i, token in enumerate(valid, 1):
        print(f"  {i}: ({token.type}, {token.value!r})")


def print_errors(tokens):
    """Imprime la lista de errores léxicos con línea, columna y descripción."""
    errors = [t for t in tokens if t.is_error()]
    if not errors:
        print("  Sin errores léxicos.")
        return
    for error in errors:
        msg = error.error_message or "Símbolo no reconocido"
        print(f"  Linea {error.line}, Columna {error.column}: {msg} {error.value!r}")


def print_parser_errors(errores):
    """Imprime la lista de errores sintácticos detectados por el parser."""
    if not errores:
        print("  Sin errores sintácticos.")
        return
    for error in errores:
        print(f"  {error}")


def analyze(source, label=""):
    """Ejecuta el análisis léxico y sintáctico, mostrando resultados."""
    print(f"\n{'=' * 60}")
    if label:
        print(f" Archivo: {label}")
    print(f" Resultado del análisis")
    print(f"{'=' * 60}")

    # Fase 1: Análisis léxico
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    print("\nToken List:")
    print_tokens(tokens)

    print(f"\n{'-' * 60}")
    print("Error List (léxicos):")
    print_errors(tokens)

    # Fase 2: Análisis sintáctico
    lexer_errors = [t for t in tokens if t.is_error()]
    if not lexer_errors:
        print(f"\n{'-' * 60}")
        print("Análisis Sintáctico (AST):")

        parser = Parser(tokens)
        ast = parser.parse()

        if parser.tiene_errores():
            print("\n  Errores sintácticos encontrados:")
            print_parser_errors(parser.errores)
            print(f"\n  >> No se pudo generar el árbol sintáctico debido a errores sintácticos.")
        else:
            print()
            imprimir_ast(ast)
            print(f"\n  >> Árbol sintáctico generado exitosamente.")

        print(f"\n{'-' * 60}")
        print("Error List (sintácticos):")
        print_parser_errors(parser.errores)
    else:
        print(f"\n{'-' * 60}")
        print("Análisis Sintáctico (AST):")
        print("  Se omite el análisis sintáctico debido a errores léxicos.")
        print(f"\n  >> No se pudo generar el árbol sintáctico debido a errores léxicos.")


def main():
    if len(sys.argv) > 1:
        # Modo archivo
        filepath = sys.argv[1]
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                source = f.read()
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo '{filepath}'")
            sys.exit(1)
        except IOError as e:
            print(f"Error al leer el archivo: {e}")
            sys.exit(1)
        analyze(source, label=filepath)
    else:
        # Modo interactivo
        print("StatScript — Analizador Léxico y Sintáctico")
        print("Escribe tu programa StatScript (línea vacía para analizar):\n")

        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if line == "":
                break
            lines.append(line)

        source = "\n".join(lines)
        analyze(source)


if __name__ == "__main__":
    main()
