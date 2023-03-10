from enum import StrEnum, auto

class TokenType(StrEnum):
    EOF = auto()
    Invalid = auto()

    Id = auto()
    Int = auto()
    Float = auto()
    String = auto()

    Inc = auto() # ++
    Dec = auto() # --
    Dot = auto() # .
    Comma = auto() # ,

    Add = auto() # +
    Sub = auto() # - 
    Mul = auto() # *
    Div = auto() # / 
    Rem = auto() # %
    Colon = auto() # :
    Assign = auto() # =
    AddAssign = auto() # +=
    SubAssign = auto() # -=
    MulAssign = auto() # *=
    DivAssign = auto() # /=
    RemAssign = auto() # %=

    Or = auto() # |
    Xor = auto() # ^
    And = auto() # &
    Not = auto() # !
    LOr = auto() # ||
    LAnd = auto() # &&

    Equal = auto() # ==
    NotEqual = auto() # !=
    LessThan = auto() # <
    GreaterThan = auto() # >
    LessThanEqual = auto() # <=
    GreaterThanEqual = auto() # >=

    LPar = auto() # (
    RPar = auto() # )
    LBrack = auto() # [
    RBrack = auto() # ]
    LBrace = auto() # {
    RBrace = auto() # }

    # Keywords
    Let = auto()

class Token:
    type: TokenType
    value: str
    position: tuple[int, int]

    def __init__(self, line: int, column: int, type: TokenType, value: str) -> None:
        self.type = type
        self.value = value
        self.position = (line, column)

    def matches(self, type: TokenType, value: str) -> bool:
        return self.type == type and self.value == value
    
    def matches_type(self, type: TokenType) -> bool:
        return self.type == type

    def matches_value(self, value: str) -> bool:
        return self.value == value