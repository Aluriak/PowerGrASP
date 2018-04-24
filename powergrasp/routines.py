"""Definition of high level functions operating the compression.

"""

from .searchers import CliqueSearcher, BicliqueSearcher, StarSearcher, NonStarBicliqueSearcher
from .graph import Graph
from .constants import MULTISHOT_MOTIF_SEARCH, BUBBLE_FOR_EACH_STEP, TIMERS, SHOW_STORY, STATISTIC_FILE, USE_STAR_MOTIF
from .motif_batch import MotifBatch


if TIMERS:
    import time
    def get_time() -> float: return round(time.time(), 2)
    if STATISTIC_FILE:
        # empty the file
        with open(STATISTIC_FILE, 'w') as fd:
            pass
        # function to fill it during compression
        def save_stats(*args):
            """Fill statistic file with given data"""
            with open(STATISTIC_FILE, 'a') as fd:
                fd.write(','.join(map(str, args)) + '\n')

def search_best_motifs(searchers, step) -> MotifBatch:
    """Return (new step, best_motif(s))"""
    score_to_beat = 0
    best_motifs, best_motifs_score = None, 0
    for searcher in sorted(searchers, key=lambda s: s.upperbound, reverse=True):
        motifs = MotifBatch(searcher.search(step, score_to_beat))
        if motifs and motifs.score > best_motifs_score:
            best_motifs, best_motifs_score = motifs, motifs.score
            score_to_beat = best_motifs_score
    return best_motifs


def compress(graph:Graph) -> [str]:
    """Yield bubble lines found in graph"""
    if TIMERS:
        timer_start = get_time()
        timer_last = timer_start
    if USE_STAR_MOTIF:
        searchers = CliqueSearcher(graph), NonStarBicliqueSearcher(graph), StarSearcher(graph)
    else:
        searchers = CliqueSearcher(graph), BicliqueSearcher(graph)
    if SHOW_STORY:
        print('INFO searchers: ' + ', '.join(s.name for s in searchers))
    step = 0
    complete_compression = True
    while True:
        step += 1
        try:
            best_motifs = search_best_motifs(searchers, step)
        except KeyboardInterrupt:
            print('WARNING interrupted search. Graph compression aborted. Output will be written.')
            complete_compression, best_motifs = False, None
            break
        if best_motifs:
            step += graph.compress_all(best_motifs.non_overlapping_subset())
            for searcher in searchers:
                searcher.on_new_compressed_motif(best_motifs)
            if BUBBLE_FOR_EACH_STEP:
                graph.output('out/out_k{}_s{}.bbl'.format(step, best_motif.score))
            if SHOW_STORY:
                print('INFO {} {} motif of score {} compressed'.format(best_motifs.count, best_motifs.name, best_motifs.score))
            if TIMERS:
                now = get_time()
                timers = round(now - timer_start, 2), round(now - timer_last, 2)
                if STATISTIC_FILE:
                    save_stats(*timers, best_motifs.name, best_motifs.score)
                if SHOW_STORY:
                    print("TIMER since start: {}s\t\tsince last motif: {}s"
                          "".format(*timers))
                timer_last = now
        else:
            break  # nothing to compress
    if TIMERS and SHOW_STORY:
        timer_output = get_time()
    yield from graph.bubble_repr(head_comment='Warning: incomplete compression (stopped at step {})'.format(step) if not complete_compression else '')
    if TIMERS and SHOW_STORY:
        now = get_time()
        timers = round(now - timer_start, 2), round(now - timer_output, 2)
        print("TIMER since start: {}s\t\toutput generation: {}s"
              "".format(*timers))


def compress_by_cc(fname:str) -> [str]:
    """Yield bubble lines from compression of each cc found in given filename"""
    graphs = Graph.ccs_from_file(fname)
    for idx, graph in enumerate(graphs, start=1):
        if idx > 1:  yield ''
        yield '# CONNECTED COMPONENT {}'.format(idx)
        yield from compress(graph)
