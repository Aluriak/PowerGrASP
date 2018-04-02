
# import utils
from searchers import CliqueSearcher, BicliqueSearcher
from graph import Graph


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
                best_motif = motif
                score_to_beat = best_motif.score
        if best_motif:
            graph.compress(best_motif)
            for searcher in searchers:
                searcher.on_new_compressed_motif(best_motif)
        else:
            break  # nothing to compress
    yield from graph.bubble_repr()


def compress_multishot(graph:Graph) -> [str]:
    """Yield bubble lines found in graph"""
    searchers = (CliqueSearcher(graph), BicliqueSearcher(graph))
    step = 0
    while True:
        step += 1
        score_to_beat = 0
        best_motifs, best_motifs_score = None, 0
        for searcher in sorted(searchers, key=lambda s: s.upperbound, reverse=True):
            score, motifs = searcher.search(step, score_to_beat)
            if score and score > best_motifs_score:
                best_motifs, best_motifs_score = motifs, score
                score_to_beat = best_motifs_score
        if best_motifs:
            graph.compress_all(best_motifs)
            for searcher in searchers:
                searcher.on_new_compressed_motif(best_motif)
        else:
            break  # nothing to compress
    yield from graph.bubble_repr()


def compress_by_cc(fname:str) -> [str]:
    """Yield bubble lines from compression of each cc found in given filename"""
    graphs = Graph.ccs_from_file(fname)
    for idx, graph in enumerate(graphs, start=1):
        if idx > 1:  yield ''
        yield '# CONNECTED COMPONENT {}'.format(idx)
        yield from compress(graph)


if __name__ == "__main__":
    # graphfile = 'data/ddiam.lp'
    # graphfile = 'data/one_edge.lp'
    # graphfile = 'data/clique.lp'
    # graphfile = 'data/perfectfit.lp'
    # graphfile = 'data/abnormal.lp'
    # graphfile = 'data/n8_d0.7.lp'
    # graphfile = 'data/partition.lp'
    # graphfile = 'data/cliques.lp'
    # graphfile = 'data/pnode-to-clique.lp'
    # graphfile = 'data/concomp.lp'
    # graphfile = 'data/perfectfit.lp'
    # graphfile = 'data/quoting.lp'
    # graphfile = 'data/variable-name.gml'
    # graphfile = 'data/hanging-bio-notree-cc0.lp'
    # graphfile = 'data/horrible_data.lp'
    # graphfile = 'data/hanging-study.lp'
    # graphfile = 'data/disjoint-subpnodes.lp'
    # graphfile = 'data/inclusions.lp'
    # graphfile = 'data/double_biclique_unambiguous.lp'
    graphfile = 'data/bintree.lp'

    with open('out/out.bbl', 'w') as fd:
        for line in compress_by_cc(graphfile):
            fd.write(line + '\n')

