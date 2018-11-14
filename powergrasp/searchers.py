
import math
import itertools
from collections import defaultdict

from . import asp
from . import utils
from .utils import get_time
from .motif import Motif
from .graph import Graph
from .recipe import RecipeEntry
from .constants import (TEST_INTEGRITY, SHOW_STORY, SHOW_DEBUG, KEEP_SINGLE_NODES,
                        MULTISHOT_MOTIF_SEARCH, BICLIQUE_LOWERBOUND_MAXNEI,
                        OPTIMIZE_FOR_MEMORY, CLINGO_OPTIONS)
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
        self.__timer = None

    def init_for_graph(self, graph:Graph):
        if hasattr(self, 'compute_initial_bounds'):  # all-in-one method
            self._lowerbound, self._upperbound = self.compute_initial_bounds(graph)
        else:  # use the standard one
            self._lowerbound = self.compute_initial_lowerbound(graph)
            self._upperbound = self.compute_initial_upperbound(graph)
        if not KEEP_SINGLE_NODES and self._lowerbound in {0, 1}:
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
    def compute_new_lowerbound(self, graph:Graph, motif:Motif) -> int:
        return 2

    def on_new_found_motif(self, motif:Motif):
        """How to react when a motif is found ?"""
        if motif.ismaximal and motif.name == self.name:
            self._upperbound = min(self._upperbound, motif.score)

    def on_new_compressed_motif(self, motif:Motif):
        """How to react when a motif is compressed ?"""
        self._lowerbound = self.compute_new_lowerbound(self.graph, motif)


    def search(self, step:int, score_to_beat:int=0, recipe:RecipeEntry=None) -> [Motif]:
        """Search for motifs, better than the one to beat."""
        self.__timer = get_time()
        if recipe and not recipe.isbreakable:
            supplementary_asp_atoms = recipe.as_asp(is_star=self.name == 'star')
            lowerbound = len(recipe.seta) * len(recipe.setb)
            upperbound = self.upperbound if recipe.isextendable else lowerbound
            if SHOW_DEBUG:
                print(f'DEBUG recipe {recipe} used.')
        elif recipe and recipe.isbreakable:
            supplementary_asp_atoms = ''
            lowerbound = 2
            upperbound = self.upperbound
            if SHOW_DEBUG:
                print(f'DEBUG breakable recipe {recipe} used.')
        else:
            supplementary_asp_atoms = ''
            lowerbound = max(self.lowerbound, score_to_beat+1)
            upperbound = self.upperbound
            if SHOW_DEBUG:
                print('DEBUG no recipe available.')
        if lowerbound > upperbound:
            if SHOW_STORY:
                print("INFO No {} search because of bounds ({};{})."
                      "".format(self.name, *self.bounds))
            return  # impossible to find a motif in such conditions
        models = self._search(step, self.graph.with_recipe(recipe), lowerbound, upperbound, supplementary_asp_atoms)
        yield from (
            # the Motif is maximal, unless a recipe was biasing the search
            Motif(self.name, model, maximal=not recipe, step=step, searcher=self)
            for model in models
        )
        self.__timer = get_time() - self.__timer

    @property
    def last_search_time(self) -> float:
        return self.__timer

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

    def compute_initial_bounds(self, graph:Graph) -> int:
        """
        Maximal lowerbound is the score of biggest star, or the score of the biggest intersection.
        Minimal upperbound is the maximal possible association of the most connected nodes
        """
        neis = {node: frozenset(neighbors) for node, neighbors in graph.neighbors()}
        sorted_degrees = sorted(tuple(map(len, neis.values())), reverse=True)
        try:
            upperbound = max(idx * deg for idx, deg in enumerate(sorted_degrees, start=1) if deg > 1)
        except ValueError:
            upperbound = math.inf
        upperbound = min(upperbound, graph.nb_edge)
        biggest_star = max(len(neighbors) for neighbors in neis.values())
        if BICLIQUE_LOWERBOUND_MAXNEI <= 1:
            lowerbound = biggest_star
        elif BICLIQUE_LOWERBOUND_MAXNEI == 2:
            maxnei2 = max(len(neis[a] & neis[b]) * 2 for a, b in itertools.combinations(neis.keys(), r=2))
            lowerbound = max(maxnei2, biggest_star)
        elif BICLIQUE_LOWERBOUND_MAXNEI >= 3:
            lowerbound = 0
            for level in range(2, BICLIQUE_LOWERBOUND_MAXNEI + 1):
                try:
                    max_for_level = max(len(frozenset.intersection(*(neis[s] for s in sets))) * level for sets in itertools.combinations(neis.keys(), r=level))
                except ValueError:
                    max_for_level = 0
                if max_for_level < lowerbound: break
                if lowerbound < biggest_star: break
                lowerbound = max(lowerbound, max_for_level)
        else:
            maxnei2 = max(len(neis[a] & neis[b]) * 2 for a, b in itertools.combinations(neis.keys(), r=2))
            lowerbound = max(maxnei2, biggest_star)
        return lowerbound, upperbound


    def _search(self, step:int, graph:Graph, lowerbound:int, upperbound:int, other_atoms:str='') -> iter:
        graph = ''.join(graph.as_asp(step, filter_for_bicliques=True, lowerbound=lowerbound, upperbound=upperbound))
        if SHOW_DEBUG:
            print('MXDKJX: GRAPH:', graph + '\n' + other_atoms)
        yield from asp.solve_motif_search(step, lowerbound, upperbound,
                                          options=self._clingo_options(),
                                          files=FULLBICLIQUE_ASP_FILES,
                                          graph=graph + other_atoms)

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

    def compute_initial_bounds(self, graph:Graph) -> int:
        """
        Maximal lowerbound is the score of the biggest intersection.
        Minimal upperbound is the maximal possible association of the most connected nodes
        """
        neis = {node: frozenset(neighbors) for node, neighbors in graph.neighbors()}
        sorted_degrees = sorted(tuple(map(len, neis.values())), reverse=True)
        try:
            upperbound = max(idx * deg for idx, deg in enumerate(sorted_degrees, start=1) if deg > 1)
        except ValueError:
            upperbound = math.inf
        upperbound = min(upperbound, graph.nb_edge)
        if BICLIQUE_LOWERBOUND_MAXNEI >= 3:
            maxnei = 0
            for level in range(2, BICLIQUE_LOWERBOUND_MAXNEI + 1):
                try:
                    max_for_level = max(len(frozenset.intersection(*(neis[s] for s in sets))) * level for sets in itertools.combinations(neis.keys(), r=level))
                except ValueError:
                    max_for_level = 0
                if max_for_level < maxnei: break
                maxnei = max_for_level
        else:
            try:
                maxnei = max(len(neis[a] & neis[b]) * 2 for a, b in itertools.combinations(neis.keys(), r=2))
            except ValueError:
                maxnei = 0
        return maxnei, upperbound

    def compute_new_lowerbound(self, graph:Graph, motif:Motif) -> int:
        return 4  # At least 2 elements in each set

    def _search(self, step:int, graph:Graph, lowerbound:int, upperbound:int, other_atoms:str='') -> iter:
        graph = ''.join(graph.as_asp(step, filter_for_bicliques=True, lowerbound=lowerbound, upperbound=upperbound))
        if SHOW_DEBUG:
            print('UHJGMR: GRAPH:', graph + '\n' + other_atoms)
        yield from asp.solve_motif_search(step, lowerbound, upperbound,
                                          options=self._clingo_options(),
                                          files=BICLIQUE_ASP_FILES,
                                          graph=graph + other_atoms)

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

    def _search(self, step:int, graph:Graph, lowerbound:int, upperbound:int, other_atoms:str='') -> iter:
        graph = ''.join(graph.as_asp(step, filter_for_stars=True, lowerbound=lowerbound, upperbound=upperbound))
        if SHOW_DEBUG:
            print('ABQSSN: GRAPH:', graph + '\n' + other_atoms)
        yield from asp.solve_motif_search(step, lowerbound, upperbound,
                                          options=self._clingo_options(),
                                          files=STAR_ASP_FILES,
                                          graph=graph + other_atoms)

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

    def compute_new_lowerbound(self, graph:Graph, motif:Motif) -> int:
        return 3  # At least 3 elements in a clique


    def _search(self, step:int, graph:Graph, lowerbound:int, upperbound:int, other_atoms:str='') -> iter:
        graph = ''.join(graph.as_asp(step, filter_for_cliques=True, lowerbound=lowerbound, upperbound=upperbound))
        if SHOW_DEBUG:
            print('OKAPOD: GRAPH:', graph + '\n' + other_atoms)
        yield from asp.solve_motif_search(step, lowerbound, upperbound,
                                          options=self._clingo_options(),
                                          files=CLIQUE_ASP_FILES,
                                          graph=graph + other_atoms)

    def covered_edges(self, sets:[frozenset]) -> iter:
        """Return the edges that are covered by given sets"""
        assert len(sets) == 1
        nodes = frozenset(next(iter(sets)))
        yield from map(frozenset, itertools.combinations(nodes, r=2))


# verify clingo options
SEARCHERS = {searcher.name: searcher for searcher in globals().values()
             if type(searcher) is type and issubclass(searcher, MotifSearcher) and searcher is not MotifSearcher}
for searcher in CLINGO_OPTIONS:
    if searcher not in SEARCHERS and searcher is not None:
        raise ValueError("CLINGO_OPTIONS got a non-valid searcher value: " + searcher)
