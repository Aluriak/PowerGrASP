
from constants import TEST_INTEGRITY, SHOW_STORY, COVERED_EDGES_FROM_ASP


class Motif:
    """A motif found by a motif searcher.

    The motif is a proxy to the ASP model, with a large set of properties
    that Graph and Searchers will use to determine the Motif effect
    on the Graph.

    """
    def __init__(self, typename:str, atoms:dict, maximal:bool, step:int, covered_edges_function:callable):
        self.typename, self.atoms, self.ismaximal, self.step = str(typename), atoms, bool(maximal), int(step)
        self._covered_edges_function = covered_edges_function
        if SHOW_STORY:
            from pprint import pprint
            print('ATOMS FOR MOTIF {}:'.format(typename))
            pprint(self.atoms)
        self._score = None


    @property
    def name(self) -> str:  return self.typename
    @property
    def uid(self) -> int:  return self.step


    @property
    def score(self) -> int:
        if self._score is None:
            self._score = self._compute_score()
        return self._score
    @property
    def edge_cover(self) -> int:
        return self.score

    def _compute_score(self) -> int:
        """Compute and return the score of this motif"""
        score_atoms = tuple(self.atoms.get('score', ()))
        if not score_atoms:
            raise ASPModelError("No atom `score` found")
        if len(score_atoms) > 1:
            raise ASPModelError("Multiple atom `score` found: {}".format(len(score_atoms)))
        score_atom_args = score_atoms[0]
        if len(score_atom_args) != 1:
            raise ASPModelError("Atom `score` got a non-valid number of arguments: {}".format(score_atom_args))
        score = score_atom_args[0]
        if not isinstance(score, int):
            raise ASPModelError("Atom `score` got a non-int argument of type {}: {}".format(type(score), score))
        assert isinstance(score, int)
        return score


    @property
    def new_powernodes(self) -> iter:
        yield from self.atoms.get('new_powernode', ())
    @property
    def powernodes(self) -> iter:
        yield from self.atoms.get('powernode', ())
    @property
    def stars(self) -> iter:
        yield from (args[0] for args in self.atoms.get('star', ()))
    @property
    def new_poweredge(self) -> iter:
        for args in self.atoms.get('poweredge', ()):
            if len(args) == 4:
                step_a, set_a, step_b, set_b = args
                yield (step_a, set_a), (step_b, set_b)
            elif len(args) == 3:
                step_a, set_a, node = args
                yield (step_a, set_a), node
    @property
    def edges_covered(self) -> iter:
        """Note that the computation of edges covered by the motif is delegated
        to the searcher object, in order to avoid a costly output from ASP.
        This may or may not be useful.

        """
        if COVERED_EDGES_FROM_ASP:
            yield from map(frozenset, self.atoms.get('covered_edge', ()))
        else:
            yield from frozenset(self._covered_edges_function(self))
    @property
    def hierachy_added(self) -> iter:
        yield from self.atoms.get('hierarchy_add', ())
    @property
    def hierachy_removed(self) -> iter:
        yield from self.atoms.get('hierarchy_remove', ())
