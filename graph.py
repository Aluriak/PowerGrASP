import phasme
import networkx
from collections import defaultdict
from pprint import pprint
from constants import TEST_INTEGRITY, SHOW_STORY

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
        self.__hierarchy = set()  # inclusions between powernodes
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
        assert step > 0, step
        assert (step-1) >= 0, step
        for source, target in self.__edges:
            yield 'edge({},{}).'.format(source, target)
        for (stepa, seta), nodes in self.__powernodes.items():
            for node in nodes:
                yield 'block({},{},{},{}).'.format(step-1, stepa, seta, node)
        for stepa, seta, stepb, setb in self.__hierarchy:
            yield 'include_block({},{},{},{},{}).'.format(step-1, stepa, seta, stepb, setb)
        if powerobjects:
            raise NotImplementedError()


    def compress(self, motif:Motif):
        print('COMPRESS…')
        pprint(dict(self.__powernodes))
        # handle the simple values: new powernodes, poweredges.
        for numset, node in motif.new_powernodes:
            print('\tP-NODE', numset, node)
            self.__powernodes[motif.uid, numset].add(node)
        for source, target in motif.new_poweredge:
            print('\tP-EDGE', source, target)
            self.__poweredges[source].add(target)

        # graph edges reduction and monitoring
        covered = frozenset(motif.edges_covered)
        nb_edges = len(self.__edges)
        self.__edges -= covered
        if nb_edges - len(covered) != len(self.__edges):
            diff = covered - self.__edges
            raise ValueError("{} edges yielded by {} searcher were not in the graph: {}"
                             "".format(len(diff), motif.name, ', '.join(map(str, diff))))
        print('\tCOVER', len(covered))

        # Now the big part: hierarchy. ASP send patch to apply on it.
        for args in motif.hierachy_added:
            print('\tADD HIERARCHY', args)
            self.__hierarchy.add(args)
            step_parent, num_parent, step_son, num_son = args
            # nodes in the parent block must be moved to the new block.
            # without that, the node would be at the same time in two powernodes.
            nodes = self.__powernodes[step_parent, num_parent] & self.__powernodes[step_son, num_son]
            if nodes:
                self.__powernodes[step_parent, num_parent] -= nodes
                self.__powernodes[step_son, num_son] |= nodes
                print('\tMOVE NODES: {} FROM {} TO {}'.format(nodes, (step_parent, num_parent), (step_son, num_son)))

        for args in motif.hierachy_removed:
            print('\tDEL HIERARCHY', args)
            self.__hierarchy.remove(args)

        # Checking that the total number of nodes didn't change,
        #  i.e. there is no node placed in two powernodes,
        #  would be a great idea, but there is no way to do that since there is
        #  no way to know how many nodes are on ground (not in any powernode)
        #  without using the self.__powernodes attribute.
        # import itertools
        # nb_nodes_in_pnodes = sum(1 for _ in itertools.chain.from_iterable(self.__powernodes.values()))
        # nb_nodes_in_ground = ...
        # assert nb_nodes_in_pnodes == self.nb_node, (nb_nodes_in_pnodes, self.nb_node)
        print('PNODES:')
        pprint(dict(self.__powernodes))



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
        """Write in given filename the bubble representation of the graph"""
        print('\n\n###########################\n')
        print('PNODES:')
        pprint(dict(self.__powernodes))
        print('HIERAC:')
        pprint(self.__hierarchy)
        print('PEDGES:')
        pprint(dict(self.__poweredges))
        print(' EDGES:')
        pprint(self.__edges)


        with open(filename, 'w') as fd:
            for line in self.bubble_repr():
                fd.write(line + '\n')


    def bubble_repr(self) -> iter:
        """Yield lines of bubble representation"""
        for uid in self.__powernodes:
            yield 'SET\t{}\t1.0'.format(format_name(uid))
        for stepa, seta, stepb, setb in self.__hierarchy:
            if stepa == 0 and seta == 0:  # base level
                continue  # ignore it
            yield 'IN\t{}\t{}'.format(format_name((stepb, setb)), format_name((stepa, seta)))  # contained first
        for (step, numset), nodes in self.__powernodes.items():
            for node in nodes:
                yield 'IN\t{}\t{}'.format(format_name(node), format_name((step, numset)))
        for source, targets in self.__poweredges.items():
            for target in targets:
                yield 'EDGE\t{}\t{}\t1.0'.format(format_name(source), format_name(target))
        for source, target in self.__edges:
            yield 'EDGE\t{}\t{}\t0.5'.format(source, target)


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
