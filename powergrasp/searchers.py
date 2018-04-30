
import itertools
from collections import defaultdict

from . import asp
from . import utils
from .motif import Motif
from .graph import Graph
from .constants import TEST_INTEGRITY, SHOW_STORY, SHOW_DEBUG, MULTISHOT_MOTIF_SEARCH, BICLIQUE_LOWERBOUND_MAXNEI, OPTIMIZE_FOR_MEMORY, CLINGO_OPTIONS
from . import ASP_FILES


MOTIF_ASP_FILES = ASP_FILES['process-motif'], ASP_FILES['scoring_powergraph'], (ASP_FILES['block-constraint-memory'] if OPTIMIZE_FOR_MEMORY else ASP_FILES['block-constraint-cpu'])
CLIQUE_ASP_FILES = (ASP_FILES['search-clique'], *MOTIF_ASP_FILES)
FULLBICLIQUE_ASP_FILES = (ASP_FILES['search-fullbiclique'], *MOTIF_ASP_FILES)
BICLIQUE_ASP_FILES = (ASP_FILES['search-biclique'], *MOTIF_ASP_FILES)
STAR_ASP_FILES = (ASP_FILES['search-star'], *MOTIF_ASP_FILES)


class MotifSearcher:
    """A motif searcher instance provides a search over a graph
    of a particular motif.
    If the graph must change more than described by signals,
    the motif searcher instance is invalid.

    It consists in the following client API:

    - init_for_graph: called on the graph on which the search will take place.
    - search: called to search a motif in the graph.
    - on_new_compressed_motif: called when a new motif is compressed. Information on that motif is given, notably its score.
    - covered_edges: function giving the edges covered by a given motif

    And the following methods to be overwritten (if no default) by subclasses:

    - name: the name of the motif, human-readable, making it different from the others.
    - _compute_initial_upperbound: give upperbound at first step for given graph (default: number of graph edges)
    - _compute_initial_lowerbound: idem for lowerbound (default: 2)
    - _search: called to search a motif in the graph, returns atoms found by ASP solver.

    Note that a motif searcher will maintain by itself the lowerbound
    and upperbound for the motifs, by considering that a motif score is the maximal it can do.
    Computations of these bounds may rely on complex computations
    and information taken from the graph receive by init.

    """

    def __init__(self, graph:Graph):
        self.graph = graph
        self.init_for_graph(graph)

    def init_for_graph(self, graph:Graph):
        if hasattr(self, 'compute_initial_bounds'):  # all-in-one method
            self._lowerbound, self._upperbound = self.compute_initial_bounds(graph)
        else:  # use the standard one
            self._lowerbound = self.compute_initial_lowerbound(graph)
            self._upperbound = self.compute_initial_upperbound(graph)
        if self._lowerbound in {0, 1}:
            print("WARNING lowerbound computed for {} is {}, which is an "
                  "unexpected number.".format(self.name, self._lowerbound))
        self._lowerbound = max(2, self._lowerbound)
        if SHOW_STORY and self.lowerbound > self.upperbound:
            print("INFO Search for {} will not be functional, because bounds"
                  " ({};{}) avoid any search.".format(self.name, *self.bounds))

    @property
    def lowerbound(self) -> int:  return self._lowerbound
    @property
    def upperbound(self) -> int:  return self._upperbound
    @property
    def bounds(self) -> (int, int):  return self.lowerbound, self.upperbound

    def compute_initial_upperbound(self, graph:Graph) -> int:
        return graph.nb_edge
    def compute_initial_lowerbound(self, graph:Graph) -> int:
        return 2
    def on_new_compressed_motif(self, motif:Motif):
        """How to react when a motif is compressed ?"""
        if motif.ismaximal and motif.name == self.name:
            self._upperbound = motif.score
        self._lowerbound = 2  # now the optimization is not valid


    def search(self, step:int, score_to_beat:int=0) -> [Motif]:
        """Search for motifs, better than the one to beat."""
        lowerbound = max(self.lowerbound, score_to_beat)
        if lowerbound > self.upperbound:
            if SHOW_STORY:
                print("INFO No {} search because of bounds ({};{})."
                      "".format(self.name, *self.bounds))
            return  # impossible to find a motif in such conditions
        models = self._search(step, self.graph, lowerbound, self.upperbound)
        yield from (
            Motif(self.name, model, maximal=True, step=step, searcher=self)
            for model in models
        )

    def _search(self, graph:Graph, lowerbound:int, upperbound:int) -> Motif:
        raise NotImplementedError()


    def covered_edges(self, motif:Motif) -> iter:
        """Yield edges covered by given motif."""
        raise NotImplementedError()

    def _clingo_options(self):
        return CLINGO_OPTIONS[None] + ' ' + CLINGO_OPTIONS.get(self.name, '')


class BicliqueSearcher(MotifSearcher):
    """Searcher for Bicliques, including stars."""

    name = 'biclique'

    def compute_initial_lowerbound(self, graph:Graph) -> int:
        """Maximal lowerbound is the score of biggest star, or the score of the biggest intersection"""
        n = {node: frozenset(neighbors) for node, neighbors in graph.neighbors()}
        biggest_star = max(len(neighbors) for _, neighbors in graph.neighbors())
        if BICLIQUE_LOWERBOUND_MAXNEI <= 1:
            return biggest_star
        elif BICLIQUE_LOWERBOUND_MAXNEI == 2:
            maxnei2 = max(len(n[a] & n[b]) * 2 for a, b in itertools.combinations(n.keys(), r=2))
            return max(maxnei2, biggest_star)
        elif BICLIQUE_LOWERBOUND_MAXNEI >= 3:
            maxnei = 0
            for level in range(2, BICLIQUE_LOWERBOUND_MAXNEI + 1):
                max_for_level = max(len(frozenset.intersection(*(n[s] for s in sets))) * level for sets in itertools.combinations(n.keys(), r=level))
                if max_for_level <= maxnei: break
                maxnei = max_for_level
                if maxnei <= biggest_star: break
            return max(maxnei, biggest_star)
        else:
            maxnei2 = max(len(n[a] & n[b]) * 2 for a, b in itertools.combinations(n.keys(), r=2))
            return max(maxnei2, biggest_star)

    def _search(self, step:int, graph:Graph, lowerbound:int, upperbound:int) -> iter:
        graph = ''.join(graph.as_asp(step))
        if SHOW_DEBUG:
            print('MXDKJX: GRAPH:', graph)
        yield from asp.solve_motif_search(step, lowerbound, upperbound,
                                          options=self._clingo_options(),
                                          files=FULLBICLIQUE_ASP_FILES, graph=graph)

    def covered_edges(self, sets:[frozenset]) -> iter:
        """Return the edges that are covered by given sets"""
        assert len(sets) == 2
        yield from map(frozenset, itertools.product(*sets))


class NonStarBicliqueSearcher(MotifSearcher):
    """Searcher for Bicliques with at least 2 elements in each set.

    To be combined with StarSearcher to reproduce the behavior of
    BicliqueSearcher.

    """

    name = 'non-star-biclique'

    def compute_initial_lowerbound(self, graph:Graph) -> int:
        """Maximal lowerbound is the score of biggest star, or the score of the biggest intersection"""
        n = {node: frozenset(neighbors) for node, neighbors in graph.neighbors()}
        if BICLIQUE_LOWERBOUND_MAXNEI >= 3:
            maxnei = 0
            for level in range(2, BICLIQUE_LOWERBOUND_MAXNEI + 1):
                max_for_level = max(len(frozenset.intersection(*(n[s] for s in sets))) * level for sets in itertools.combinations(n.keys(), r=level))
                if max_for_level <= maxnei: break
                maxnei = max_for_level
            return maxnei
        else:
            maxnei2 = max(len(n[a] & n[b]) * 2 for a, b in itertools.combinations(n.keys(), r=2))
            return maxnei2

    def _search(self, step:int, graph:Graph, lowerbound:int, upperbound:int) -> iter:
        graph = ''.join(graph.as_asp(step))
        if SHOW_DEBUG:
            print('UHJGMR: GRAPH:', graph)
        yield from asp.solve_motif_search(step, lowerbound, upperbound,
                                          options=self._clingo_options(),
                                          files=BICLIQUE_ASP_FILES, graph=graph)

    def covered_edges(self, sets:[frozenset]) -> iter:
        """Return the edges that are covered by given sets"""
        assert len(sets) == 2
        yield from map(frozenset, itertools.product(*sets))


class StarSearcher(MotifSearcher):
    """Searcher for Stars."""

    name = 'star'

    def __init__(self, graph:Graph):
        self.__star_size = max(len(neighbors) for _, neighbors in graph.neighbors())
        super().__init__(graph)


    def compute_initial_lowerbound(self, graph:Graph) -> int:
        return self.__star_size
    def compute_initial_upperbound(self, graph:Graph) -> int:
        return self.__star_size

    def _search(self, step:int, graph:Graph, lowerbound:int, upperbound:int) -> iter:
        graph = ''.join(graph.as_asp(step))
        if SHOW_DEBUG:
            print('ABQSSN: GRAPH:', graph)
        yield from asp.solve_motif_search(step, lowerbound, upperbound,
                                          options=self._clingo_options(),
                                          files=STAR_ASP_FILES, graph=graph)

    def covered_edges(self, sets:[frozenset]) -> iter:
        """Return the edges that are covered by given sets"""
        assert any(len(set) == 1 for set in sets)
        assert len(sets) == 2
        yield from map(frozenset, itertools.product(*sets))


class CliqueSearcher(MotifSearcher):
    """Searcher for Cliques."""

    name = 'clique'

    def compute_initial_bounds(self, graph:Graph) -> ():
        """Return lowerbound and upperbound for initial problems.

        If any node with clustering coefficient equals to 1 exists,
        the number of neighbors gives a lowerbound.

        Use utils.maximal_clique_size function on all nodes of graph to
        compute the biggest clique possible theoretically.

        """
        node_to_edge = lambda n: (n * (n - 1)) // 2
        min_clique_size, max_clique_size = 0, 0
        for node, neighbors, nb_edge in graph.neighbors(increasing_degree=True, nb_edges_between_neighbors=True):
            node_clique_size = utils.maximal_clique_size(nb_edge)
            max_clique_size = max(max_clique_size, node_clique_size)
            if nb_edge == node_to_edge(len(neighbors)):  # clustering coefficient is 1
                min_clique_size = max(min_clique_size, len(neighbors))
            # if clique_size > len(neighbors):  # TODO: test and prove useful that optimization
                # break  # we can't found better since it's sorted
        return max(3, node_to_edge(min_clique_size)), node_to_edge(max_clique_size)


    def _search(self, step:int, graph:Graph, lowerbound:int, upperbound:int) -> iter:
        graph = ''.join(graph.as_asp(step))
        yield from asp.solve_motif_search(step, lowerbound, upperbound,
                                          options=self._clingo_options(),
                                          files=CLIQUE_ASP_FILES, graph=graph)

    def covered_edges(self, sets:[frozenset]) -> iter:
        """Return the edges that are covered by given sets"""
        assert len(sets) == 1
        nodes = frozenset(next(iter(sets)))
        yield from map(frozenset, itertools.combinations(nodes, r=2))


# verify clingo options
SEARCHERS = {searcher.name for searcher in globals().values()
             if type(searcher) is type and issubclass(searcher, MotifSearcher) and searcher is not MotifSearcher}
for searcher in CLINGO_OPTIONS:
    if searcher not in SEARCHERS and searcher is not None:
        raise ValueError("CLINGO_OPTIONS got a non-valid searcher value: " + searcher)
