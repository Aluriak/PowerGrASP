
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
        for searcher in searchers:
            motif = searcher.search(step, score_to_beat)
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


def compress_by_cc(fname:str) -> [str]:
    """Yield bubble lines from compression of each cc found in given filename"""
    graphs = Graph.ccs_from_file(fname)
    for idx, graph in enumerate(graphs, start=1):
        yield '\n# CONNECTED COMPONENT {}'.format(idx)
        yield from compress(graph)


if __name__ == "__main__":
    # graphfile = 'data/ddiam.lp'
    # graphfile = 'data/one_edge.lp'
    # graphfile = 'data/clique.lp'
    # graphfile = 'data/perfectfit.lp'
    # graphfile = 'data/abnormal.lp'
    # graphfile = 'data/n8_d0.7.lp'
    # graphfile = 'data/hanging-bio-notree-cc0.lp'
    # graphfile = 'data/partition.lp'
    graphfile = 'data/cliques.lp'

    with open('out/out.bbl', 'w') as fd:
        for line in compress_by_cc(graphfile):
            fd.write(line + '\n')

