
import asp
import utils

from motif import Motif
from graph import Graph


class MotifSearcher:
    """A motif searcher instance provides a search over a graph
    of a particular motif.
    If the graph must change more than described by signals,
    the motif searcher instance is invalid.

    It consists in the following client API:

    - init_for_graph: called on the graph on which the search will take place.
    - search: called to search a motif in the graph.
    - on_new_compressed_motif: called when a new motif is compressed. Information on that motif is given, notably its score.
    - name: the name of the motif, human-readable, making it different from the others.

    And the following methods to be overwritten (if no default) by subclasses:

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
        self.upperbound = self.compute_initial_upperbound(graph)
        self.lowerbound = self.compute_initial_lowerbound(graph)

    def compute_initial_upperbound(self, graph:Graph) -> int:
        return graph.nb_edge
    def compute_initial_lowerbound(self, graph:Graph) -> int:
        return 2
    def on_new_compressed_motif(self, motif:Motif):
        """How to react when a motif is compressed ?"""
        if motif.ismaximal:
            self.upperbound = motif.score


    def search(self, step:int, score_to_beat:int=0) -> Motif:
        """Search for a motif, better than the one to beat."""
        lowerbound = max(self.lowerbound, score_to_beat)
        assert isinstance(lowerbound, int)
        atoms = self._search(step, self.graph, lowerbound, self.upperbound)
        if atoms is None:  return None
        return Motif(self.name, atoms, maximal=True, step=step)

    def _search(self, graph:Graph, lowerbound:int, upperbound:int) -> Motif:
        raise NotImplementedError()

    @property
    def name(self) -> str:
        return str(self._name())
    def _name(self) -> str:
        raise NotImplementedError()


class BicliqueSearcher(MotifSearcher):
    """Searcher for bicliques."""

    def _name(self) -> str: return 'biclique'

    def compute_initial_lowerbound(self, graph:Graph) -> int:
        """Maximal lowerbound is the score of biggest star"""
        return max(len(neighbors) for _, neighbors in graph.neighbors())

    def _search(self, step:int, graph:Graph, lowerbound:int, upperbound:int) -> iter:
        graph = ''.join(graph.as_asp(step))
        files = ('asp/search-biclique.lp', 'asp/process-motif.lp', 'asp/scoring_powergraph.lp')
        return asp.solve_motif_search(step, lowerbound, upperbound, files=files, graph=graph)


class CliqueSearcher(MotifSearcher):
    """Searcher for Cliques."""

    def _name(self) -> str: return 'clique'

    def compute_initial_upperbound(self, graph:Graph) -> int:
        """Use utils.maximal_clique_size function on all nodes of graph to
        compute the biggest clique possible theoretically."""
        upperbound = 0
        for node, neighbors, nb_edge in graph.neighbors(increasing_degree=True, nb_edges_between_neighbors=True):
            clique_size = utils.maximal_clique_size(nb_edge)
            # if upperbound > len(neighbors):  # TODO: test and prove useful that optimization
                # break  # we can't found better since it's sorted
            upperbound = max(upperbound, upperbound)
        return upperbound

    def _search(self, step:int, graph:Graph, lowerbound:int, upperbound:int) -> iter:
        graph = ''.join(graph.as_asp(step))
        files = ('asp/search-clique.lp', 'asp/process-motif.lp', 'asp/scoring_powergraph.lp')
        return asp.solve_motif_search(step, lowerbound, upperbound, files=files, graph=graph)
