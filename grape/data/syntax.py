from __future__ import annotations
from abc import ABC, abstractmethod

from typing import TypeVar, Generic, Any

Node = TypeVar('Node')


class Cograph(ABC, Generic[Node]):
    @abstractmethod
    def __repr__(self) -> str: ...

    def __mul__(self, other: Cograph[Node]) -> Cograph[Node]: return Product(self, other)
    def __add__(self, other: Cograph[Node]) -> Cograph[Node]: return Coproduct(self, other)


class Unit(Cograph[Node]):
    __match_args__ = ('content',)
    content: Node

    def __init__(self, content: Node) -> None:
        self.content = content

    def __repr__(self) -> str: return f'U({self.content})'
    def __eq__(self, other: Any) -> bool: return isinstance(other, Unit) and self.content == other.content
    def __hash__(self) -> int: return hash(self.content)


class Product(Cograph[Node]):
    __match_args__ = ('operands',)
    operands: tuple[Cograph, ...]

    def __init__(self, *operands: Cograph):
        if len(operands) <= 1:
            raise ValueError('A product must have at least two operands.')
        self.operands = sum(
            (flatten(operand) if isinstance(operand, (Unit, Product)) else (operand,) for operand in operands),
            ())

    def __repr__(self) -> str: return '⨂'.join(map(show, (a for a in self.operands)))


class Coproduct(Cograph[Node]):
    __match_args__ = ('operands',)
    operands: tuple[Cograph, ...]

    def __init__(self, *operands: Cograph):
        if len(operands) <= 1:
            raise ValueError('A coproduct must have at least two operands.')
        self.operands = sum(
            (flatten(operand) if isinstance(operand, (Unit, Coproduct)) else (operand,) for operand in operands),
            ())

    def __repr__(self) -> str: return '⨁'.join(map(show, (a for a in self.operands)))


def flatten(x: Cograph) -> tuple[Cograph, ...]:
    match x:
        case Unit(_): return (x,)
        case Product(operands) | Coproduct(operands): return operands
        case _: raise ValueError


def show(x: Cograph) -> str:
    return repr(x) if isinstance(x, Unit) else f'({repr(x)})'
