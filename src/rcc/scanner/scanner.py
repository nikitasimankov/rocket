from src.rcc.context.context import Context
from src.rcc.token.token import Token, TokenType

operators: dict = {
    "+": TokenType.Add,
    "-": TokenType.Sub,
    "*": TokenType.Mul,
    "/": TokenType.Div,
    "%": TokenType.Rem,
    ".": TokenType.Dot,
    ",": TokenType.Comma,
    ":": TokenType.Colon,
    "=": TokenType.Assign,

    "++": TokenType.Inc,
    "--": TokenType.Dec,
    "+=": TokenType.AddAssign,
    "-=": TokenType.SubAssign,
    "*=": TokenType.MulAssign,
    "/=": TokenType.DivAssign,
    "%=": TokenType.RemAssign,

    "|": TokenType.Or,
    "&": TokenType.And,
    "!": TokenType.Not,
    "||": TokenType.LOr,
    "&&": TokenType.LAnd,

    "<": TokenType.LessThan,
    ">": TokenType.GreaterThan,

    "==": TokenType.Equal,
    "!=": TokenType.NotEqual,
    "<=": TokenType.LessThanEqual, 
    ">=": TokenType.GreaterThanEqual,

    "(": TokenType.LPar,
    ")": TokenType.RPar,
    "[": TokenType.LBrack,
    "]": TokenType.RBrack,
    "{": TokenType.LBrace,
    "}": TokenType.RBrace,
}

keywords: dict = {
    "let": TokenType.Let,
}

class Scanner:
    line: int
    index: int
    column: int

    char: str
    input: str
    ctx: Context

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx
        self.input = ctx.content

        self.line = 0
        self.index = 0
        self.column = 0
        self.char = self.input[self.index]

    def scan(self) -> list[Token]:
        tokens: list[Token] = []

        while self.char != "":
            if self.is_digit():
                tokens.append(self.scan_number())
            elif self.is_letter() or self.char == '_':
                tokens.append(self.scan_id())
            elif self.is_operator():
                tokens.append(self.scan_operator())
            elif self.char == '"':
                tokens.append(self.scan_string())
            elif self.char in ' \t\r\n':
                self.next()
            else:
                self.ctx.error((self.line, self.column), f"invalid character '{self.char}'")

        return tokens

    def next(self) -> None:
        self.index += 1
        self.column += 1

        if self.char == '\n':
            self.line += 1
            self.column = 0

        if self.index >= len(self.input):
            self.char = ""
        else:
            self.char = self.input[self.index]

    def is_digit(self) -> bool:
        digits = "0123456789"

        return self.char in digits
    
    def is_letter(self) -> bool:
        letters = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"

        return self.char in letters
    
    def is_operator(self) -> bool:
        operator_chars = "+-*/%:=|^&!<>()[]{}.,"

        return self.char in operator_chars

    def scan_id(self) -> Token:
        index = self.index
        line, column = self.line, self.column

        while self.char != "" and (
            self.is_letter() or self.is_digit() or self.char == '_'
        ):
            self.next()

        id: str = self.input[index:self.index]

        try:
            kw: TokenType = keywords[id]
            return Token(line, column, kw, id)
        except KeyError:
            return Token(line, column, TokenType.Id, id)

    def scan_number(self) -> Token:
        is_float = False
        index = self.index
        line, column = self.line, self.column

        while self.char != "" and (self.is_digit() or self.char == '.'):
            if self.char == '.':
                is_float = True

            self.next()

        number: str = self.input[index:self.index]

        if is_float:
            return Token(line, column, TokenType.Float, number)
        
        return Token(line, column, TokenType.Int, number)
    
    def scan_string(self) -> Token:
        index = self.index
        line, column = self.line, self.column

        self.next()

        while self.char != "" and self.char != '"':
            self.next()

        string: str = self.input[index + 1:self.index]
        self.next() # Skip the closing double quote

        return Token(line, column, TokenType.String, string)
    
    def scan_operator(self) -> Token:
        line, column = self.line, self.column

        char_1: str = self.char
        self.next()

        if char_1 + self.char in [
            "++", "--", "+=", "-=", 
            "*=", "/=", "%=", "==", 
            "!=", "||", "&&", "<=", 
            ">="
        ]:
            char = self.char
            self.next()

            op_type: TokenType = operators[char_1 + char]
            return Token(line, column, op_type, char_1 + char)
        
        op_type: TokenType = operators[char_1]
        return Token(line, column, op_type, char_1)

