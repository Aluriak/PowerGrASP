import phasme
import networkx
from collections import defaultdict
from pprint import pprint
from powergrasp import utils
from powergrasp import constants
from powergrasp.motif import Motif
from powergrasp.constants import (TEST_INTEGRITY, SHOW_STORY, SHOW_DEBUG,
                                  SHOW_MOTIF_HANDLING, COVERED_EDGES_FROM_ASP)


def proper_nx_graph(graph:networkx.Graph) -> networkx.Graph:
    """Return the same graph, but with properly formatted node names."""
    def node_repr(node:str or int or float) -> str or int or float:
        """Ensure that nodes in graph are well encoded, ie that integer
        nodes are integer in graph, because ASP will understand
        and handle them as integer.
        """
        if isinstance(node, str) and node.isnumeric():
            return int(node)
        elif isinstance(node, int):
            return node
        # print('NODE REPR:', node, utils.normalized_name(node))
        return utils.normalized_name(node)  # needed to avoid collisions with constants, variable,…
    proper = type(graph)()
    repr_edges = (frozenset(map(node_repr, edge)) for edge in graph.edges)  # apply node representation
    proper.add_edges_from(edge for edge in repr_edges if len(edge) == 2)  # filter self loops
    return proper


class Graph:
    """A graph object, exposing some data on it.

    Note that a data is computed during its first access.

    Note the uid parameter for constructor

    """
    def __init__(self, graph:str or networkx.Graph):
        if isinstance(graph, networkx.Graph):
            nxgraph = networkx.Graph(graph)
        elif isinstance(graph, str):
            nxgraph = phasme.build_graph.graph_from_file(graph)
        else:
            raise ValueError("Unexpected {}".format(graph))
        # internal graph representation
        self.__edges = map(frozenset, nxgraph.edges)
        if TEST_INTEGRITY:
            self.__edges = tuple(self.__edges)
            for args in self.__edges:
                if len(args) > 2:
                    print('WARNING: Weird edge: {}. It will be filtered.'.format(args))
                else:
                    assert len(args) == 2, args
        self.__edges = set(edge for edge in self.__edges if len(edge) == 2)

        # data
        self.__nodes = set(nxgraph.nodes)
        self.__uid = str(min(self.__nodes, key=str))
        self.__nb_node = len(self.__nodes)
        self.__nb_cc = networkx.number_connected_components(nxgraph)
        self._nxgraph = networkx.freeze(nxgraph)

        self.__hierarchy = set()  # inclusions between powernodes
        self.__powernodes = defaultdict(set)  # (step, set) -> {node in powernode}
        self.__poweredges = defaultdict(set)  # (step, set) -> (step, set)

    @staticmethod
    def ccs_from_file(filename:str) -> iter:
        """Yield graphs found in given filename. Each graph is a connected component."""
        nxgraph = proper_nx_graph(phasme.build_graph.graph_from_file(filename))
        yield from (Graph(nxgraph.subgraph(cc))
                    for cc in networkx.connected_components(nxgraph))

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
        if SHOW_STORY or SHOW_DEBUG:
            print('COMPRESS…')
        if SHOW_DEBUG:
            pprint(dict(self.__powernodes))
        # Add the poweredges
        for source, target in motif.new_poweredge:
            if SHOW_MOTIF_HANDLING: print('\tP-EDGE', source, target)
            self.__poweredges[source].add(target)
        # Get the powernodes as set of nodes, and build the new ones.
        if not COVERED_EDGES_FROM_ASP:
            powernodes = set(motif.powernodes) | set(motif.stars)  # set of nodes
        for numset, node in motif.new_powernodes:
            uid = motif.uid, numset
            if SHOW_MOTIF_HANDLING: print('\tP-NODE', *uid, node)
            self.__powernodes[uid].add(node)
            if not COVERED_EDGES_FROM_ASP: powernodes.add(uid)

        # graph edges reduction and monitoring
        if COVERED_EDGES_FROM_ASP:
            covered = frozenset(motif.edges_covered())
        else:
            covered = frozenset(motif.edges_covered(self.__powernodes.get(uid, {uid}) for uid in powernodes))
        nb_edges = len(self.__edges)
        if TEST_INTEGRITY:
            edges = frozenset(self.__edges)
            if SHOW_DEBUG: print('IFBTVC GRAPH:', self.__edges)
            if SHOW_DEBUG: print('ZEDRBM COVER:', covered)
        self.__edges -= covered
        diff = nb_edges - len(covered) != len(self.__edges)
        if TEST_INTEGRITY and diff:
            diff_cov = covered - edges
            diff_edg = edges - covered
            raise ValueError("{} edges yielded by {} searcher were not in the graph: {}.\n\n"
                             "{} edges in the graph were not in the {} searcher: {}."
                             "".format(len(diff_cov), motif.name, ', '.join(map(str, diff_cov)),
                                       len(diff_edg), motif.name, ', '.join(map(str, diff_edg))))
        elif diff:
            raise ValueError("Edges yielded by {} searcher were not in the graph."
                             " Rerun with TEST_INTEGRITY to get the problem."
                             "".format(motif.name))
        if SHOW_MOTIF_HANDLING:
            print('\tCOVER', len(covered))

        # Now the big part: hierarchy. ASP send patch to apply on it.
        for args in motif.hierachy_added:
            if SHOW_MOTIF_HANDLING:
                print('\tADD HIERARCHY', args)
            self.__hierarchy.add(args)
            step_parent, num_parent, step_son, num_son = args
            # nodes in the parent block must be moved to the new block.
            # without that, the node would be at the same time in two powernodes.
            nodes = self.__powernodes[step_parent, num_parent] & self.__powernodes[step_son, num_son]
            if nodes:
                self.__powernodes[step_parent, num_parent] -= nodes
                self.__powernodes[step_son, num_son] |= nodes
                if SHOW_MOTIF_HANDLING:
                    print('\tMOVE NODES: {} FROM {} TO {}'.format(nodes, (step_parent, num_parent), (step_son, num_son)))

        for args in motif.hierachy_removed:
            if SHOW_MOTIF_HANDLING:
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
        if SHOW_DEBUG:
            print('PNODES:')
            pprint(dict(self.__powernodes))

        if TEST_INTEGRITY:
            inclusions = defaultdict(set)
            for stp, nsp, sts, nss in self.__hierarchy:
                inclusions[stp, nsp].add((sts, nss))
            # reversed:
            parents = defaultdict(set)
            for parent, sons in inclusions.items():
                for son in sons:
                    parents[son].add(parent)
            # detect son with multiple parents
            multiple_parents = {son for son, parents in parents.items() if len(parents) > 1}
            if multiple_parents:
                print('ERROR MULTIPLE PARENT:', len(multiple_parents))
                pprint(multiple_parents)
                exit(1)


    def compress_all(self, motifs:iter) -> int:
        """Compress all given motifs."""
        for step_diff, motif in enumerate(motifs, start=0):
            motif.increase_step(step_diff)
            self.compress(motif)
        return step_diff


    @property
    def uid(self) -> str:
        return self.__uid
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
        if SHOW_DEBUG:
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


    def bubble_repr(self, head_comment:str='') -> iter:
        """Yield lines of bubble representation"""
        if head_comment:
            yield from ('# ' + line for line in head_comment.splitlines(False))
        _format_name = lambda x: format_name(format_name(None, self.uid), x)
        if constants.BUBBLE_WITH_NODES:
            for node in self.__nodes:
                yield 'NODE\t{}'.format(_format_name(node))
        if constants.BUBBLE_WITH_SETS:
            for uid in self.__powernodes:
                yield 'SET\t{}\t1.0'.format(_format_name(uid))
        for stepa, seta, stepb, setb in self.__hierarchy:
            if stepa == 0 and seta == 0:  # base level
                continue  # ignore it
            yield 'IN\t{}\t{}'.format(_format_name((stepb, setb)), _format_name((stepa, seta)))  # contained first
        for (step, numset), nodes in self.__powernodes.items():
            for node in nodes:
                yield 'IN\t{}\t{}'.format(_format_name(node), _format_name((step, numset)))
        for source, targets in self.__poweredges.items():
            for target in targets:
                source, target = sorted(tuple(map(_format_name, (source, target))))
                yield 'EDGE\t{}\t{}\t{}'.format(source, target, constants.BUBBLE_POWEREDGE_FACTOR)
        for source, target in self.__edges:
            source, target = sorted(tuple(map(_format_name, (source, target))))
            yield 'EDGE\t{}\t{}\t{}'.format(source, target, constants.BUBBLE_EDGE_FACTOR)


def format_name(cc:str, name:str or tuple):
    """Return string representation of powernode of given step and set nb.

    This string representation is not ASP valid,
     but can be used as name in most file formats :

        PWRN-<cc>-<step>-<num_set>

    >>> format_name(1, 'cc')
    'cc'
    >>> format_name(1, '"A"')
    'A'
    >>> format_name(1, 'A')
    'A'
    >>> format_name(42, (1, 4))
    'PWRN-42-1-4'
    >>> format_name(23, ('cc', 4))
    'PWRN-23-cc-4'
    >>> format_name(23, ('"cc"', 4))
    'PWRN-23-cc-4'

    """
    if isinstance(name, int):
        return str(name)
    elif isinstance(name, str):
        if constants.BUBBLE_SIMPLIFY_QUOTES and name[0] == '"' and name[-1] == '"':
            return name[1:-1]
        else:
            return name
    return 'PWRN-{}-{}-{}'.format(cc, *map(lambda x: format_name(None, x), name))
