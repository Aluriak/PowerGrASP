
from powergrasp.constants import TEST_INTEGRITY, SHOW_DEBUG, COVERED_EDGES_FROM_ASP


class Motif:
    """A motif found by a motif searcher.

    The motif is a proxy to the ASP model, with a large set of properties
    that Graph and Searchers will use to determine the Motif effect
    on the Graph.

    """
    def __init__(self, typename:str, atoms:dict, maximal:bool, step:int, searcher:object):
        self.typename, self.atoms, self.ismaximal, self.step = str(typename), dict(atoms), bool(maximal), int(step)
        self.step_modifier = 0
        self._searcher = searcher
        if SHOW_DEBUG:
            from pprint import pprint
            print('ATOMS FOR MOTIF {}:'.format(typename))
            pprint(self.atoms)
        self._score = None


    @property
    def name(self) -> str:  return self.typename
    @property
    def uid(self) -> int:  return self.step + self.step_modifier
    @property
    def type(self):  return self._searcher


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

    def increase_step(self, step_diff:int):
        """Increase internally the step of self"""
        self.step_modifier += int(step_diff)

    @property
    def new_nodes(self) -> iter:
        yield from (node for numset, node in self.atoms.get('new_powernode', ()))
        yield from self.stars
    @property
    def new_powernodes(self) -> iter:
        yield from self.atoms.get('new_powernode', ())
    @property
    def powernodes(self) -> iter:
        _ = lambda s: s + (self.step_modifier if s == self.step else 0)
        yield from (
            (_(step), numset) for step, numset in self.atoms.get('powernode', ())
        )
    @property
    def stars(self) -> iter:
        yield from (args[0] for args in self.atoms.get('star', ()))
    @property
    def new_poweredge(self) -> iter:
        _ = lambda s: s + (self.step_modifier if s == self.step else 0)
        for args in self.atoms.get('poweredge', ()):
            if len(args) == 4:
                step_a, set_a, step_b, set_b = args
                yield (_(step_a), set_a), (_(step_b), set_b)
            elif len(args) == 3:
                step_a, set_a, node = args
                yield (_(step_a), set_a), node
    @property
    def hierachy_added(self) -> iter:
        _ = lambda s: s + (self.step_modifier if s == self.step else 0)
        yield from (
            (_(step1), numset, _(step2), numset2)
            for step1, numset, step2, numset2
            in self.atoms.get('hierarchy_add', ()))
    @property
    def hierachy_removed(self) -> iter:
        _ = lambda s: s + (self.step_modifier if s == self.step else 0)
        yield from (
            (_(step1), numset, _(step2), numset2)
            for step1, numset, step2, numset2
            in self.atoms.get('hierarchy_remove', ()))


    def edges_covered(self, sets:[frozenset]=None) -> iter:
        """If sets are given, the computation of edges covered by the motif
        is delegated to the searcher object.

        This allow to avoid a costly output from ASP.

        """
        if sets:  # give that to the searcher
            yield from frozenset(self.type.covered_edges(tuple(sets)))
        else:  # ASP provide us with the data
            yield from map(frozenset, self.atoms.get('covered_edge', ()))
