import networkx as nx
from networkx import Graph

from typing import Iterable

from .syntax import Cotree, Coproduct, Product, Unit


def modular_decomposition(graph: Graph) -> Iterable[Graph]:
    return (graph.subgraph(module).copy() for module in nx.connected_components(graph))


def parse(graph: Graph) -> Cotree:
    if len(graph.nodes()) == 1:
        return Unit(next(iter(graph.nodes)))

    if nx.is_connected(graph):
        return Product(*[parse(nx.complement(module)) for module in modular_decomposition(nx.complement(graph))])
    else:
        return Coproduct(*[parse(module) for module in modular_decomposition(graph)])
