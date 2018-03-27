import phasme
import networkx
from collections import defaultdict

from motif import Motif

class Graph:
    """A graph object, exposing some data on it.

    Note that a data is computed during its first access.

    """
    def __init__(self, graph:str or networkx.Graph):
        if isinstance(graph, networkx.Graph):
            nxgraph = networkx.Graph(graph)
        elif isinstance(graph, str):
            nxgraph = phasme.build_graph.graph_from_file(graph)
        else:
            raise ValueError("Unexpected {}".format(graph))
        # data
        self.__nb_node = nxgraph.order()
        self.__nb_cc = networkx.number_connected_components(nxgraph)
        self._nxgraph = nxgraph

        # internal graph representation
        self.__edges = set(map(frozenset, nxgraph.edges))
        self.__nodes = set(nxgraph.nodes)
        self.__hierarchy = {('cc', n) for n in nxgraph.nodes}
        self.__powernodes = defaultdict(set)  # (step, set) -> {node in powernode}
        self.__poweredges = defaultdict(set)  # (step, set) -> (step, set)

    @staticmethod
    def ccs_from_file(filename:str) -> iter:
        """Yield graphs found in given filename. Each graph is a connected component."""
        nxgraph = phasme.build_graph.graph_from_file(filename)
        yield from (Graph(nxgraph.subgraph(cc)) for cc in networkx.connected_components(nxgraph))

    def as_asp(self, step:int, powerobjects:bool=False) -> [str]:
        """Yield atoms of graph's ASP string representation, in edges and hierarchy.

        powerobjects -- also include powernodes and poweredges

        """
        for source, target in self.__edges:
            yield 'edge({},{}).'.format(source, target)
        for node in self.__nodes:
            yield 'membercc({}).'.format(node)
        for container, contained in self.__hierarchy:
            if isinstance(contained, str):
                yield 'block({},p(cc,{},{}),{}).'.format(step-1, *container, contained)
            else:
                yield 'include_block({},p(cc,{},{}),p(cc,{},{})).'.format(step-1, *container, *contained)
        if powerobjects:
            raise NotImplementedError()


    def compress(self, motif:Motif):
        # for upper, lower in motif.hierachy_added:
            # self.__hierarchy.add(upper, lower)
        # for upper, lower in motif.hierachy_removed:
            # self.__hierarchy.remove(upper, lower)
        print('COMPRESS…')
        for upper, lower in motif.include_blocks:
            # print('\tINC BLOCK', upper, lower)
            self.__hierarchy.add((upper, lower))

        for numset, node in motif.new_powernode:
            # print('\tP-NODE', numset, node)
            self.__powernodes[motif.uid, numset].add(node)
        for source, target in motif.new_poweredge:
            self.__poweredges[source].add(target)
        self.__edges -= set(motif.edges_covered)


    @property
    def nb_edge(self) -> int:
        return len(self.__edges)
    @property
    def nb_node(self) -> int:
        return self.__nb_node
    @property
    def nb_cc(self) -> int:
        return self.__nb_cc
    def neighbors(self, increasing_degree:bool=False,
                  nb_edges_between_neighbors:bool=False) -> iter:
        """Yield pairs (node, {neighbor}).

        increasing_degree -- yield the pairs sorted
        nb_edges_between_neighbors -- yield (node, {neighbors}, N), with N the
                                      number of edges in graph with given neighbors.

        """
        def yield_data():
            for node, neighbors in self._nxgraph.adjacency():
                neighbors = tuple(neighbors)
                if nb_edges_between_neighbors:
                    yield node, neighbors, self._nxgraph.subgraph(neighbors).size()
                else:
                    yield node, neighbors
        if increasing_degree:
            data = sorted(tuple(yield_data()), key=lambda x: len(x[1]))
        else:
            data = yield_data()
        data = tuple(data)
        yield from data


    def output(self, filename:str):
        def yield_lines():
            for source, target in self.__edges:
                yield 'EDGE\t{}\t{}\t1.0\n'.format(source, target)
            for uid in self.__powernodes:
                yield 'SET\t{}\t1.0\n'.format(format_name(uid))
            for container, contained in self.__hierarchy:
                yield 'IN\t{}\t{}\t1.0\n'.format(format_name(contained), format_name(container))  # contained first
            for source, targets in self.__poweredges.items():
                for target in targets:
                    yield 'EDGE\t{}\t{}\t1.0\n'.format(format_name(source), format_name(target))
        with open(filename, 'w') as fd:
            for line in yield_lines():
                fd.write(line)

def format_name(name):
    """Return string representation of powernode of given step and set nb.

    This string representation is not ASP valid,
     but can be used as name in most file formats :

        PWRN-<step>-<num_set>

    >>> format_name('cc')
    'cc'
    >>> format_name((1, 4))
    'PWRN-1-4'
    >>> format_name(('cc', 4))
    'PWRN-cc-4'

    """
    if isinstance(name, str):
        return name
    return 'PWRN-{}-{}'.format(*name)
