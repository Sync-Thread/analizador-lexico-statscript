from typing import List, Any
from token_model import Token
from tokens import KEYWORD_LEXEMES


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.begin = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.position = 0
        self.keywords = KEYWORD_LEXEMES

    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            self.begin = self.current
            self.scan_token()

        self.add_token("EOF", "")
        return self.tokens

    def scan_token(self):
        c = self.advance()

        if c == ';':
            self.add_token("PUNTO_COMA")
        elif c == ',':
            self.add_token("COMA")
        elif c == '(':
            self.add_token("LPAREN")
        elif c == ')':
            self.add_token("RPAREN")

        elif c == '=':
            self.add_token("IGUAL" if self.match('=') else "ASIGNAR")
        elif c == '!':
            if self.match('='):
                self.add_token("DIFERENTE")
            else:
                self.add_error(c, "Símbolo no reconocido")
        elif c == '>':
            self.add_token("MAYOR_IGUAL" if self.match('=') else "MAYOR")
        elif c == '<':
            if self.match('='):
                self.add_token("MENOR_IGUAL")
            elif self.peek() == '-' and self.peek_next() == '-':
                self.advance()
                self.advance()
                self.block_comment()
            else:
                self.add_token("MENOR")

        elif c == '+':
            self.add_token("MAS")
        elif c == '-':
            if self.match('-'):
                self.line_comment()
            else:
                self.add_token("MENOS")
        elif c == '*':
            self.add_token("MULTIPLICAR")
        elif c == '/':
            self.add_token("DIVIDIR")
        elif c == '%':
            self.add_token("MODULO")

        elif c in ' \t\r':
            return
        elif c == '\n':
            self.add_token("NEWLINE")
            self.line += 1
            self.column = 1

        elif c == '"':
            self.string_literal()

        elif c.isdigit():
            self.number_literal()

        elif self.is_alpha(c):
            self.identifier()

        else:
            self.add_error(c, "Símbolo no reconocido")

    def add_token(self, token_type: str, value: Any = None):
        if value is None:
            value = self.source[self.begin:self.current]

        token = Token(
            type=token_type,
            value=value,
            line=self.line,
            column=self.token_start_column(),
            position=self.begin
        )
        self.tokens.append(token)

    def add_error(self, value: str, message: str):
        token = Token(
            type="ERROR",
            value=value,
            line=self.line,
            column=self.token_start_column(),
            position=self.begin,
            error_message=message
        )
        self.tokens.append(token)

    def token_start_column(self) -> int:
        i = self.begin - 1
        while i >= 0 and self.source[i] != '\n':
            i -= 1
        return self.begin - i

    def advance(self) -> str:
        if self.is_at_end():
            return '\0'
        ch = self.source[self.current]
        self.current += 1
        self.position = self.current
        self.column += 1
        return ch

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        self.position = self.current
        self.column += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def is_alpha(self, c: str) -> bool:
        return c.isalpha() or c == '_'

    def is_alnum(self, c: str) -> bool:
        return self.is_alpha(c) or c.isdigit()

    def line_comment(self):
        while self.peek() not in ('\n', '\0'):
            self.advance()

    def block_comment(self):
        while not self.is_at_end():
            if (self.peek() == '-' and self.peek_next() == '-'
                    and self.current + 2 < len(self.source)
                    and self.source[self.current + 2] == '>'):
                self.advance()
                self.advance()
                self.advance()
                return
            if self.peek() == '\n':
                self.line += 1
                self.column = 1
            self.advance()
        self.add_error(self.source[self.begin:self.current], "Comentario de bloque sin cerrar")

    def string_literal(self):
        while self.peek() not in ('"', '\n', '\0'):
            self.advance()

        if self.peek() == '"':
            self.advance()
            raw = self.source[self.begin:self.current]
            self.add_token("CADENA", raw[1:-1])
        else:
            self.add_error(self.source[self.begin:self.current], "Cadena sin cerrar")

    def number_literal(self):
        while self.peek().isdigit():
            self.advance()

        is_float = False
        if self.peek() == '.' and self.peek_next().isdigit():
            is_float = True
            self.advance()
            while self.peek().isdigit():
                self.advance()

        if self.is_alpha(self.peek()):
            while self.is_alnum(self.peek()):
                self.advance()
            raw = self.source[self.begin:self.current]
            self.add_error(raw, "Identificador inválido")
            return

        raw = self.source[self.begin:self.current]
        if is_float:
            self.add_token("FLOTANTE", float(raw))
        else:
            self.add_token("ENTERO", int(raw))

    def identifier(self):
        while self.is_alnum(self.peek()):
            self.advance()

        text = self.source[self.begin:self.current]
        key = text.lower()

        token_type = self.keywords.get(key)
        if token_type is not None:
            self.add_token(token_type, text)
        else:
            self.add_token("ID", text)
