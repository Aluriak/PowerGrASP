"""Batch of concurrent motif on a graph.

Offers an API useful for compression routine (access to score),
internal integrity test (equivalency of all contained motifs),
and non-overlapping subset selection.

"""

from itertools import islice
from powergrasp.motif import Motif
from powergrasp.constants import TEST_INTEGRITY


class MotifBatch:
    """Container of Motif"""

    def __init__(self, motifs:iter):
        self.motifs = tuple(motifs)
        self.score = self.motifs[0].score if self.motifs else None
        if TEST_INTEGRITY and self.score:
            scores = set(m.score for m in self.motifs)
            assert len(scores) == 1, "Multiple different scores in motifs: " + str(scores)

    def __bool__(self) -> bool:
        return bool(self.motifs)

    @property
    def empty(self) -> bool:
        return not self
    @property
    def name(self) -> str:  return self.motifs[0].typename
    @property
    def ismaximal(self) -> bool:  return self.motifs[0].ismaximal
    @property
    def count(self) -> int:  return len(self.motifs)


    def non_overlapping_subset(self) -> iter:
        """Yield motifs contained in self that are non overlapping between them.

        These motifs can all be compressed at the same time because they
        do not share any node.

        """
        if self.empty: return  # nothing to yield
        motifs = iter(self.motifs)
        first = next(motifs)
        nodes = frozenset(first.new_nodes)
        yield first
        for motif in motifs:
            motif_nodes = frozenset(motif.new_nodes)
            if motif_nodes.isdisjoint(nodes):
                nodes |= motif_nodes
                yield motif
