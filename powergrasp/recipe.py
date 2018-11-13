"""Definition of a Recipe.

"""

class RecipeError(ValueError):
    pass

class Recipe:
    RecipeError = RecipeError

    """Basically, a list of RecipeEntry"""

    def __init__(self, lines:iter):
        self._lines = tuple(RecipeEntry(*line) for line in lines)

    def __iter__(self):
        yield from self._lines

    def __len__(self):
        return len(self._lines)

    def __getitem__(self, idx):
        return self._lines[idx]

    def __str__(self):
        return f'<Recipe of {len(self._lines)} motifs>'

    def works_on(self, graph) -> bool:
        "True if the graph has a node referenced in self."
        for entry in self:
            if f'"{entry.one_node}"' in graph.nodes:
                return True
        return False


    @staticmethod
    def from_lines(lines:[str]) -> object:
        """Build a Recipe instance from given file"""
        def motif_from_line(line:str) -> (str, [str], [str]) or None:
            if not line or line.count('\t') != 2:
                return None  # not a Motif ; it needs to be looked by itself
            typemotif, seta, setb = line.split('\t')
            return set(typemotif.split(',')), set(seta.split(' ')), set(setb.split(' '))

        motifs = tuple(motif for motif in
                       map(motif_from_line, map(str.strip, lines)) if motif)
        return Recipe(
            (typemotifs, seta, setb) for typemotifs, seta, setb in motifs
        )

    @staticmethod
    def from_file(fname:str) -> object:
        """Build a Recipe instance from given file"""
        if fname is None: return Recipe(())
        with open(fname) as fd:
            return Recipe.from_lines(fd)


class RecipeEntry:
    RecipeError = RecipeError
    def __init__(self, typenames:set, seta:set, setb:set):
        self.typenames = frozenset(typenames)
        self.seta = frozenset(seta)
        self.setb = frozenset(setb)

    @property
    def isextendable(self) -> bool:
        return 'open' in self.typenames
    @property
    def islast(self) -> bool:
        return 'last' in self.typenames
    @property
    def isrequired(self) -> bool:
        return 'optional' not in self.typenames
    @property
    def one_node(self) -> str:
        """Return one node found in sets"""
        return next(iter(self.seta), None) or next(iter(self.setb))


    def __iter__(self):
        return iter((self.typenames, self.seta, self.setb))

    def __str__(self):
        return f"<RecipeEntry for {','.join(self.typenames)} with {{{','.join(self.seta)}}}×{{{','.join(self.setb)}}}>"

    def as_asp(self, is_star:bool):
        """Return ASP atoms translating the given recipe line"""
        typenames, seta, setb = self
        if min(setb) < min(seta):  # minimal element must be in seta
            setb, seta = seta, setb
        if is_star and len(seta) == 1:  # if it's a star, then single element must be in setb
            setb, seta = seta, setb
        return '\n'.join((
            ' '.join(f'newconcept(1,"{element}").' for element in seta),
            ' '.join(f'newconcept(2,"{element}").' for element in setb),
            # '|'.join(typenames) + '.'
        ))
