import itertools
from collections import defaultdict

class Motif:
    """A motif found by a motif searcher."""
    def __init__(self, typename:str, atoms:dict, maximal:bool, step:int):
        self.typename, self.atoms, self.ismaximal, self.step = str(typename), atoms, bool(maximal), int(step)
        print('MXVUFU:', self.atoms)
        self._score = None


    @property
    def name(self) -> str:  return self.name
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
        print('SCORE', score)
        return score


    @property
    def new_powernode(self) -> iter:
        yield from ((set, node) for _cc, _step, set, node in self.atoms.get('powernode', ()))
    @property
    def new_poweredge(self) -> iter:
        for args in self.atoms.get('poweredge', ()):
            if len(args) == 5:
                cc, step_a, set_a, step_b, set_b = args
                yield (step_a, set_a), (step_b, set_b)
            elif len(args) == 4:
                cc, step, set, node = args
                yield (step_a, set_a), node
    @property
    def edges_covered(self) -> iter:
        pnodes = defaultdict(set)
        for numset, node in self.new_powernode:
            pnodes[numset].add(node)
        yield from map(frozenset, itertools.product(*pnodes.values()))
    @property
    def blocks(self) -> iter:
        for args in self.atoms.get('block', ()):
            if len(args) == 3:
                _, step_a, set_a, node = args
                yield (step_a, set_a), node
            elif len(args) == 4:
                _, cc, node = args
                yield (0, 0), node
    @property
    def include_blocks(self) -> iter:
        for args in self.atoms.get('include_block', ()):
            if len(args) == 5:
                _, step_a, set_a, step_b, set_b = args
                yield (step_a, set_a), (step_b, set_b)
            elif len(args) == 4:
                _, cc, step, set = args
                yield (0, 0), (step, set)
    # @property
    # def hierachy_added(self) -> iter:
        # yield from self.atoms.get('hierarchy_add', ())
    # @property
    # def hierachy_removed(self) -> iter:
        # yield from self.atoms.get('hierarchy_remove', ())
