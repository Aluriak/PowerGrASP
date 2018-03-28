
# import utils
from searchers import CliqueSearcher, BicliqueSearcher
from graph import Graph


if __name__ == "__main__":
    # graphs = Graph.ccs_from_file('data/ddiam.lp')
    # graphs = Graph.ccs_from_file('data/one_edge.lp')
    # graphs = Graph.ccs_from_file('data/clique.lp')
    graphs = Graph.ccs_from_file('data/perfectfit.lp')
    for idx, graph in enumerate(graphs, start=1):

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
        graph.output('out/out_{}.bbl'.format(idx))

