from src.rcc.scanner.scanner import Scanner
from src.rcc.context.context import Context
from src.rcc.token.token import Token, TokenType
from src.rcc.ast.ast import (
    Node,
    DataType,
    NodeType,
    Statement,
    StatementType,
    Expression,
    ExpressionType,

    Literal,
    VarAccess,
    VarDeclaration
)

class Parser:
    ctx: Context
    tokens: list[Token]

    index: int
    token: Token

    def __init__(self, ctx: Context, scanner: Scanner) -> None:
        self.ctx = ctx
        self.tokens = scanner.scan()

        self.index = 0
        self.token = self.tokens[0]

    def next(self) -> None:
        self.index += 1
        self.token = self.tokens[self.index] if self.index < len(self.tokens) else None

    def parse(self) -> list[Node]:
        nodes: list[Node] = []

        while self.token is not None:
            nodes.append(self.parse_statement())

        return nodes

    def parse_statement(self) -> Statement:
        if self.token.matches_type(TokenType.Let):
            return self.parse_variable_decl()
        
    def parse_expression(self) -> Expression:
        if self.token.type in [TokenType.Int, TokenType.Float, TokenType.String]:
            token: Token = self.token
            self.next()
            return Literal(
                token.position,
                NodeType.Expression,
                ExpressionType.Literal,
                token.type,
                token.value,
            )
        elif self.token.matches_type(TokenType.Id):
            token: Token = self.token
            self.next()
            return VarAccess(
                token.position,
                NodeType.Expression,
                ExpressionType.VariableAccess,
                token.value
            )

    def parse_variable_decl(self) -> Statement:
        pos = self.token.position
        self.next()

        variable_name: str = ""
        variable_data_type: DataType = None
        variable_data_type_raw: str = ""
        variable_value_expr: Expression = None

        if not self.token.matches_type(TokenType.Id):
            self.ctx.error(self.token.position, f"invalid identifier '{self.token.value}'")
        else:
            variable_name = self.token.value
            self.next()

        if not self.token.matches_type(TokenType.Id):
            self.ctx.error(self.token.position, f"invalid data type '{self.token.value}'")
        else:
            (variable_data_type, variable_data_type_raw) = self.parse_data_type()
            self.next()

        if not self.token.matches_type(TokenType.Assign):
            self.ctx.error(self.token.position, f"expected '=', but got '{self.token.value}'")
        else:
            self.next()

        variable_value_expr = self.parse_expression()

        return VarDeclaration(
            pos,
            NodeType.Statement,
            StatementType.VariableDeclaration,
            variable_name,
            variable_data_type,
            variable_data_type_raw,
            variable_value_expr,
        )

    def parse_data_type(self) -> tuple[DataType, str]:
        match self.token.value:
            case "i8":
                return (DataType.I8, self.token.value)
            case "i16":
                return (DataType.I16, self.token.value)
            case "i32":
                return (DataType.I32, self.token.value)
            case "i64":
                return (DataType.I64, self.token.value)
            case "u8":
                return (DataType.U8, self.token.value)
            case "u16":
                return (DataType.U16, self.token.value)
            case "u32":
                return (DataType.U32, self.token.value)
            case "u64":
                return (DataType.U64, self.token.value)
            case "f32":
                return (DataType.F32, self.token.value)
            case "f64":
                return (DataType.F64, self.token.value)
            case "str":
                return (DataType.Str, self.token.value)
            case "bool":
                return (DataType.Bool, self.token.value)
            case _:
                return (DataType.UserDefined, self.token.value)

        

