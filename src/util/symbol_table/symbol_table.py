from dataclasses import dataclass

from enum import StrEnum, auto
from src.rcc.ast.ast import DataType, Expression


class SymbolType(StrEnum):
    Variable = auto()


@dataclass
class Symbol:
    name: str
    sym_type: SymbolType
    data_type: DataType
    data_type_raw: str
    value_expr: Expression


@dataclass
class SymbolTable:
    __symbols: list[Symbol]

    def __init__(self) -> None:
        self.__symbols = []

    def new_symbol(
            self, 
            name: str, 
            data_type: DataType, 
            data_type_raw: str, 
            value_expr: Expression
        ) -> None:
        self.__symbols.append(Symbol(name, data_type, data_type_raw, value_expr))