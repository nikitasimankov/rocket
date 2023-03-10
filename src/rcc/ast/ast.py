from enum import StrEnum, auto
from dataclasses import dataclass

from src.rcc.token.token import TokenType

class DataType(StrEnum):
    I8 = auto()
    I16 = auto()
    I32 = auto()
    I64 = auto()
    U8 = auto()
    U16 = auto()
    U32 = auto()
    U64 = auto()
    F32 = auto()
    F64 = auto()
    Str = auto()
    Bool = auto()
    UserDefined = auto()

class NodeType(StrEnum):
    Statement = auto()
    Expression = auto()

class StatementType(StrEnum):
    VariableDeclaration = auto()

class ExpressionType(StrEnum):
    Literal = auto()
    VariableAccess = auto()

@dataclass
class Node:
    pos: tuple[int, int]
    node_type: NodeType

@dataclass
class Statement(Node):
    statement_Type: StatementType

@dataclass
class Expression(Node):
    expression_type: ExpressionType

@dataclass
class LiteralNode(Expression):
    literal_kind: TokenType
    literal_value: str

@dataclass
class VariableAccessNode(Expression):
    variable_name: str

@dataclass
class VariableDeclarationNode(Statement):
    variable_name: str
    variable_data_type: DataType
    variable_data_type_raw: str
    variable_value_expr: Expression