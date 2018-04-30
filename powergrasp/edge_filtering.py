"""Routines implementing edge filtering on input graphs,
knowing the bounds on the size of the motif to search in it.

All routines follow the following interface:
- arguments are the graph and the bounds
- yield valid edges as pairs of nodes

"""

import networkx as nx


def for_biclique(graph:nx.Graph, lowerbound:int, upperbound:int) -> [(str, str)]:
    """
    Remove any edge implying a node of degree 1, and a node of degree < lowerbound.
    """
    def ok_to_go(edge:tuple) -> bool:
        one, two = edge
        degone, degtwo = map(graph.degree, edge)
        return not any((
            degone == 1 and degtwo < lowerbound,
            degtwo == 1 and degone < lowerbound,
        ))
    for edge in graph.edges:
        if ok_to_go(edge):
            yield edge


def for_star(graph:nx.Graph, lowerbound:int, upperbound:int) -> [(str, str)]:
    """
    """
    def ok_to_go(edge:tuple) -> bool:
        one, two = edge
        degone, degtwo = map(graph.degree, edge)
        return not all((
            degone < lowerbound,
            degtwo < lowerbound,
        ))
    for edge in graph.edges:
        if ok_to_go(edge):
            yield edge


def for_clique(graph:nx.Graph, lowerbound:int, upperbound:int) -> [(str, str)]:
    """
    Remove an edge when one participating node has a clustering coefficient equal to 0.
    """
    clusterings = {}  # node -> clustering coefficient
    def clustering_of(node:str) -> float:
        if node in clusterings:
            return clusterings[node]
        else:
            return clusterings.setdefault(node, nx.clustering(graph, node))
    for edge in graph.edges:
        if all(clustering_of(node) > 0. for node in edge):
            yield edge
