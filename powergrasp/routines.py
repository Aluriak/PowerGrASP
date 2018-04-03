"""Definition of high level functions operating the compression.

"""

from .searchers import CliqueSearcher, BicliqueSearcher
from .graph import Graph
from .constants import MULTISHOT_MOTIF_SEARCH


def compress(graph:Graph) -> [str]:
    """Yield bubble lines found in graph"""
    searchers = (CliqueSearcher(graph), BicliqueSearcher(graph))
    step = 0
    while True:
        step += 1
        score_to_beat = 0
        best_motif = None
        for searcher in sorted(searchers, key=lambda s: s.upperbound, reverse=True):
            motif = next(searcher.search(step, score_to_beat), None)
            if motif and (best_motif is None or motif.score > best_motif.score):
                best_motif, score_to_beat = motif, motif.score
        if best_motif:
            graph.compress(best_motif)
            for searcher in searchers:
                searcher.on_new_compressed_motif(best_motif)
        else:
            break  # nothing to compress
    yield from graph.bubble_repr()


def compress_multishot(graph:Graph) -> [str]:
    """Yield bubble lines found in graph"""
    from motif_batch import MotifBatch
    searchers = (CliqueSearcher(graph), BicliqueSearcher(graph))
    step = 0
    while True:
        step += 1
        score_to_beat = 0
        best_motifs, best_motifs_score = None, 0
        for searcher in sorted(searchers, key=lambda s: s.upperbound, reverse=True):
            motifs = MotifBatch(searcher.search(step, score_to_beat))
            if motifs and motifs.score > best_motifs_score:
                best_motifs, best_motifs_score = motifs, motifs.score
                score_to_beat = best_motifs_score
        if best_motifs:
            step += graph.compress_all(best_motifs.non_overlapping_subset())
            for searcher in searchers:
                searcher.on_new_compressed_motif(best_motifs)
        else:
            break  # nothing to compress
    yield from graph.bubble_repr()


def compress_by_cc(fname:str) -> [str]:
    """Yield bubble lines from compression of each cc found in given filename"""
    graphs = Graph.ccs_from_file(fname)
    for idx, graph in enumerate(graphs, start=1):
        if idx > 1:  yield ''
        yield '# CONNECTED COMPONENT {}'.format(idx)
        if MULTISHOT_MOTIF_SEARCH:
            yield from compress_multishot(graph)
        else:
            yield from compress(graph)
